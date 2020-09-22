#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
from typing import Set, AnyStr, Pattern

# class Preprocesser:
spliter = re.compile(r"[，！。？《》,@“”（）【】、‘’：；↓#:;()]|…{2}|—{2}|/{2}|/", re.UNICODE)
zh_eng_num = re.compile(r"[\u4e00-\u9fa5a-zA-Z0-9]", re.UNICODE)
zh_detail = re.compile(r"([\u4E00-\u9FD5]+)", re.UNICODE)
skip_detail = re.compile(r"([.0-9]+|[a-zA-Z0-9]+)")
eng = re.compile(r"[a-zA-Z0-9]+")
num = re.compile("[.0-9]+")
count = re.compile(r"[0-9]+/[0-9]+|[第]*[.0-9]+[%]*[余多]*[十百千万亿]*[余多]*", re.UNICODE)
time = re.compile(r"[0-9]+[年月日][代]*", re.UNICODE)

# time -> count -> spliter
patterns = [time, count, spliter]


def add_space(matched):
    return ' ' + matched.group(0) + ' '


def split_step(sentence: AnyStr, pattern: Pattern, matches: Set):
    new_sentence = sentence.split()
    for i in range(len(new_sentence)):
        string = new_sentence[i]
        if string in matches:
            continue
        else:
            matches = matches.union(set(pattern.findall(string)))
            new_sentence[i] = pattern.sub(add_space, string)
    result = ' '.join(new_sentence)

    return result, matches


def preprocess(sentence: AnyStr):
    # split punctuation symbols
    matches: Set = set()
    for pattern in patterns:
        sentence, matches = split_step(sentence, pattern, matches)
        # print(sentence)
    return sentence.split(), matches


# if __name__ == '__main__':
#     line = "//你好，你是谁？我知道了。再见！现在是10月。我有0.3万元。大概1/3在银行，存了20年。100元/股。"
#     # line = "苏更透露，10月20日印尼新总统就职当天，印尼政府将公布经济新战略，其中包括长期投资额高达7千万亿印尼盾（约合3.6万亿人民币）的基础设施建设计划。"
#
#     print(preprocess(line))
