#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import List, AnyStr, Dict, Set

max_vocab_length = 4


def FMM(string: AnyStr, vocab: Dict):
    ans = []
    sentence_length = len(string)
    width = min(sentence_length, max_vocab_length)

    i = 0
    while i < sentence_length:
        for j in range(width, 0, -1):
            right = i + j
            right = right if right < sentence_length else sentence_length - 1
            sub_string = string[i:right]
            if sub_string in vocab:
                ans.append(sub_string)
                i += j
                break
        else:
            ans.append(string[i])
            i += 1
    return ans


def RMM(string: AnyStr, vocab: Dict):
    ans = []
    non_matches = []
    sentence_length = len(string)
    width = min(sentence_length, max_vocab_length)

    i = sentence_length - 1
    while i >= 0:
        for j in range(width, 0, -1):
            left = i - j + 1
            left = left if left >= 0 else 0
            sub_string = string[left:i + 1]
            if sub_string in vocab:
                ans.append(sub_string)
                i -= j
                break
        else:
            non_matches.append(len(ans))
            ans.append(string[i])
            i -= 1
    ans = ans[::-1]
    non_matches = non_matches[::-1]
    non_matches = [len(ans) - match - 1 for match in non_matches]
    ans = connect_non_matches(ans, non_matches)
    return ans


def connect_non_matches(strings, non_matches):
    ans = []
    connect_str = ''
    length = len(strings)
    for i in range(length):
        if i in non_matches:
            if i < length - 1 and i + 1 in non_matches:
                connect_str += strings[i]
            else:
                connect_str += strings[i]
                ans.append(connect_str)
                connect_str = ''
        else:
            ans.append(strings[i])
    return ans


def analyze(sentence: List, matched: Set, vocab: Dict):
    result = []
    for string in sentence:
        if string in matched:
            result.append(string)
        else:
            result.extend(RMM(string, vocab))
    result_str = ' '.join(result)
    return result_str


# if __name__ == '__main__':
#     line = ['北京大学生前来应聘alibaba', '，', '前来应聘']
#     vocab = ["北京大学", "生前", "来", "应聘", "大学生", "前来", "北京"]
#     vocab = dict(zip(vocab, range(len(vocab))))
#     matched = {'，'}
#     print(analyze(line, matched, vocab))
