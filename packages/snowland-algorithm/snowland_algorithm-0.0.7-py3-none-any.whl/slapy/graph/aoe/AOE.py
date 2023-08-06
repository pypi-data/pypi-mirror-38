#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: AOE.py
# @time: 2018/10/5 3:17
# @Software: PyCharm

from scipy import sparse
import numpy as np

npa = np.array


def cpm(snode, enode, povertime):
    """
    AOE关键路径算法,输入所有工作的开尾节点(snode)、所有工作的头结点(enode)、对应工作
    所需时间povertime,返回最早开始时间、关键路径、自由时间、总工时
    :param snode: 起始节点
    :param enode: 结束节点
    :param povertime: 执行时间
    :return:
    """
    n = max(np.max(snode), np.max(enode)) + 1
    a = sparse.csr_matrix((povertime, (snode, enode)), shape=(n, n)).toarray()
    earliestST = np.zeros(n)
    latestET = np.ones(n) * np.inf
    for i in range(1, n):
        new1 = a[:i, i] + earliestST[:i]
        earliestST[i] = np.max(new1)
    latestET[-1] = earliestST[-1]
    for i in range(n - 2, -1, -1):
        new2 = latestET[i + 1:] - a[i, i + 1:]
        latestET[i] = np.min(new2)
    route = np.where(earliestST == latestET)[0]
    freetime = latestET - earliestST
    worktime = earliestST[-1]
    return earliestST, route, freetime, worktime


if __name__ == '__main__':
    # test data:
    snode = npa([0, 0, 0, 1, 1, 1, 2, 3, 4, 4, 4, 5, 6, 7, 7, 8, 8,
                 9, 10], dtype=np.int32)
    enode = npa([2, 1, 3, 2, 3, 4, 5, 7, 5, 7, 10, 6, 10, 8, 9, 9, 10,
                 11, 11], dtype=np.int32)
    povertime = npa([8, 5, 7, 0, 0, 8, 12, 17, 16, 5, 14, 8, 10, 23, 0, 0, 0, 12, 15])
    earliestST, route, freetime, worktime = cpm(snode, enode, povertime)
