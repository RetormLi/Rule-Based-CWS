#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import data_process
import preprocess
import analyze
# import eval

if __name__ == "__main__":
    vocab = dict()
    to_pred_file = 'data/test.txt'
    target_file = 'prediction.txt'

    # combine vocabulary
    vocab_paths = ['vocab/new_zh_vocab.json',
                   'vocab/new_caijing_vocab.json',
                   'vocab/new_food_vocab.json',
                   'vocab/new_chengyu_vocab.json',
                   'vocab/new_diming_vocab.json',
                   'vocab/new_pku_vocab.json',
                   'vocab/eng_name_vocab.json',
                   'vocab/place_vocab.json',
                   'vocab/chinese_vocab.json']
    for path in vocab_paths:
        vocab.update(data_process.get_vocab(path))
    data_process.store_vocab('vocab/big_vocab_dict.json', vocab)

    # get vocab from file
    # vocab = data_process.get_vocab('vocab/big_vocab_dict.json')

    # get result
    with open(to_pred_file, 'r', encoding='utf-8') as test_file:
        with open(target_file, 'w', encoding='utf-8') as result_file:
            for line in test_file:
                preprocess_sentence, matched = preprocess.preprocess(line)
                split_sentence = analyze.analyze(preprocess_sentence, matched, vocab)
                result_file.write(split_sentence + '\n')

    # eval.evaluate('data/dev.txt', vocab)
