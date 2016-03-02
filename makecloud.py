#!/usr/bin/env python3.5
#

# http://sebastianraschka.com/Articles/2014_twitter_wordcloud.html

import glob
from collections import defaultdict

import matplotlib.pyplot as plt
from wordcloud import WordCloud

ALL_EXPERTS = glob.glob("transcripts/*Expert/*.txt")
NIST_EXPERTS = glob.glob("transcripts/NIST Expert*/*.txt")
NON_NIST_EXPERTS = glob.glob("transcripts/M*Expert*/*.txt")
GENERAL = glob.glob("transcripts/*General*/*.txt")

TRANSCRIPTS = {"expert_all": ALL_EXPERTS,
               "expert_nist": NIST_EXPERTS,
               "expert_non-nist": NON_NIST_EXPERTS,
               "general": GENERAL
               }


def cloud_for_document(outfile=None, fulltext=None):
    """Create a wordcloud for the DOCUMENT and save the result in OUTFILE"""
    assert outfile != None
    assert fulltext != None
    wc = WordCloud(width=1024, height=640)
    wc.generate_from_text(fulltext)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(outfile, dpi=300)


def process(outfile, infiles):
    """
Process a set of transcript files and generate both wordcloud and the linguistic top-N
    :rtype: None
    """
    print("Create {} from:")
    for line in infiles:
        print("     {}".format(line))
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

    cloud_for_document(outfile, fulltext)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Analyze the TXT transcript files and build a word cloud!")
    args = parser.parse_args()
    # Get the text from the input files

    for (label, files) in TRANSCRIPTS.items():
        process(label + ".png", files)
