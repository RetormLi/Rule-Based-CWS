#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import re
from typing import AnyStr, List


def zh_token2vocab(data_path, save_path=None, encoding='utf-8'):
    """Generate chinese word vocab."""
    max_length = 0
    vocab = dict()
    cop = re.compile("[^\u4e00-\u9fa5 ]+")
    with open(data_path, 'r', encoding=encoding) as data_file:
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
    """Load vocab from json file."""
    with open(path, "r", encoding='utf-8') as json_file:
        return json.load(json_file)


def store_vocab(path, vocab):
    """Store a Dict vocab to a json file."""
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(vocab, json_file, ensure_ascii=False)


# methods of getting word from different datasets.
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
    """Generate vocab from datasets."""
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
    """
    Disambiguate the segmentation interests of different datasets.

    :param origin_path: The reference dataset.
    :param new_vocab: The additional dataset.
    :param save_path: Vocabulary saving path.
    :param max_len: Max word length to save into vocab.
    """
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
                        if origin_lines.count(new_word) > origin_lines.count(' ' + word + ' '):
                            print(new_word)
                            result_file.write(new_word + '\n')
                            break
                    else:
                        vocab[word] = vocab.get(word, 0) + 1
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(vocab, save_file, ensure_ascii=False)


def vocab_disambiguate(origin_path, new_vocab, save_path, max_len=5):
    """
    Disambiguate the segmentation interests of different datasets.

    :param origin_path: The reference dataset.
    :param new_vocab: The additional vocab.
    :param save_path: Vocabulary saving path.
    :param max_len: Max word length to save into vocab.
    """

    origin_lines = ''
    vocab = dict()
    with open(origin_path, 'r', encoding='utf-8') as origin_file:
        for line in origin_file:
            origin_lines += ' ' + line
    count = 0
    with open(new_vocab, 'r', encoding='utf-8') as new_file:
        old_vocab = json.load(new_file)
        with open('data/amb_pku.txt', 'w', encoding='utf-8') as result_file:
            for word in old_vocab:
                count += 1
                if count % 1000 == 0:
                    print(count)
                if len(word) > max_len:
                    continue
                else:
                    for i in range(1, len(word)):
                        new_word = ' ' + word[:i] + ' ' + word[i:] + ' '
                        if origin_lines.count(new_word) > origin_lines.count(' ' + word + ' '):
                            print(new_word)
                            result_file.write(new_word + '\n')
                            break
                    else:
                        vocab[word] = vocab.get(word, 0) + 1
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(vocab, save_file, ensure_ascii=False)


def train_disambiguate(train_path, vocab_path, save_path):
    """
    Disambiguate the segmentation interests of within training datasets.

    :param train_path: Training file
    :param vocab_path: Vocab from training set
    :param save_path: New vocab saving path
    """

    origin_lines = ''
    vocab = dict()
    with open(train_path, 'r', encoding='utf-8') as origin_file:
        for line in origin_file:
            origin_lines += ' ' + line
    count = 0
    with open(vocab_path, 'r', encoding='utf-8') as new_file:
        old_vocab = json.load(new_file)
        for word in old_vocab:
            count += 1
            if count % 1000 == 0:
                print(count)
            else:
                for i in range(1, len(word)):
                    new_word = ' ' + word[:i] + ' ' + word[i:] + ' '
                    if origin_lines.count(new_word) > origin_lines.count(' ' + word + ' '):
                        print(new_word)
                        break
                else:
                    vocab[word] = vocab.get(word, 0) + 1
    with open(save_path, 'w', encoding='utf-8') as save_file:
        json.dump(vocab, save_file, ensure_ascii=False)


if __name__ == '__main__':
    # 'vocab/new_zh_vocab.json',
    # 'vocab/new_caijing_vocab.json',
    # 'vocab/new_food_vocab.json',
    # 'vocab/new_chengyu_vocab.json',
    # 'vocab/new_diming_vocab.json',
    # 'vocab/new_pku_vocab.json',
    # 'vocab/eng_name_vocab.json',
    # 'vocab/place_vocab.json',
    # 'vocab/chinese_vocab.json'

    zh_token2vocab('data/all.txt', 'vocab/zh_vocab_dict.json')
    zh_token2vocab('data/pku_training.txt', 'vocab/pku_vocab.json', encoding='gbk')
    generate_vocab('data/English_Cn_Name_Corpus（48W）.txt', 'vocab/eng_name_vocab.json')
    generate_vocab('data/THUOCL_diming.txt', 'vocab/diming_vocab.json', THUOCL_get_word)
    generate_vocab('data/THUOCL_chengyu.txt', 'vocab/chengyu_vocab.json', THUOCL_get_word)
    generate_vocab('data/THUOCL_caijing.txt', 'vocab/caijing_vocab.json', THUOCL_get_word)
    generate_vocab('data/THUOCL_food.txt', 'vocab/food_vocab.json', THUOCL_get_word)
    generate_vocab('data/places.txt', 'vocab/place_vocab.json', place_get_word, max_len=6)

    train_disambiguate('data/all.txt', 'vocab/zh_vocab_dict.json', 'vocab/new_zh_vocab.json')
    disambiguate('data/all.txt', 'data/30wChinese.txt', 'vocab/chinese_vocab.json')
    vocab_disambiguate('data/all.txt', 'vocab/pku_vocab.json', 'vocab/new_pku_vocab.json')
    vocab_disambiguate('data/all.txt', 'vocab/diming_vocab.json', 'vocab/new_diming_vocab.json')
    vocab_disambiguate('data/all.txt', 'vocab/chengyu_vocab.json', 'vocab/new_chengyu_vocab.json')
    vocab_disambiguate('data/all.txt', 'vocab/caijing_vocab.json', 'vocab/new_caijing_vocab.json')
    vocab_disambiguate('data/all.txt', 'vocab/food_vocab.json', 'vocab/new_food_vocab.json')
