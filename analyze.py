#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import List, AnyStr, Dict, Set

max_vocab_length = 8


def FMM(string: AnyStr, vocab: Dict):
    ans = []
    non_matches = []
    sentence_length = len(string)
    width = min(sentence_length, max_vocab_length)

    i = 0
    while i < sentence_length:
        for j in range(width, 0, -1):
            right = i + j
            right = right if right < sentence_length else sentence_length
            if right - i < j:
                continue
            sub_string = string[i:right]
            if sub_string in vocab:
                ans.append(sub_string)
                i += j
                break
        else:
            non_matches.append(len(ans))
            ans.append(string[i])
            i += 1
    ans = connect_non_matches(ans, non_matches)
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
            if i + 1 - left < j:
                continue
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


def count_single_word(segments):
    count = 0
    for word in segments:
        if len(word) == 1:
            count += 1
    return count


def BMM(string, vocab):
    """
    1.假设正反向分词结果词数不同，则取分词数量较少的那个。
    2.假设分词结果词数同样
         a.分词结果同样，就说明没有歧义，可返回随意一个。
         b.分词结果不同。返回当中单字较少的那个。
    """
    rmm_result = RMM(string, vocab)
    fmm_result = FMM(string, vocab)
    if len(rmm_result) != len(fmm_result):
        return min([rmm_result, fmm_result], key=len)
    else:
        if rmm_result == fmm_result:
            return rmm_result
        else:
            return min([rmm_result, fmm_result], key=count_single_word)


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
            result.extend(BMM(string, vocab))
    result_str = ' '.join(result)
    return result_str


# if __name__ == '__main__':
#     line = ['北京大学生前来应聘了吗', '，', '前来应聘']
#     vocab = ["北京大学", "生前", "来", "应聘", "大学生", "前来", "北京"]
#     vocab = dict(zip(vocab, range(len(vocab))))
#     matched = {'，'}
#     print(analyze(line, matched, vocab))
