#!/usr/bin/env python3.5
#

# http://sebastianraschka.com/Articles/2014_twitter_wordcloud.html

import matplotlib.pyplot as plt
from wordcloud import WordCloud

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Analyze DOCX transcript files from TranscribeMe!")
    parser.add_argument("files", help="Files or directories to analyze", nargs="+")
    args = parser.parse_args()
    # Get the text from the input files

    text_array = [open(fn).read() for fn in args.files]
    text = "\n".join(text_array)

    d = open("transcripts/MW201", "r")
    wc = WordCloud(width=1024, height=640)
    wc.generate(text)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig("data.pdf", dpi=300)
    plt.show()
