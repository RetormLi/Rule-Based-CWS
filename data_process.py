#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import re
from typing import AnyStr, List


class Data:
    def __init__(self, path):
        self.data_path = path

    def token2vocab(self, save_path=None):
        vocab = dict()
        cop = re.compile("[^\u4e00-\u9fa5a-zA-Z0-9 ]+")
        with open(self.data_path, 'r', encoding='utf-8') as data_file:
            for line in data_file:
                new_line = cop.sub('', line)
                for word in new_line.split():
                    vocab[word] = vocab.get(word, 0) + 1
        if save_path is not None:
            with open(save_path, 'w', encoding='utf-8') as json_file:
                json.dump(vocab, json_file, ensure_ascii=False)
        return vocab

    def zh_token2vocab(self, save_path=None, encoding='utf-8'):
        max_length = 0
        vocab = dict()
        cop = re.compile("[^\u4e00-\u9fa5 ]+")
        with open(self.data_path, 'r', encoding=encoding) as data_file:
            for line in data_file:
                new_line = cop.sub('', line)
                for word in new_line.split():
                    if len(word) > max_length:
                        max_length = len(word)
                    vocab[word] = vocab.get(word, 0) + 1
        if save_path is not None:
            with open(save_path, 'w', encoding='utf-8') as json_file:
                json.dump(vocab, json_file, ensure_ascii=False)
        print(max_length)
        return vocab


def get_vocab(path):
    with open(path, "r", encoding='utf-8') as json_file:
        return json.load(json_file)


def store_vocab(path, vocab):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(vocab, json_file, ensure_ascii=False)


def THUOCL_get_word(line):
    return [line[:line.find('\t')]]


def chinese_get_word(line):
    pair = line.split()
    if pair[1] in ['nt', 'ns']:
        return []
    else:
        return [pair[0]]


def naive_get_word(line):
    return [line]


def place_get_word(line):
    ans = []
    words: List[AnyStr] = line.split()
    for word in words:
        if not word.isnumeric():
            ans.append(word)
            if len(word) > 2:
                ans.append(word[:-1])
    return ans


def generate_vocab(origin_path, save_path, func=naive_get_word, max_len=3):
    vocab = dict()
    with open(origin_path, 'r', encoding='utf-8') as origin_file:
        for line in origin_file:
            words = func(line)
            for word in words:
                if len(word) <= max_len:
                    vocab[word] = vocab.get(word, 0) + 1
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(vocab, save_file, ensure_ascii=False)


def disambiguate(origin_path, new_vocab, save_path, max_len=5):
    origin_lines = ''
    vocab = dict()
    with open(origin_path, 'r', encoding='utf-8') as origin_file:
        for line in origin_file:
            origin_lines += ' ' + line
    count = 0
    with open(new_vocab, 'r', encoding='utf-8') as new_file:
        with open('data/amb.txt', 'w', encoding='utf-8') as result_file:
            for line in new_file:
                count += 1
                if count % 1000 == 0:
                    print(count)
                pair = line.split()
                word = pair[0]
                if pair[1] in ['nt', 'ns', '@'] or len(word) > max_len:
                    continue
                else:
                    for i in range(1, len(word)):
                        new_word = ' ' + word[:i] + ' ' + word[i:] + ' '
                        if new_word in origin_lines:
                            print(new_word)
                            result_file.write(new_word + '\n')
                            break
                    else:
                        vocab[word] = vocab.get(word, 0) + 1
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(vocab, save_file, ensure_ascii=False)


escape = ['一次', '这个', '那个', '这次', '那次', '此次', '最低',
          '最高', '最多', '最少', '最佳', '最好', '最新', '就是',
          '都是', '一天', '同一', '一个', '各个', '每个', '哪个',
          '一片', '一对', '一家', '一步', '一本']

if __name__ == '__main__':
    # generate_vocab('data/THUOCL_diming.txt', 'vocab/diming_vocab.json', THUOCL_get_word)
    # generate_vocab('data/THUOCL_chengyu.txt', 'vocab/chengyu_vocab.json', THUOCL_get_word)
    # generate_vocab('data/THUOCL_caijing.txt', 'vocab/caijing_vocab.json', THUOCL_get_word)
    # generate_vocab('data/THUOCL_food.txt', 'vocab/food_vocab.json', THUOCL_get_word)
    # generate_vocab('data/places.txt', 'vocab/place_vocab.json', place_get_word, max_len=6)
    # pku = Data('data/Chinese_Names_Corpus（120W）.txt')
    # pku.zh_token2vocab('vocab/ch_name_vocab.json')
    store_vocab('vocab/escape_vocab.json', dict(zip(escape, [1 for x in escape])))
    # disambiguate('data/train.txt', 'data/30wChinese.txt', 'vocab/chinese_vocab.json')
