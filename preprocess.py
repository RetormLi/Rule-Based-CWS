#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This File is to preprocess sentences, spliting them by some patterns and punctuations.

import re
from typing import Set, AnyStr, Pattern


# Regex patterns
web = re.compile(r"(([a-zA-Z0-9]([a-zA-Z0-9\-@_]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})", re.UNICODE)
name = re.compile(r"[.0-9]*[a-zA-Z_āáǎàēéěèūúǔùōóǒòīíǐìǖǘǚǜü]+[.0-9]*[a-zA-Z_]*", re.UNICODE)
count = re.compile(r"([0-9]+/[0-9]+|[第]*([.0-9]+,)*[.0-9]+[%％]*[余多]*[十百千万亿]*[余多]*)",
                   re.UNICODE)
time = re.compile(r"[.0-9]+[月日时][早晚]?|[0-9]{4}年|[0-9]+年代|[一二三四五六七八九]+十年代|[0-9]+[分点](?!钟)|(?<![0-9])[0-9]{2}后",
                  re.UNICODE)
spliter = re.compile(r"[，！。？《》,@“”（）【】、‘’：；↓→↑←#:;()]|…{1,2}|—{1,2}|/{1,2}|~+|\.+|·+", re.UNICODE)

# Defines the order of regex processing
# web -> name -> time -> count -> spliter
patterns = [web, name, time, count, spliter]


def add_space(matched):
    """Add a space near the matched substring, ready for next step of split."""
    return ' ' + matched.group(0) + ' '


def split_step(sentence: AnyStr, pattern: Pattern, matches: Set):
    """The step of sentence spliting. Using regex to split a sentence before maximum matching segmentation,
    and return the splited sentence by adding space."""
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
    """Split punctuation symbols. Return the splited sentence by List, and set of matched symbols"""

    # matches is the set of matched symbol or substrings. Save it for Maximum Matching.
    matches: Set = set()
    for pattern in patterns:
        sentence, matches = split_step(sentence, pattern, matches)
        # print(sentence)
    return sentence.split(), matches
