#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import data_process
import preprocess
import analyze

if __name__ == "__main__":
    # train = data_process.Data('data/train.txt')
    # vocab = train.zh_token2vocab('zh_vocab_dict.json')
    vocab = data_process.get_vocab('zh_vocab_dict.json')
    with open('data/test.txt', 'r', encoding='utf-8') as test_file:
        with open('181220032.txt', 'w', encoding='utf-8') as result_file:
            for line in test_file:
                preprocess_sentence, matched = preprocess.preprocess(line)
                split_sentence = analyze.analyze(preprocess_sentence, matched, vocab)
                result_file.write(split_sentence + '\n')
