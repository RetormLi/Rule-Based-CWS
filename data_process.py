#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import re


class Data:
    def __init__(self, path):
        self.data_path = path

    def token2vocab(self, save_path=None):
        vocab = dict()
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        with open(self.data_path, 'r', encoding='utf-8') as data_file:
            for line in data_file:
                for word in line.split():
                    new_word = cop.sub('', word)
                    vocab[new_word] = vocab.get(new_word, 0) + 1
            del vocab['']
        if save_path is not None:
            with open(save_path, 'w', encoding='utf-8') as json_file:
                json.dump(vocab, json_file, ensure_ascii=False)
        return vocab


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
