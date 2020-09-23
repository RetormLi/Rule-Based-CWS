#!/usr/bin/env python
# -*- encoding: utf-8 -*-


def match_count(target, pred):
    """
    Calculate the match count of two list of strings.

    :return: count of match strings
    """
    target_len = len(target)
    pred_len = len(pred)
    count = 0
    target_i = 0
    pred_i = 0
    target_end = 0
    pred_end = 0
    next_target = True
    next_pred = True
    while target_i < target_len and pred_i < pred_len:
        target_word = target[target_i]
        pred_word = pred[pred_i]

        # choose from target and prediction list to iterate according to the former iter
        if next_target:
            target_end += len(target_word)
            next_target = False
        if next_pred:
            pred_end += len(pred_word)
            next_pred = False

        # Exact match of the location and string
        if target_word == pred_word and target_end == pred_end:
            count += 1
            target_i += 1
            pred_i += 1
            next_pred = True
            next_target = True
        # Choose the list of shorter length to iterate
        else:
            if target_end > pred_end:
                pred_i += 1
                next_pred = True
            elif target_end < pred_end:
                target_i += 1
                next_target = True
            else:
                pred_i += 1
                target_i += 1
                next_pred = True
                next_target = True
    return count


def precision(target, pred):
    """Calculate precision"""
    pred_len = len(pred)
    count = match_count(target, pred)
    return count / pred_len


def recall(target, pred):
    """Calculate recall"""
    target_len = len(target)
    count = match_count(target, pred)
    return count / target_len


def f1_score(target, pred):
    prec = precision(target, pred)
    rec = recall(target, pred)
    return (2 * prec * rec) / (prec + rec)


# if __name__ == '__main__':
#     target = '我 爱 中国'.split()
#     pred = '我爱 中国'.split()
#     print('prec: ', precision(target, pred))
#     print('recall: ', recall(target, pred))
#     print('F1: ', f1_score(target, pred))