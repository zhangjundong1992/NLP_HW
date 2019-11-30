import re
import numpy as np
from scipy.sparse import dok_matrix
import operator


# 读取中文字典，保存为一个list，同时返回字典中的最长单词的长度
def get_lst():
    ch_lst = []
    max_len = 0
    with open("中文字典.txt", 'r') as f:
        for line in f:
            str = line.split()[1]
            ch_lst.append(str)
            max_len = max(max_len, len(str))

    return ch_lst, max_len


# 读取中文字典，保存为一个字典，键为‘中文单词’，值为‘总的出现次数’
def get_dict():
    ch_dict = {}
    with open("中文字典.txt", 'r') as f:
        for line in f:
            str = line.split()[1]
            num = line.split()[2]
            ch_dict.update(str=num)

    return ch_dict


# 得到bi_gram转移矩阵
# todo,转移矩阵的获得需要很长的时间，想办法改进一下
# todo,字典跟句子集不是完全匹配的，比如数字的处理
# todo,没有进行开头和结尾的统计
# todo，最佳方案是直接计算概率，但是计算时间需要改进
def get_matrix():
    # 初始化
    ch_lst, _ = get_lst()  # 中文单词的列表

    matrix = dok_matrix((len(ch_lst), len(ch_lst)), dtype=np.int)  # 初始化转移矩阵（稀疏矩阵）

    # 计算前后继词频
    with open('1998-01-105-带音.txt') as f:
        counter = 0
        for line in f:
            # 标记一下当前处理的行号
            counter += 1

            if counter % 100 == 0:
                print(counter)

            if counter > 10:
                break

            # 遍历文本，删除字典中不存在的字符
            line = line.replace(' ', '')
            line_lst = re.split('/[a-z]+', line)
            line_temp = line_lst.copy()
            for s in line_temp:
                if s not in ch_lst:
                    line_lst.remove(s)

            # 根据前后继关系，构建转移矩阵（频率）
            for i in range(len(line_lst) - 1):
                m = ch_lst.index(line_lst[i])  # 行号
                n = ch_lst.index(line_lst[i + 1])  # 列号
                matrix[m, n] += 1

    # todo，遍历矩阵，计算概率这边也比较慢
    # # 计算概率
    # matrix += 1  # 加1平滑
    # for k in matrix.keys():
    #     matrix[k] = (matrix[k] + 1) / (int(ch_dict.get(ch_lst[k[0]])) + len(ch_lst))

    return matrix


# 正向最大匹配
def fmm(s):
    ch_lst, max_len = get_lst()  # 获取中文字典，以及最大单词长度

    pos = 0  # 标记当前切分到的位置
    length = max_len  # 标记当前要匹配的子串的长度
    while pos < len(s):

        if pos + length > len(s):
            length = len(s) - pos

        sub_str = s[pos:pos + length]  # 取子串进行匹配
        if sub_str in ch_lst:  # 匹配成功
            # 插入'/'
            str_lst = list(s)
            str_lst.insert(pos + length, '/')
            s = ''.join(str_lst)

            # 更新切分位置和匹配子串长度
            pos += length + 1
            length = max_len
        else:  # 匹配失败，将length减1
            length -= 1

    return s[:len(s) - 1]


# 逆向最大匹配
def bmm(s):
    ch_lst, max_len = get_lst()  # 获取中文字典，以及最大单词长度

    pos = -1  # 标记当前切分到的位置
    length = max_len  # 标记当前要匹配的子串的长度
    while pos > -(len(s) + 1):

        if pos - length < -(len(s) + 1):
            length = pos + len(s) + 1

        sub_str = s[pos:pos - length:-1][::-1]  # 取子串进行匹配
        if sub_str in ch_lst:  # 匹配成功
            # 插入'/'
            str_lst = list(s)
            str_lst.insert(pos - length + 1, '/')
            s = ''.join(str_lst)

            # 更新切分位置和匹配子串长度
            pos -= length + 1
            length = max_len
        else:  # 匹配失败，将length减1
            length -= 1

    return s[1:]


# 利用bi_gram选择两种分词方法的一种，s1,s2以列表的形式给出,m为字典模
def bi_gram(s1, s2):
    # 初始化
    ch_lst, _ = get_lst()  # 中文单词的列表
    ch_dict = get_dict()  # 中文单词和词频的哈希表
    matrix = get_matrix()  # 词频矩阵，todo，实际上应该用概率矩阵

    # 分别计算概率
    p1 = p2 = 1
    for i in range(len(s1) - 1):
        pre_index = ch_lst.index(s1[i])
        suc_index = ch_lst.index(s1[i + 1])
        if (pre_index, suc_index) in matrix:
            p = (matrix.get((pre_index, suc_index)) + 1) / (int(ch_dict.get(s1[i])) + len(ch_lst))  # 加1平滑
        else:
            p = 1 / len(ch_lst)
        p1 *= p

    for i in range(len(s2) - 1):
        pre_index = ch_lst.index(s2[i])
        suc_index = ch_lst.index(s2[i + 1])
        p = 1
        if (pre_index, suc_index) in matrix:
            p = (matrix.get((pre_index, suc_index)) + 1) / (int(ch_dict.get(s2[i])) + len(ch_lst))  # 加1平滑
        else:
            p = 1 / len(ch_lst)
        p2 *= p

    # 逆向最大匹配优先策略
    return s1 if p1 > p2 else s2


# 对单句中文进行切分
def segment(s):
    s1 = fmm(s).split('/')
    s2 = bmm(s).split('/')
    if operator.eq(s1, s2):
        return s1
    else:
        return bi_gram(s1, s2)


s = '金融智能与金融工程实验室是最好的实验室'
res = segment(s)
print('res of fmm: ', fmm(s))
print('res of bmm: ', bmm(s))
print('res of bi_gram: ', res)

print()

s = '乒乓球拍卖完了'
res = segment(s)
print('res of fmm: ', fmm(s))
print('res of bmm: ', bmm(s))
print('res of bi_gram: ', res)
