# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 18:22:57 2021

@author: ys.leng
"""

import argparse

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

parser.print_help()