#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import data_process
import preprocess
import analyze

if __name__ == "__main__":
    vocab = dict()
    vocab_paths = ['vocab/zh_vocab_dict.json',
                   'vocab/caijing_vocab.json',
                   'vocab/food_vocab.json',
                   'vocab/chengyu_vocab.json',
                   'vocab/diming_vocab.json',
                   'vocab/pku_vocab.json',
                   'vocab/eng_name_vocab.json']
    for path in vocab_paths:
        vocab.update(data_process.get_vocab(path))

    escape_path = 'vocab/escape_vocab.json'
    escape_vocab = data_process.get_vocab(escape_path)
    for escape_word in escape_vocab:
        if escape_word in vocab:
            del vocab[escape_word]

    data_process.store_vocab('vocab/big_vocab_dict.json', vocab)

    with open('data/test.txt', 'r', encoding='utf-8') as test_file:
        with open('181220032.txt', 'w', encoding='utf-8') as result_file:
            for line in test_file:
                preprocess_sentence, matched = preprocess.preprocess(line)
                split_sentence = analyze.analyze(preprocess_sentence, matched, vocab)
                result_file.write(split_sentence + '\n')
