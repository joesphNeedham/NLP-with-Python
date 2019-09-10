# -*- coding:utf-8 -*-
import codecs
import pycrfsuite


def convert_char_to_label():
    """
    1. 用于判断某个字符是否是一个word的开头
    :return:
    """
    prepared_sentence = []  # 每个元素对应的是一行字符串对应的label表示
    with open("H:\\TanBoOwn\\Github\\CRF\\crf_train_corpus.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lengths = [len(w) for w in line.split(" ")]
            positions = []

            next_pos = 0
            for length in lengths:
                next_pos = next_pos + length
                positions.append(next_pos)
            concatenated = line.replace(" ", "")

            chars = [c for c in concatenated]
            labels = [0 if i not in positions else 1 for i, c in enumerate(concatenated)]
            prepared_sentence.append(list(zip(chars, labels)))
    return prepared_sentence


def create_char_features(sentence, i):
    features = [
        'bias',
        'char=' + sentence[i][0]
    ]

    if i >= 1:
        features.extend([
            'char-1=' + sentence[i-1][0],
            'char-1:0=' + sentence[i-1][0] + sentence[i][0],
        ])
    else:
        features.append("BOS")

    if i >= 2:
        features.extend([
            'char-2=' + sentence[i-2][0],
            'char-2:0=' + sentence[i-2][0] + sentence[i-1][0] + sentence[i][0],
            'char-2:-1=' + sentence[i-2][0] + sentence[i-1][0],
        ])

    if i >= 3:
        features.extend([
            'char-3:0=' + sentence[i-3][0] + sentence[i-2][0] + sentence[i-1][0] + sentence[i][0],
            'char-3:-1=' + sentence[i-3][0] + sentence[i-2][0] + sentence[i-1][0],
        ])


    if i + 1 < len(sentence):
        features.extend([
            'char+1=' + sentence[i+1][0],
            'char:+1=' + sentence[i][0] + sentence[i+1][0],
        ])
    else:
        features.append("EOS")

    if i + 2 < len(sentence):
        features.extend([
            'char+2=' + sentence[i+2][0],
            'char:+2=' + sentence[i][0] + sentence[i+1][0] + sentence[i+2][0],
            'char+1:+2=' + sentence[i+1][0] + sentence[i+2][0],
        ])

    if i + 3 < len(sentence):
        features.extend([
            'char:+3=' + sentence[i][0] + sentence[i+1][0] + sentence[i+2][0]+ sentence[i+3][0],
            'char+1:+3=' + sentence[i+1][0] + sentence[i+2][0] + sentence[i+3][0],
        ])

    return features


def create_sentence_features(prepared_sentence):
    return [create_char_features(prepared_sentence, i) for i in range(len(prepared_sentence))]


def create_sentence_labels(prepared_sentence):
    return [str(part[1]) for part in prepared_sentence]


if __name__ == "__main__":
    prepared_sentences = convert_char_to_label()
    X = [create_sentence_features(ps) for ps in prepared_sentences[:-1000]]
    y = [create_sentence_labels(ps) for ps in prepared_sentences[:-1000]]

    X_test = [create_sentence_features(ps) for ps in prepared_sentences[-1000:]]
    y_test = [create_sentence_labels(ps) for ps in prepared_sentences[-1000:]]

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X, y):
        trainer.append(xseq, yseq)
    trainer.set_params({
        'c1': 1.0,
        'c2': 1e-3,
        'max_iterations': 60,
        'feature.possible_transitions': True
    })

    trainer.train('latin-text-segmentation.crfsuite')

    tagger = pycrfsuite.Tagger()
    tagger.open('latin-text-segmentation.crfsuite')

    predictions = tagger.tag(create_sentence_features("dominusadtemplumproperat"))
    print(predictions)




