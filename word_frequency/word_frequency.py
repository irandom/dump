#!/usr/bin/env python3

import collections
import operator
import os

import spacy


def init_frequencies():
    return collections.defaultdict(int)


def update_frequencies(nlp, frequencies, file_name):
    with open(file_name) as f:
        text = f.read()
    tokens = nlp(text)
    for token in tokens:
        frequencies[(token.lemma_, token.pos_)] += 1


def main():
    nlp = spacy.load("pt_core_news_lg")
    files = os.listdir("texts")
    frequencies = init_frequencies()
    for file in files:
        update_frequencies(nlp, frequencies, os.path.join("texts", file))

    for i in sorted([dict(count=v, lemma=k[0], pos=k[1]) for k, v in frequencies.items() if k[1] not in ["SPACE", "PUNCT"]], key=operator.itemgetter('count'), reverse=True):
        print(i)


if __name__ == "__main__":
    main()
