# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:48:31 2021

@author: ys.leng
"""
import numpy as np
import os
import pandas as pd
import openpyxl

parent_dir = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0225_wirecard" # change into current path
os.chdir(parent_dir)
df = pd.read_csv(os.path.join(parent_dir, "0225_mapped_wirecard.csv")).reset_index(drop=True)
target_company = "Wirecard AG"
output_csv_file = "0225_prolong_Wirecard_0trailing.csv"
output_xlsx_file = "0225_prolong_Wirecard_0trailing.xlsx"
bert_input_file = os.path.join(parent_dir, "test_NLI_M_0trailing.csv")

prolong = 0
selected_idx = []
row_num = df.shape[0]
idx = 0

while idx < row_num:
    # print(idx)
    # if df.loc[idx, "db_company"] != "No Mapping":

    if df.loc[idx, "db_company"].strip() == target_company:
        curr_db_company = df.loc[idx, "db_company"]
        curr_company = df.loc[idx, "companies"]
        curr_u4 = df.loc[idx, "compID_u4"]
        curr_u3 = df.loc[idx, "compID_u3"]
        curr_ratio = df.loc[idx, "ratio"]
        selected_idx.append(idx)
        curr_id = df.loc[idx, "id"]
        curr_text_label = df.loc[idx, "text_labels"]

        idx += 1

        if idx < row_num and df.loc[idx, "id"] == curr_id:
            while idx < row_num and df.loc[idx, "id"] == curr_id:
                if df.loc[idx, "db_company"] != "No Mapping":
                    selected_idx.append(idx)
                idx += 1
        else:
            while idx < row_num:
                if df.loc[idx, "text_labels"] != curr_text_label:
                    break
                else:
                    print(df.loc[idx, "id"], curr_id, df.loc[idx, "companies"])
                    if df.loc[idx, "id"] - curr_id <= prolong and len(
                            df.loc[idx, "sentence_1"].strip().split(" ")) >= 3 and pd.isna(df.loc[idx, "companies"]):
                        # print(df.loc[temp_idx, "sentence_1"], len(df.loc[temp_idx, "sentence_1"].strip().split(' ')))

                        selected_idx.append(idx)
                        df.loc[idx, "db_company"] = curr_db_company
                        df.loc[idx, "companies"] = curr_company
                        df.loc[idx, "compID_u4"] = curr_u4
                        df.loc[idx, "compID_u3"] = curr_u3
                        df.loc[idx, "ratio"] = curr_ratio
                    else:
                        break
                idx += 1
    else:
        idx += 1

selected_df = df.loc[selected_idx]
# print(selected_df.shape)


data2 = selected_df
data2.to_csv(os.path.join(parent_dir, output_csv_file), index=False)
data2.to_excel(os.path.join(parent_dir, output_xlsx_file), index=False)
data2["label"] = 1
test_df = data2[["id", "sentence_1", "sentence_2", "label"]]
test_df.to_csv(bert_input_file, header=None, sep='\t', index=False)
