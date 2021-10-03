# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:01:10 2021

@author: ys.leng
"""
import nltk
import pandas as pd
import os
import argparse

def get_list_from_text(name):
    with open(name, "r", encoding="utf-8") as my_file:
        elements = my_file.readlines()
    del elements[0]
    element_list = elements
    element_lower_text = [w.lower() for w in elements]
    element_lower_text = [x.replace('\n', '') for x in element_lower_text]
    element_lower_text = [x.replace('/', '') for x in element_lower_text]
    element_lower_text = [x.replace(',', '') for x in element_lower_text]
    return [element_list, element_lower_text]

industry_name_lower = get_list_from_text(r"\\UNICORN7\TeamData\RT1\ToMeng-jou\NLP\LDA\list\industry_name.txt")[1]

stop_list = industry_name_lower
stop_list1 = nltk.corpus.stopwords.words('english')

def generate_trie(trie, word_list):
    interval = 10000
    for i, word in enumerate(word_list):
        if i % interval == 0:
            print("Done: {}".format(i))
        trie.add_word(word)

class Trie:
    def __init__(self, head):
        self.label = head
        self.branches = dict()
        self.stop = False
    
    def add_char(self, curr_char):
        if curr_char not in self.branches:
            self.branches[curr_char] = Trie(curr_char)
        return self.branches[curr_char]

    def add_word(self, word):
        curr_node = self
        for i in range(len(word)):
            curr_node = curr_node.add_char(word[i])
        curr_node.stop = True
    
    def search_word(self, word):
        curr_node = self
        for i in range(len(word)):
            curr_char = word[i]
            if curr_char not in curr_node.branches:
                return False
            curr_node = curr_node.branches[curr_char]
        return curr_node.stop

    def extract_company(self, sent):
        comp_list = []
        i = 0
        while i < len(sent):
            # print(i)
            curr_node = self
            start = i
            while i < len(sent):
                curr_char = sent[i]
                if curr_char in curr_node.branches:
                    i += 1
                    curr_node = curr_node.branches[curr_char]
                else:
                    break
            if i != start and curr_node.stop:
                comp_list.append(sent[start:i])
            else:
            # if i != start:
            #     comp_list.append(sent[start:i])
                i = start + 1
        return comp_list
    
    def is_contain(self, word):
        if not word:
            return True
        elif not self.branches:
            return False
        else:
            if word[0] == self.label:
                temp_word = word[1:]
                return any([s.is_contain(temp_word) for s in self.branches.values()])
            else:
                return any([s.is_contain(word) for s in self.branches.values()])
            
def get_from_range(start, end, path):
    '''load data using range'''
    Title_list = []
    Date_list = []
    Content_list = []
    Index_list = []
    for i in range(start, end+1):
        try:
            with open(os.path.join(path, "{}.txt".format(i)), "r", encoding="utf-8") as f:
                data = f.read().split('\n')
            Date_list.append(data[1])
            Title_list.append(data[0])
            Content_list.append(data[2])
            Index_list.append(i)
        except:
            continue
    return Title_list, Date_list, Content_list, Index_list

def remove_company_name(content_text, head_trie):
    # after_del = ''
    temp_entity_group = head_trie.extract_company(content_text)
    return content_text, temp_entity_group


def replace_company_name(tokenized_text, head_trie):
    '''replace company name with location'''
    tagged_text_list=[]
    companies_list = []
    total_del = ""
    for text in tokenized_text:
        after_del,company_list = remove_company_name(text, head_trie)
        # print(company_list)
        if company_list:
            print(company_list)
        companies_list.append(company_list)
        if not company_list:
            tagged_text_list.append(after_del)
            total_del += after_del
        else:
            after_del_1 = after_del
            after_del_2 = after_del
            for i,company in enumerate(company_list):
                after_del_1 = after_del_1.replace(company,'location - '+str(i+1),1)
                after_del_2 = after_del_2.replace(company, "")
            tagged_text_list.append(after_del_1)
            total_del += after_del_2
    return tagged_text_list, companies_list, total_del


def generate_text_sentence(pair):
    
    Title_list, Date_list, text, start, output_dir, index = pair

    # load comppany infor
    # u3_comp_info = sql_query('select * from tier2.ref.COMPANY_NUMBER_MAPPING_TEMP')
    
    tokenized_text = nltk.sent_tokenize(text)

    # # print(index)

    text_label = [start + index] * len(tokenized_text)
    text_title = [Title_list] * len(tokenized_text)
    text_date = [Date_list] * len(tokenized_text)
    df_sentence = pd.DataFrame({"sentences":tokenized_text,"text_labels":text_label,"Title":text_title,"Date":text_date})
    df_sentence.to_csv(os.path.join(output_dir, "sentence\sentence_{}.csv".format(start + index)))

        
    Tagged_text_list, Companies_list, after_del = replace_company_name(tokenized_text, head_trie)
    df_sentences = generate_sentences_information(Tagged_text_list, Companies_list, Title_list, Date_list, start + index)    
    df_sentences.to_csv(os.path.join(output_dir, "sentence_with_location\sentence_with_location_{}.csv".format(start + index)))
    # # print(after_del)
    try:
        lda_text = generate_lda(after_del)
        
        with open(os.path.join(output_dir, "lda_input\lda_{}.dat".format(start + index)), 'w', encoding='utf-8') as ff:
            ff.write(lda_text)
            ff.write('\n')
    except:
        return


# main
parser = argparse.ArgumentParser()
parser.add_argument('--start',
                    type=int,
                    default=0,
                    help="article range start")
parser.add_argument('--end', 
                    type=int, 
                    default=1,
                    help="article range end")    
parser.add_argument("--target_index",
                    type=str,
                    default="",
                    help="given txt file storing article index")
parser.add_argument("--read_list",
                    type=int,
                    default=0,
                    help="whether read files directly or not")
args = parser.parse_args()
start = args.start
end = args.end
read_judge = args.read_list


parent_dir = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0208"
input_dir = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_article"
output_dir = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_pre_lda"

comp_file = "U3_companyNames.xlsx"
company_infor = pd.read_excel(os.path.join(parent_dir, comp_file))
company_infor = company_infor[[company_infor.columns[0], company_infor.columns[-1]]]
company_infor.columns = ["u3id", "company"]
comp_id_dict = dict()
comp_list = company_infor["company"].tolist()
comp_list = [comp_name for comp_name in comp_list if len(comp_name) > 5]
for i in company_infor.index:
    comp_id_dict[company_infor.loc[i, "company"]] = company_infor.loc[i, "u3id"]


head_trie = Trie("")
generate_trie(head_trie, comp_list)

Title_list, Date_list, Content_list, index = get_from_range(start, end, input_dir)

generate_text_sentence()