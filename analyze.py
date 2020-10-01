#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is to define the method to analyze a sentence after preprocess, and segment it.
# In this case, method BMM is applyed.

from typing import List, AnyStr, Dict, Set

max_vocab_length = 8


def FMM(string: AnyStr, vocab: Dict):
    """Forward Maximum Maching."""

    ans = []
    unmatched = []
    sentence_length = len(string)
    width = min(sentence_length, max_vocab_length)

    i = 0
    while i < sentence_length:
        for j in range(width, 0, -1):
            right = i + j
            # In canse of index overflow
            right = right if right < sentence_length else sentence_length
            if right - i < j:
                continue
            sub_string = string[i:right]
            if sub_string in vocab:
                ans.append(sub_string)
                i += j
                break
        else:
            # Recording non-match characters' index for next step.
            unmatched.append(len(ans))
            ans.append(string[i])
            i += 1
    ans = connect_non_matches(ans, unmatched)
    return ans


def RMM(string: AnyStr, vocab: Dict):
    """Reversed Maximum Maching."""

    ans = []
    unmatched = []
    sentence_length = len(string)
    width = min(sentence_length, max_vocab_length)

    i = sentence_length - 1
    while i >= 0:
        for j in range(width, 0, -1):
            left = i - j + 1
            # In canse of index underflow
            left = left if left >= 0 else 0
            if i + 1 - left < j:
                continue
            sub_string = string[left:i + 1]
            if sub_string in vocab:
                ans.append(sub_string)
                i -= j
                break
        else:
            # Recording non-match characters' index for next step.
            unmatched.append(len(ans))
            ans.append(string[i])
            i -= 1
    # Reverse the matched list and unmatched list back
    ans = ans[::-1]
    unmatched = unmatched[::-1]
    unmatched = [len(ans) - match - 1 for match in unmatched]
    ans = connect_non_matches(ans, unmatched)
    return ans


def count_single_word(segments):
    """Count amount of single word in a list."""
    count = 0
    for word in segments:
        if len(word) == 1:
            count += 1
    return count


def BMM(string, vocab):
    """
    1. Assume that we got different words count between RMM and FMM results, then return the segments with less words.
    2. Assume that we got same words count
         a. Same result. Return it.
         b. Different result. Return segments with less single words.
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


def connect_non_matches(strings, unmatched):
    """Some continuous unmatched character may combine a new word. Connect them to be a new segment."""
    ans = []
    connect_str = ''
    length = len(strings)

    # unmatched is a list of unmatched characters index. Traverse the original line.
    for i in range(length):
        if i in unmatched:
            if i < length - 1 and i + 1 in unmatched:
                connect_str += strings[i]
            else:
                connect_str += strings[i]
                ans.append(connect_str)
                connect_str = ''
        else:
            ans.append(strings[i])
    return ans


def analyze(sentence: List, matched: Set, vocab: Dict):
    """
    Analyze step.
    :param sentence: List, sentence after preprocess
    :param matched: Set, matched symbols from preprocess
    :param vocab: Dict, vocabulary
    :return: String, sentence string splited by space
    """

    result = []
    method = BMM

    for string in sentence:
        if string in matched:
            result.append(string)
        else:
            result.extend(method(string, vocab))
    result_str = ' '.join(result)
    return result_str
