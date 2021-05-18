# -*- coding: utf-8 -*-
# Reference: https://en.wikipedia.org/wiki/Hurst_exponent
# python 3.6.2 AMD64
# 2018/4/19
# Calculate Hurst exponent based on Rescaled range (R/S) analysis
# How to use (example):
# import Hurst 
# ts = list(range(50))
# hurst = Hurst.hurst(ts)
# Tip: ts has to be object list(n_samples,) or np.array(n_samples,)

__Author__ = "Ryan Wang"

import numpy as np
import pandas as pd


def hurst(ts):
    ts = list(ts)  # 将time series时间序列转化为一个列表
    N = len(ts)  # N为列表长度
    if N < 20:
        raise ValueError("Time series is too short! input series ought to have at least 20 samples!")

    max_k = int(np.floor(N / 2))  # k返回值不大于N/2的最大整数
    R_S_dict = []  # 创建一个空词典
    # print('rs dict:', R_S_dict)
    for k in range(10, max_k + 1):
        R, S = 0, 0
        # split ts into subsets将ts分成子集
        subset_list = [ts[i:i + k] for i in range(0, N, k)]
        print('subset_list:',subset_list)
        print('k:',k)
        if np.mod(N, k) > 0:
            subset_list.pop()
            # tail = subset_list.pop()
            # subset_list[-1].extend(tail)
        # calc mean of every subset计算每个子集的均值
        mean_list = [np.mean(x) for x in subset_list]
        for i in range(len(subset_list)):
            cumsum_list = pd.Series(subset_list[i] - mean_list[i]).cumsum()
            R += max(cumsum_list) - min(cumsum_list)
            S += np.std(subset_list[i])
        R_S_dict.append({"R": R / len(subset_list), "S": S / len(subset_list), "n": k})

    log_R_S = []
    log_n = []
    #print(R_S_dict)
    for i in range(len(R_S_dict)):
        R_S = (R_S_dict[i]["R"] + np.spacing(1)) / (R_S_dict[i]["S"] + np.spacing(1))
        log_R_S.append(np.log(R_S))
        log_n.append(np.log(R_S_dict[i]["n"]))

    Hurst_exponent = np.polyfit(log_n, log_R_S, 1)[0]
    return Hurst_exponent


if __name__ == '__main__':
    arr = np.arange(40)
    #print('arr:',arr)
    hurst(arr)