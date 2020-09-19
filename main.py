import data_process

if __name__ == "__main__":
    train = data_process.Data('data/train.txt')
    train.token2vocab('vocab_dict.json')
    vocab = data_process.Vocab('vocab_dict.json')
    print(vocab['你'])
    print('中国' in vocab)
