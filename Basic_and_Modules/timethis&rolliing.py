# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:46:49 2021

@author: ys.leng
"""
import numpy as np
from numpy.lib.stride_tricks import as_strided as stride
import pandas as pd
import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

@timethis
def roll_np(df: pd.DataFrame, apply_func: callable, window: int, return_col_num: int, **kwargs):
    """
    rolling with multiple columns on 2 dim pd.Dataframe
    * the result can apply the function which can return pd.Series with multiple columns

    call apply function with numpy ndarray
    :param return_col_num: 返回的列数
    :param apply_func:
    :param df:
    :param window
    :param kwargs:
    :return:
    """

    # move index to values
    v = df.values

    dim0, dim1 = v.shape
    stride0, stride1 = v.strides
    result_values = np.full((dim0, return_col_num), np.nan)
    
    # min_window = 1
    for idx in range(window-1):
        min_window = idx + 1
        stride_values = stride(v[:min_window,:], (dim0 - (min_window - 1), min_window, dim1), (stride0, stride0, stride1))
        result_values[idx,] = apply_func(stride_values[:min_window,0,:], **kwargs)        
        
    stride_values = stride(v, (dim0 - (window - 1), window, dim1), (stride0, stride0, stride1))
    for idx, values in enumerate(stride_values, window - 1):
        # values : col 1 is index, other is value
        result_values[idx,] = apply_func(values, **kwargs)

    return result_values


def get_article_count_ratio(arr,article_counts_idx,sentiment_sign_idx):
    article_counts = arr[:,article_counts_idx]
    sentiment_sign = arr[:,sentiment_sign_idx]
    if ~np.isnan(sentiment_sign[-1]):
        return np.nansum(article_counts[sentiment_sign==sentiment_sign[-1]])/np.nansum(article_counts)
    else:
        return np.nan

