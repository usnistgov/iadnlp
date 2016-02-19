#!/usr/bin/env python3.5
#

# http://sebastianraschka.com/Articles/2014_twitter_wordcloud.html

import glob
from collections import defaultdict

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def process(outfile, infiles):
    """
Process a set of transcript files and generate both wordcloud and the linguistic top-N
    :rtype: None
    """
    print("\n".join(infiles))
    assert len(infiles) > 0
    text = [open(fname).read() for fname in infiles]
    fulltext = "\n".join(text)
    wordcounts = defaultdict(int)
    doccounts = defaultdict(int)
    words = set()
    for t in text:
        docwords = set(t.split())
        for word in t.split():
            wordcounts[word] += 1
        for word in docwords:
            doccounts[word] += 1
        words.union(docwords)

    # Now rank each word by TF/IDF
    for word in words:
        print(word, doccounts[word] / wordcounts[word])
    exit(0)

    wc = WordCloud(width=1024, height=640)
    wc.generate_from_text(fulltext)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(outfile, dpi=300)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Analyze the TXT transcript files and build a word cloud!")
    args = parser.parse_args()
    # Get the text from the input files

    process("expert.png", glob.glob("transcripts/*Expert*/*.txt"))
    process("expert_nist.png", glob.glob("transcripts/NIST Expert*/*.txt"))
    process("expert_marsh.png", glob.glob("transcripts/*Marsh*Expert*/*.txt"))
    process("genearl.png", glob.glob("transcripts/*General*/*.txt"))
