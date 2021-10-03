# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:52:15 2021

@author: ys.leng
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

key_label = 'Green_Economy'

def get_cr_theta(theta):
    theta = theta.split()
    # print(theta)
    for i in range(len(theta)):
        if i==0:
            theta[i] = int(theta[i])
        else:
            theta[i] = theta[i].split(':')
            # print(theta[i])
            if key_label in theta[i][0]:
                # print("yes")
                return float(theta[i][1])
            

parent_dir = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_pre_lda\output_k_4_neg_ks2"
os.chdir(parent_dir)
output_path = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_pre_lda\weight_ge_4_ks2.txt"

## read weight
weight_list = []

with open("theta.dat", "r", encoding="utf-8") as f:
    # infor_list = [s.split(' ') for s in f.read().strip('\n').split('\n')]
    thetas = f.readlines()
    
for theta in thetas:
    weight_list.append(str(get_cr_theta(theta)))
    # print(str(get_cr_theta(theta)))

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(weight_list))


real_id_path = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_pre_lda\lda_fact_id.dat"
total_id_path = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_pre_lda\lda_fact_id_neg.dat"

# read all sample ariticle
with open(real_id_path, "r", encoding='utf-8') as f:
    file_list = f.read().strip().split('\n')

with open(total_id_path, "r", encoding='utf-8') as f:
    total_file_list = f.read().strip().split('\n')

key_file_set = set(file_list)
labels = []

for file, weight in zip(total_file_list, weight_list):
    if file in key_file_set:
        labels.append(2)
    else:
        labels.append(1)

temp_df = pd.DataFrame({"text_num": total_file_list,
                        "lda_weight": weight_list,
                        "label": labels})

for i in range(1, 3):
    subset = temp_df[temp_df.label==i]    
    sns.distplot(subset["lda_weight"], hist = True, kde = True,kde_kws = {'linewidth': 2}, label=str(i))
plt.legend(title = 'Class')
plt.xlabel('lda_weight')
plt.ylabel('Density')


selected_num = list(temp_df.sort_values("lda_weight", ascending=False)["text_num"])[:20]
article_output_path = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0308\ge_article_top"
article_input_path = r"\\cri-hpc19\NLP\Logistic\From DataBase\all"

import shutil
for num in selected_num:
    curr_file = "{}.txt".format(num)
    shutil.copyfile(os.path.join(article_input_path, curr_file),
                    os.path.join(article_output_path, curr_file))
