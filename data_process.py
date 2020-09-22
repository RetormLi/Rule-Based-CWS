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

    def zh_token2vocab(self, save_path=None):
        max_length = 0
        vocab = dict()
        cop = re.compile("[^\u4e00-\u9fa5 ]+")
        with open(self.data_path, 'r', encoding='utf-8') as data_file:
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

    def get_special_vocab(self, save_path=None):
        """
        TODO
        :param save_path:
        :return:
        """
        special_vocab = dict()
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        with open(self.data_path, 'r', encoding='utf-8') as data_file:
            pass
        if save_path is not None:
            with open(save_path, 'w', encoding='utf-8') as json_file:
                json.dump(special_vocab, json_file, ensure_ascii=False)
        return special_vocab

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
