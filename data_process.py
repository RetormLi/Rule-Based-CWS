#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import re


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
            # for line in data_file:
            #     for word in line.split():
            #         vocab[word] = vocab.get(word, 0) + 1
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

    def get_line(self, split=True):
        with open(self.data_path, 'r', encoding='utf-8') as data_file:
            for line in data_file:
                if split:
                    yield line.split()
                else:
                    yield line


class Vocab:
    def __init__(self, path):
        self.path = path
        with open(path, "r", encoding='utf-8') as json_file:
            self.vocab_dict = json.load(json_file)

    def __getitem__(self, item):
        if item in self.vocab_dict:
            return self.vocab_dict[item]
        else:
            raise KeyError

    def __contains__(self, item):
        return item in self.vocab_dict

    def get(self, key, value):
        return self.vocab_dict.get(key, value)

    def add(self, new_dict):
        pass


def get_vocab(path):
    with open(path, "r", encoding='utf-8') as json_file:
        return json.load(json_file)


def store_vocab(path, vocab):
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(vocab, json_file, ensure_ascii=False)


def generate_vocab(origin_path, save_path):
    vocab = dict()
    with open(origin_path, 'r', encoding='utf-8') as origin_file:
        for line in origin_file:
            # word = line[:line.find('\t')]
            word = line
            vocab[word] = vocab.get(word, 0) + 1
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(vocab, save_file, ensure_ascii=False)


escape = ['一次', '这个', '那个', '这次', '那次', '此次', '最低',
          '最高', '最多', '最少', '最佳', '最好', '最新', '就是',
          '都是', '一天', '同一', '一个', '各个', '每个', '哪个']

if __name__ == '__main__':
    # generate_vocab('data/THUOCL_diming.txt', 'vocab/diming_vocab.json')
    # generate_vocab('data/THUOCL_chengyu.txt', 'vocab/chengyu_vocab.json')
    # generate_vocab('data/THUOCL_caijing.txt', 'vocab/caijing_vocab.json')
    # generate_vocab('data/THUOCL_food.txt', 'vocab/food_vocab.json')
    # pku = Data('data/Chinese_Names_Corpus（120W）.txt')
    # pku.zh_token2vocab('vocab/ch_name_vocab.json')
    store_vocab('vocab/escape_vocab.json', dict(zip(escape, [1 for x in escape])))
