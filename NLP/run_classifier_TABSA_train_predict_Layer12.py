# coding=utf-8

"""BERT finetuning runner."""

from __future__ import absolute_import, division, print_function

import argparse
import collections
import logging
import os
import random
import time
import math

from numba import cuda
import numpy as np
import torch
torch.cuda.empty_cache()
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler, SequentialSampler
from tqdm import tqdm, trange

import utils.tokenization as tokenization
from utils.modeling import BertConfig, BertForSequenceClassification, BertForSequenceNewClassification
from utils.optimization import BERTAdam
from utils.processor import (Semeval_NLI_B_Processor, Semeval_NLI_M_Processor,
                       Semeval_QA_B_Processor, Semeval_QA_M_Processor,
                       Semeval_single_Processor, Sentihood_NLI_B_Processor,
                       Sentihood_NLI_M_Processor, Sentihood_QA_B_Processor,
                       Sentihood_QA_M_Processor, Sentihood_single_Processor)

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_id):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id


def convert_examples_to_features(examples, label_list, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""

    label_map = {}
    for (i, label) in enumerate(label_list):
        label_map[label] = i

    print(label_map)
    features = []
    for (ex_index, example) in enumerate(tqdm(examples)):
        tokens_a = tokenizer.tokenize(example.text_a)

        tokens_b = None
        if example.text_b:
            tokens_b = tokenizer.tokenize(example.text_b)

        if tokens_b:
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3"
            _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        else:
            # Account for [CLS] and [SEP] with "- 2"
            if len(tokens_a) > max_seq_length - 2:
                tokens_a = tokens_a[0:(max_seq_length - 2)]

        # The convention in BERT is:
        # (a) For sequence pairs:
        #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
        #  type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
        # (b) For single sequences:
        #  tokens:   [CLS] the dog is hairy . [SEP]
        #  type_ids: 0   0   0   0  0     0 0
        #
        # Where "type_ids" are used to indicate whether this is the first
        # sequence or the second sequence. The embedding vectors for `type=0` and
        # `type=1` were learned during pre-training and are added to the wordpiece
        # embedding vector (and position vector). This is not *strictly* necessary
        # since the [SEP] token unambigiously separates the sequences, but it makes
        # it easier for the model to learn the concept of sequences.
        #
        # For classification tasks, the first vector (corresponding to [CLS]) is
        # used as as the "sentence vector". Note that this only makes sense because
        # the entire model is fine-tuned.
        tokens = []
        segment_ids = []
        tokens.append("[CLS]")
        segment_ids.append(0)
        for token in tokens_a:
            tokens.append(token)
            segment_ids.append(0)
        tokens.append("[SEP]")
        segment_ids.append(0)

        if tokens_b:
            for token in tokens_b:
                tokens.append(token)
                segment_ids.append(1)
            tokens.append("[SEP]")
            segment_ids.append(1)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1] * len(input_ids)

        # Zero-pad up to the sequence length.
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length

        if math.isnan(float(example.label)):
            continue
        label_id = label_map[str(int(float(example.label)))]

        features.append(
                InputFeatures(
                        input_ids=input_ids,
                        input_mask=input_mask,
                        segment_ids=segment_ids,
                        label_id=label_id))
    return features


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--task_name",
                        default=None,
                        type=str,
                        required=True,
                        choices=["sentihood_single", "sentihood_NLI_M", "sentihood_QA_M", \
                                "sentihood_NLI_B", "sentihood_QA_B", "semeval_single", \
                                "semeval_NLI_M", "semeval_QA_M", "semeval_NLI_B", "semeval_QA_B"],
                        help="The name of the task to train.")
    parser.add_argument("--data_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The input data dir. Should contain the .tsv files (or other data files) for the task.")
    parser.add_argument("--vocab_file",
                        default=None,
                        type=str,
                        required=True,
                        help="The vocabulary file that the BERT model was trained on.")
    parser.add_argument("--bert_config_file",
                        default=None,
                        type=str,
                        required=True,
                        help="The config json file corresponding to the pre-trained BERT model. \n"
                             "This specifies the model architecture.")
    parser.add_argument("--output_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The output directory where the model checkpoints will be written.")

    ## Other parameters
    parser.add_argument("--init_checkpoint",
                        default=None,
                        type=str,
                        help="Initial checkpoint (usually from a pre-trained BERT model).")
    parser.add_argument("--init_eval_checkpoint",
                        default=None,
                        type=str,
                        help="Initial checkpoint (usually from a pre-trained BERT model + classifier).")
    parser.add_argument("--do_save_model",
                        default=False,
                        action='store_true',
                        help="Whether to save model.")
    parser.add_argument("--eval_test",
                        default=False,
                        action='store_true',
                        help="Whether to run eval on the test set.")
    parser.add_argument("--do_lower_case",
                        default=False,
                        action='store_true',
                        help="Whether to lower case the input text. True for uncased models, False for cased models.")
    parser.add_argument("--max_seq_length",
                        default=128,
                        type=int,
                        help="The maximum total input sequence length after WordPiece tokenization. \n"
                             "Sequences longer than this will be truncated, and sequences shorter \n"
                             "than this will be padded.")
    parser.add_argument("--train_batch_size",
                        default=32,
                        type=int,
                        help="Total batch size for training.")
    parser.add_argument("--eval_batch_size",
                        default=8,
                        type=int,
                        help="Total batch size for eval.")
    parser.add_argument("--learning_rate",
                        default=5e-5,
                        type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument("--num_train_epochs",
                        default=3.0,
                        type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--warmup_proportion",
                        default=0.1,
                        type=float,
                        help="Proportion of training to perform linear learning rate warmup for. "
                             "E.g., 0.1 = 10%% of training.")
    parser.add_argument("--no_cuda",
                        default=False,
                        action='store_true',
                        help="Whether not to use CUDA when available")
    parser.add_argument("--accumulate_gradients",
                        type=int,
                        default=1,
                        help="Number of steps to accumulate gradient on (divide the batch_size and accumulate)")
    parser.add_argument("--local_rank",
                        type=int,
                        default=-1,
                        help="local_rank for distributed training on gpus")
    parser.add_argument('--seed',
                        type=int,
                        default=42,
                        help="random seed for initialization")
    parser.add_argument('--gradient_accumulation_steps',
                        type=int,
                        default=1,
                        help="Number of updates steps to accumualte before performing a backward/update pass.")
    parser.add_argument('--seed_num',
                        type=int,
                        default=1,
                        help="random seed number for iteration")
    args = parser.parse_args()

    print('-' * 20 + "Check Parameters" + '-' * 20)
    print("local rank:", args.local_rank)
    print("no_cuda:", args.no_cuda)
    print('-' * 20 + "End Check Parameters" + '-' * 20)


    if args.local_rank == -1 or args.no_cuda:
        device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
        n_gpu = torch.cuda.device_count()
    else:
        device = torch.device("cuda", args.local_rank)
        n_gpu = 1
        # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
        torch.distributed.init_process_group(backend='nccl')
    logger.info("device %s n_gpu %d distributed training %r", device, n_gpu, bool(args.local_rank != -1))

    print('-' * 20 + "Check Device" + '-' * 20)
    print(device)
    print('-' * 20 + "End Check Device" + '-' * 20)

    if args.accumulate_gradients < 1:
        raise ValueError("Invalid accumulate_gradients parameter: {}, should be >= 1".format(
                            args.accumulate_gradients))

    args.train_batch_size = int(args.train_batch_size / args.accumulate_gradients)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    np.random.seed(args.seed)
    seeds = np.random.randint(0, 1000, args.seed_num)
    # seeds = [121]


    # random.seed(args.seed)
    # np.random.seed(args.seed)
    # torch.manual_seed(args.seed)

    seed_log_path = os.path.join(args.output_dir, "seeds_records.txt")
    seed_log = open(seed_log_path, 'wt')

    seed_log.write("Learning Rate: {}\n".format(args.learning_rate))
    seed_log.write("Max Seq Length: {}\n".format(args.max_seq_length))
    seed_log.write("Train Batch Size: {}\n\n".format(args.train_batch_size))

    curr_best_model = None
    curr_best_dev_accu = 0

    for seed in seeds:
        print("SEED: {}".format(seed))
        seed_log.write("seed: {}\n".format(seed))
        seed_log.write("================\n")
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(args.seed)

        # if n_gpu > 0:
        #     torch.cuda.manual_seed_all(args.seed)

        bert_config = BertConfig.from_json_file(args.bert_config_file)

        if args.max_seq_length > bert_config.max_position_embeddings:
            raise ValueError(
                "Cannot use sequence length {} because the BERT model was only trained up to sequence length {}".format(
                args.max_seq_length, bert_config.max_position_embeddings))

        # if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
        #     raise ValueError("Output directory ({}) already exists and is not empty.".format(args.output_dir))
        # os.makedirs(args.output_dir, exist_ok=True)




        # prepare dataloaders
        processors = {
            "sentihood_single":Sentihood_single_Processor,
            "sentihood_NLI_M":Sentihood_NLI_M_Processor,
            "sentihood_QA_M":Sentihood_QA_M_Processor,
            "sentihood_NLI_B":Sentihood_NLI_B_Processor,
            "sentihood_QA_B":Sentihood_QA_B_Processor,
            "semeval_single":Semeval_single_Processor,
            "semeval_NLI_M":Semeval_NLI_M_Processor,
            "semeval_QA_M":Semeval_QA_M_Processor,
            "semeval_NLI_B":Semeval_NLI_B_Processor,
            "semeval_QA_B":Semeval_QA_B_Processor,
        }

        processor = processors[args.task_name]()
        label_list = processor.get_labels()

        tokenizer = tokenization.FullTokenizer(
            vocab_file=args.vocab_file, do_lower_case=args.do_lower_case)

        # training set
        train_examples = None
        num_train_steps = None
        train_examples = processor.get_train_examples(args.data_dir)
        num_train_steps = int(
            len(train_examples) / args.train_batch_size * args.num_train_epochs)

        train_features = convert_examples_to_features(
            train_examples, label_list, args.max_seq_length, tokenizer)
        logger.info("***** Running training *****")
        logger.info("  Num examples = %d", len(train_examples))
        logger.info("  Batch size = %d", args.train_batch_size)
        logger.info("  Num steps = %d", num_train_steps)

        all_input_ids = torch.tensor([f.input_ids for f in train_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in train_features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in train_features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_id for f in train_features], dtype=torch.long)

        train_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
        if args.local_rank == -1:
            train_sampler = RandomSampler(train_data)
        else:
            train_sampler = DistributedSampler(train_data)
        train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=args.train_batch_size)

        # dev set
        dev_examples = processor.get_dev_examples(args.data_dir)
        dev_features = convert_examples_to_features(
            dev_examples, label_list, args.max_seq_length, tokenizer)

        all_input_ids = torch.tensor([f.input_ids for f in dev_features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in dev_features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in dev_features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_id for f in dev_features], dtype=torch.long)

        dev_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
        dev_dataloader = DataLoader(dev_data, batch_size=args.eval_batch_size, shuffle=False)

        # test set
        if args.eval_test:
            test_examples = processor.get_test_examples(args.data_dir)
            test_features = convert_examples_to_features(
                test_examples, label_list, args.max_seq_length, tokenizer)

            all_input_ids = torch.tensor([f.input_ids for f in test_features], dtype=torch.long)
            all_input_mask = torch.tensor([f.input_mask for f in test_features], dtype=torch.long)
            all_segment_ids = torch.tensor([f.segment_ids for f in test_features], dtype=torch.long)
            all_label_ids = torch.tensor([f.label_id for f in test_features], dtype=torch.long)

            test_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
            test_dataloader = DataLoader(test_data, batch_size=args.eval_batch_size, shuffle=False)


        # model and optimizer
        model = BertForSequenceClassification(bert_config, len(label_list))

        # # new model
        # hidden_layer_num = 128
        # model = BertForSequenceNewClassification(bert_config, hidden_layer_num, len(label_list))
        print(os.path.join(os.getcwd(), args.init_checkpoint))
        # print(os.path.join(os.getcwd(), args.init_eval_checkpoint))

        if args.init_eval_checkpoint is not None:
            model.bert.load_state_dict(torch.load(os.path.join(os.getcwd(), args.init_checkpoint), map_location='cpu'))
            model.load_state_dict(torch.load(os.path.join(os.getcwd(), args.init_eval_checkpoint), map_location='cpu'))
        elif args.init_checkpoint is not None:
            model.bert.load_state_dict(torch.load(os.path.join(os.getcwd(), args.init_checkpoint), map_location='cpu'))
        model.to(device)


        # for name, param in model.named_parameters():
        #     # if epoch == 1:
        #     #     if param.requires_grad:
        #     #         prev_layer_dict[name] = param.data.clone()
        #     if "bert" in name:
        #         # if 'embeddings' in name:
        #         #     param.requires_grad = False
        #         # else:
        #         #     if "encoder" in name:
        #         #         this_num = int(name.split('.')[3])
        #         #         if this_num <= 12:
        #         #             param.requires_grad = False
        #         param.requires_grad = False

        # for name, param in model.named_parameters():
        #     # if epoch == 1:
        #     #     if param.requires_grad:
        #     #         prev_layer_dict[name] = param.data.clone()
        #     print(name, ":", param.requires_grad)

        if args.local_rank != -1:
            model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank],
                                                        output_device=args.local_rank)
        elif n_gpu > 1:
            model = torch.nn.DataParallel(model)

        no_decay = ['bias', 'gamma', 'beta']
        optimizer_parameters = [
            {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay_rate': 0.01},
            {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay_rate': 0.0}
            ]

        optimizer = BERTAdam(optimizer_parameters,
                            lr=args.learning_rate,
                            warmup=args.warmup_proportion,
                            t_total=num_train_steps)

        # train
        output_log_file = os.path.join(args.output_dir, "log.txt")
        print("output_log_file=",output_log_file)
        with open(output_log_file, "w") as writer:
            if args.eval_test:
                writer.write("epoch\tglobal_step\tloss\ttest_loss\ttest_accuracy\n")
            else:
                writer.write("epoch\tglobal_step\tloss\n")

        global_step = 0
        epoch = 0
        prev_layer_dict = dict()


        if args.init_eval_checkpoint is None and args.init_checkpoint is not None:
            for _ in trange(int(args.num_train_epochs), desc="Epoch"):
                epoch += 1
                print("============={}=============".format(epoch))
                model.train()
                tr_loss = 0
                nb_tr_examples, nb_tr_steps = 0, 0
                for step, batch in enumerate(train_dataloader):
                    batch = tuple(t.to(device) for t in batch)
                    input_ids, input_mask, segment_ids, label_ids = batch
                    loss, _ = model(input_ids, segment_ids, input_mask, label_ids)
                    if n_gpu > 1:
                        loss = loss.mean() # mean() to average on multi-gpu.
                    if args.gradient_accumulation_steps > 1:
                        loss = loss / args.gradient_accumulation_steps
                    loss.backward()
                    tr_loss += loss.item()
                    nb_tr_examples += input_ids.size(0)
                    nb_tr_steps += 1
                    if (step + 1) % args.gradient_accumulation_steps == 0:
                        optimizer.step()    # We have accumulated enought gradients
                        model.zero_grad()
                        global_step += 1

                # this_counter = 0

                # for name, param in model.named_parameters():
                #     if epoch == 1:
                #         if param.requires_grad:
                #             prev_layer_dict[name] = param.data.clone()

                #     else:
                #         if param.requires_grad:
                #             print(name, ":", torch.equal(prev_layer_dict[name], param.data))
                #             prev_layer_dict[name] = param.data.clone()
                #     this_counter += 1
                #     if this_counter >= 6:
                #         break

                model.eval()
                train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=args.train_batch_size)

                # all 'test' should be replaced by 'train'
                test_loss, test_accuracy = 0, 0
                nb_test_steps, nb_test_examples = 0, 0
                for input_ids, input_mask, segment_ids, label_ids in train_dataloader:
                    input_ids = input_ids.to(device)
                    input_mask = input_mask.to(device)
                    segment_ids = segment_ids.to(device)
                    label_ids = label_ids.to(device)

                    with torch.no_grad():
                        tmp_test_loss, logits = model(input_ids, segment_ids, input_mask, label_ids)

                    logits = F.softmax(logits, dim=-1)
                    logits = logits.detach().cpu().numpy()
                    label_ids = label_ids.to('cpu').numpy()
                    # print label_ids to see wheter they are true
                    outputs = np.argmax(logits, axis=1)
                    tmp_test_accuracy=np.sum(outputs == label_ids)

                    test_loss += tmp_test_loss.mean().item()
                    test_accuracy += tmp_test_accuracy

                    nb_test_examples += input_ids.size(0)
                    nb_test_steps += 1

                test_loss = test_loss / nb_test_steps
                test_accuracy = test_accuracy / nb_test_examples

                print("train_loss:", test_loss)
                print("train_accuracy:", test_accuracy)

                seed_log.write("Epoch: {}\n".format(epoch))
                seed_log.write("train_loss: {}\n".format(test_loss))
                seed_log.write("train_accuracy: {}\n".format(test_accuracy))


                # all 'test' should be replaced by 'dev'
                test_loss, test_accuracy = 0, 0
                revised_test_accuracy = 0
                nb_test_steps, nb_test_examples = 0, 0
                with open(os.path.join(args.output_dir, f"dev_ep_{seed}_seed_{epoch}.txt"), "w") as f_test:
                    for input_ids, input_mask, segment_ids, label_ids in dev_dataloader:
                        input_ids = input_ids.to(device)
                        input_mask = input_mask.to(device)
                        segment_ids = segment_ids.to(device)
                        label_ids = label_ids.to(device)

                        with torch.no_grad():
                            tmp_test_loss, logits = model(input_ids, segment_ids, input_mask, label_ids)

                        logits = F.softmax(logits, dim=-1)
                        logits = logits.detach().cpu().numpy()
                        label_ids = label_ids.to('cpu').numpy()
                        # print label_ids to see wheter they are true
                        outputs = np.argmax(logits, axis=1)
                        for output_i in range(len(outputs)):
                            f_test.write(str(outputs[output_i]))
                            for ou in logits[output_i]:
                                f_test.write(" "+str(ou))
                            f_test.write("\n")
                        tmp_test_accuracy=np.sum(outputs == label_ids)

                        # print(outputs)
                        # print(label_ids)
                        for i in range(len(outputs)):
                            if outputs[i] == 2 and label_ids[i] == 2:
                                revised_test_accuracy += 1
                            elif outputs[i] in [0, 1] and label_ids[i] in [0, 1]:
                                revised_test_accuracy += 1
                            elif outputs[i] in [3, 4] and label_ids[i] in [3, 4]:
                                revised_test_accuracy += 1

                        test_loss += tmp_test_loss.mean().item()
                        test_accuracy += tmp_test_accuracy

                        nb_test_examples += input_ids.size(0)
                        nb_test_steps += 1

                test_loss = test_loss / nb_test_steps
                test_accuracy = test_accuracy / nb_test_examples
                revised_test_accuracy = revised_test_accuracy / nb_test_examples

                print("dev_loss:", test_loss)
                print("dev_accuracy:", test_accuracy)
                print("revised_dev_accuracy:", revised_test_accuracy)
                print('-' * 20)

                if args.do_save_model and test_accuracy > curr_best_dev_accu:
                    if n_gpu > 1:
                        curr_best_model = model.module.state_dict()
                    else:
                        curr_best_model = model.state_dict()
                    curr_best_dev_accu = test_accuracy
                    print("UPDATE MODEL")

                seed_log.write("dev_loss: {}\n".format(test_loss))
                seed_log.write("dev_accuracy: {}\n".format(test_accuracy))
                seed_log.write("revised_dev_accuracy: {}\n".format(revised_test_accuracy))

        seed_log.write("\n")

        # # output the ultimate model
        # if args.do_save_model:
        #     if n_gpu > 1:
        #         torch.save(model.module.state_dict(), os.path.join(args.output_dir, f'model_ep_{seed}.bin'))
        #     else:
        #         torch.save(model.state_dict(), os.path.join(args.output_dir, f'model_ep_{seed}.bin'))


        if args.eval_test:
            # model = curr_best_model
            model.eval()
            test_loss, test_accuracy = 0, 0
            nb_test_steps, nb_test_examples = 0, 0
            with open(os.path.join(args.output_dir, f"test_ep_{seed}.txt"), "w") as f_test:
                for input_ids, input_mask, segment_ids, label_ids in test_dataloader:
                    input_ids = input_ids.to(device)
                    input_mask = input_mask.to(device)
                    segment_ids = segment_ids.to(device)
                    label_ids = label_ids.to(device)

                    with torch.no_grad():
                        tmp_test_loss, logits = model(input_ids, segment_ids, input_mask, label_ids)

                    logits = F.softmax(logits, dim=-1)
                    logits = logits.detach().cpu().numpy()
                    label_ids = label_ids.to('cpu').numpy()
                    outputs = np.argmax(logits, axis=1)
                    for output_i in range(len(outputs)):
                        f_test.write(str(outputs[output_i]))
                        for ou in logits[output_i]:
                            f_test.write(" "+str(ou))
                        f_test.write("\n")
                    tmp_test_accuracy=np.sum(outputs == label_ids)

                    test_loss += tmp_test_loss.mean().item()
                    test_accuracy += tmp_test_accuracy

                    nb_test_examples += input_ids.size(0)
                    nb_test_steps += 1
                    if nb_test_steps % 100 == 0:
                        print("Done: {}".format(nb_test_steps))

            # test_loss = test_loss / nb_test_steps
            # test_accuracy = test_accuracy / nb_test_examples
    if args.do_save_model:
        torch.save(curr_best_model, os.path.join(args.output_dir, f'model_best.bin'))
    seed_log.write("=" * 20 + "\n")
    seed_log.write("best_dev_accuracy: {}\n".format(curr_best_dev_accu))
    seed_log.write("=" * 20 + "\n")
    seed_log.close()

    #     result = collections.OrderedDict()
    #     if args.eval_test:
    #         result = {'epoch': epoch,
    #                 'global_step': global_step,
    #                 #'loss': tr_loss/nb_tr_steps,
    #                 'test_loss': test_loss,
    #                 'test_accuracy': test_accuracy}
    #     else:
    #         result = {'epoch': epoch,
    #                 'global_step': global_step,
    #                 'loss': tr_loss/nb_tr_steps}

    #     logger.info("***** Eval results *****")
    #     with open(output_log_file, "a+") as writer:
    #         for key in result.keys():
    #             logger.info("  %s = %s\n", key, str(result[key]))
    #             writer.write("%s\t" % (str(result[key])))
    #         writer.write("\n")

if __name__ == "__main__":
    start = time.time()
    # device = cuda.get_current_device()
    # device.reset()
    main()
    torch.cuda.empty_cache()
    print("Finish: {}".format(time.time() - start))
