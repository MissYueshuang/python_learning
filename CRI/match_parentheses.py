# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:02:49 2020

brace check

@author: rmileng
"""

def match_parentheses(braces):
    ls = []
    parentheses = '()[]{}'
    for i in range(len(braces)):
        # if not parentheses, continue
        si = braces[i]
        if parentheses.find(si) == -1:
            continue
        # 左括号入栈
        if si == '(' or si == '[' or si == '{':
            ls.append(si)
            continue
        if len(ls) == 0: # have extra right braces
            print('extra right parentheses!')
            return False
        # 出栈比较是否匹配
        p = ls.pop() # the last item
        if (p == '(' and si==')') or (p == '[' and si==']') or ('p'=='{' and si=='}'):
            continue
        else:
            print('parentheses does not match!')
            return False           
        
    if len(ls) > 0: # have extra left braces
        print('extra left parentheses!')
        return False       
    return True

braces = "{abc}{de}(f)(g)]"
match_parentheses(braces)