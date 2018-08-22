#!/usr/bin/python3.6
"""
    author  :   Johnsonhe He
    date    :   2018/08/21
"""

import copy
import itertools
import operator


def _has_infrequence_subset(c, L):
    """[判断k项候选集c的k-1项子集看是否存在非频繁子集]
    
    Arguments:
        c {[tuple]} -- [k项侯选集]
        L {[list[tuple]]} -- [频繁k-1项集]
    """
    for i in range(0, len(c)):
        c_subset = set(c[:i] + c[i + 1:])
        flag = True
        for l_child in L:
            if operator.eq(c_subset, set(l_child)):
                flag = False
                break
        if flag:
            return True
    return False


def _judge_can_join(l1, l2):
    """[判断2个k-1子项是否是可连接的并且能形成k子项, 如果前(k-1)个项都相同，
        则可连接，条件l1[-1] < l2[-1]是简单地确保不产生重复项]
    
    Arguments:
        item1 {[tuple]} -- [description]
        item2 {[tuple]} -- [description]
    """
    item_len = len(l1)
    if l1[-1] >= l2[-1]:
        return False
    for i in range(0, item_len - 1):
        if l1[i] != l2[i]:
            return False
    return True


def apiori_gen(L):
    """[连接L(k-1)频繁项集产生候选k项候选集]
    
    Arguments:
        L {[list[tuple]]} -- [L(k-1)频繁项集]
    Returns:
        [list] -- [k项候选集]
    """
    C_k = []
    for l1 in L:
        for l2 in L:
            if _judge_can_join(l1, l2):
                c = (l1 + (l2[-1], ))
                if not _has_infrequence_subset(c, L):
                    C_k.append(c)
    return C_k


def _find_frequent_itemset(dataset, C, k, mix_up):
    """[遍历事务集中每个项的k项子集，找出候选集中的，累加次数后，
        筛选出满足最小支持阈值的侯选集]]
    
    Arguments:
        dataset {[list[tuple]]} -- [事务集]
        C {[list[tuple]]} -- [候选集]
        k {[int]} -- [项数]
        mix_up {int]} -- [最小支持阈值]
    
    Returns:
        [list[tuple]] -- [频繁k项集]
    """
    count_k_item = [0 for _ in range(len(C))]
    for each in dataset:
        k_subset_dataset = list(itertools.combinations(each, k))
        for idx, item in enumerate(C):
            for k_subset in k_subset_dataset:
                if operator.eq(item, k_subset) == True:
                    count_k_item[idx] += 1
                    break
    L_k = [C[i] for i in range(len(C)) if count_k_item[i] >= mix_up]
    return L_k


def find_itemset_by_layer_iteration_base_on_candidate(dataset, mix_up):
    """[使用逐层迭代方法基于候选产生找出频繁项集， 算法假定事务DATA或项中的项按字典排序]
    
    Arguments:
        dataset {[list[tuple]]} -- [事务集]
        mix_up {[int]} -- [最小支持阈值]
    
    Returns:
        [list[tuple]]] -- [k项频繁集]]
    """
    itemset = []
    K = (max([len(_) for _ in dataset]))
    for k in range(1, K + 1):
        print(f'|一 计算{k}项频繁集合')
        if k == 1:
            C_k = [(1, ), (2, ), (3, ), (4, ), (5, )]
        else:
            C_k = apiori_gen(itemset[k - 2])
        L_k = _find_frequent_itemset(dataset, C_k, k, mix_up)
        if L_k == []:
            return itemset
        itemset.append(L_k)
    return itemset


def _format_print(data):
    for idx, item in enumerate(data):
        print(f'=========={idx+1}项频繁集=============')
        print(item)
        print('\n')


if __name__ == '__main__':
    DATA = [(1, 2, 5), (2, 4), (2, 3), (1, 2, 4), (1, 3), (2, 3), (1, 3),
            (1, 2, 3, 5), (1, 2, 3)]

    result = find_itemset_by_layer_iteration_base_on_candidate(DATA, 2)
    print('|一一 所有的频繁集合已经找出.')
    _format_print(result)
