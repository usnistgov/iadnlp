#!/usr/bin/env python3.5
#
# sentiment analysis on security expert transcripts
import os.path

from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import MWETokenizer

import makecloud

if __name__ == "__main__":
    # Read the words of interest
    words = open("emotion_words.txt").read().lower().split("\n")
    sentiment_bag = set()

    # Get the multi-word expression tokenizer and add each to the sentiment_bag
    mwe = set(filter(lambda a: " " in a, words))
    print("Multi-word expressions in emotion words: {}".format(",".join(mwe)))

    # Create the MWE tokenizer
    mwe_tokenizer = MWETokenizer()
    for s in mwe:
        print("Add mwe ", s)
        mwe_tokenizer.add_mwe(s.split(" "))
        sentiment_bag.add(s.replace(" ", "_"))

    lmtzr = WordNetLemmatizer()
    st = LancasterStemmer()
    ps = PorterStemmer()
    print("Stemming:")
    for word in filter(lambda a: " " not in a, words):
        print("{} => {} / {} / {}".format(word, lmtzr.lemmatize(word), st.stem(word), ps.stem(word)))
        sentiment_bag.add(word)
        sentiment_bag.add(st.stem(word))  # I like this one the best

    # Process all the lists
    for (label, files) in makecloud.TRANSCRIPTS.items():
        scores = []
        print("{}:\n{}=".format(label, "=" * len(label)))

        scount = 0
        for fname in files:
            raw = open(fname, "r").read().lower()
            tokens = word_tokenize(raw)
            tokens = mwe_tokenizer.tokenize(tokens)
            tokens = list(filter(st.stem, tokens))
            bar = ""
            for t in tokens:
                if t in sentiment_bag:
                    bar += "*"
                    scount += 1
                    # print(t," ",end="")
            score = scount / len(tokens)
            print("{:35s}  {:3.6f} {}".format(os.path.basename(fname), score, bar))
            scores.append(score)
        print("\n{} Average Score: {:3.6f}".format(str.capitalize(label), sum(scores) / len(scores)))
        print("\n\n")
