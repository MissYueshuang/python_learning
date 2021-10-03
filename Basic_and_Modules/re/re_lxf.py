# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 16:19:23 2020

@author: rmileng
"""
import re

# example 1
# 先编译好正则
re_name_of_email  = re.compile(r'^<?([\w]+\s*[\w]*)>?\s*[\w]*\@[\w]+\.org$')
# 正则解释：     字母一个以上 .一个或没有 字母一个以上 @ 字母不限 .com
def name_of_email(addr):
    if re_name_of_email.match(addr):
        return re_name_of_email.match(addr).group(1)

# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')

# example 2
# 先编译好正则
re_email = re.compile(r'^[\w]+\.?[\w]+@[\w]+\.com$')
# 正则解释：     字母一个以上 .一个或没有 字母一个以上 @ 字母不限 .com
def is_valid_email(addr):
    if re_email.match(addr):
        return True

# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')
