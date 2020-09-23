#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
from typing import Set, AnyStr, Pattern

# class Preprocesser:
zh_eng_num = re.compile(r"[\u4e00-\u9fa5a-zA-Z0-9]", re.UNICODE)
zh_detail = re.compile(r"([\u4E00-\u9FD5]+)", re.UNICODE)
skip_detail = re.compile(r"([.0-9]+|[a-zA-Z0-9]+)")
eng = re.compile(r"[a-zA-Z0-9]+")
num = re.compile("[.0-9]+")

emoji = re.compile(r"→_→", re.UNICODE)
web = re.compile(r"(([a-zA-Z0-9]([a-zA-Z0-9\-@_]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})", re.UNICODE)
name = re.compile(r"[.0-9]*[a-zA-Z_]+[.0-9]*[a-zA-Z_]*", re.UNICODE)
count = re.compile(r"([0-9]+/[0-9]+|[第]*([.0-9]*,)*[.0-9]+[%％]*[余多]*[十百千万亿]*[余多]*)",
                   re.UNICODE)
time = re.compile(r"[.0-9]+[月日时][早晚]?|[0-9]{4}年|[0-9]+年代|[一二三四五六七八九]+十年代|[0-9]+[分点](?!钟)|(?<![0-9])[0-9]{2}后",
                  re.UNICODE)
spliter = re.compile(r"[，！。？《》,@“”（）【】、‘’：；↓→↑←#:;()]|…{1,2}|—{1,2}|/{1,2}|~+|\.+", re.UNICODE)

# emoji -> web -> name -> time -> count -> spliter
patterns = [emoji, web, name, time, count, spliter]


def add_space(matched):
    return ' ' + matched.group(0) + ' '


def split_step(sentence: AnyStr, pattern: Pattern, matches: Set):
    new_sentence = sentence.split()
    for i in range(len(new_sentence)):
        string = new_sentence[i]
        if string in matches:
            continue
        else:
            match = pattern.findall(string)
            if match:
                if type(match[0]) == tuple:
                    matches = matches.union({match_group[0] for match_group in match})
                else:
                    matches = matches.union(set(match))
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


if __name__ == '__main__':
    # line = "//你好，你是谁？—我知道了。再见！现在是10月。我有0.3万元。大概1/3在银行，存了20年。10,000元/股。2020年，10分钟之前，12点13分的时候，20年后，90年代，二十年代。100多年来。20日早。"
    # line = "苏更透露，10月20日印尼新总统就职当天，印尼政府将公布经济新战略，其中包括长期投资额高达7千万亿印尼盾（约合3.6万亿人民币）的基础设施建设计划。"
    line = "21日上午，一艘长77.8米的烟花集装箱货轮正在长沙船舶厂进行最后一道工艺建造。"
    # line = "因为它富含丰富的维生素C，可以帮助调动人体免疫系统，预防感冒。财经网站iposcoop显示，智联招聘将于6月13日在纽交所正式挂牌交易。"
    print(preprocess(line)[0])
