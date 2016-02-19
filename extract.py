#!/usr/bin/env python3.5

import argparse
import os
import os.path

import docx
import docx.enum.text


def process(fname):
    if os.path.basename(fname).startswith("~") or not fname.endswith(".docx"):
        return
    if "/NOTES/" in fname:
        return
    transcript_fname = "transcripts/" + os.path.splitext(os.path.basename(fname))[0]+".txt"
    if os.path.exists(transcript_fname):
        return
    print(fname)
    d = docx.Document(fname)
    assert d.tables[0].rows[0].cells[0].text == 'Date:'
    date = d.tables[0].rows[0].cells[1].text
    print("{} {}".format(os.path.basename(fname),date),end='   ')
    speakers = {}
    errors = []
    for table in d.tables[1:]:
        for row in table.rows:
            try:
                c0 = row.cells[0].text
                c1 = row.cells[1].text
            except IndexError:
                continue
            speaker = c0[0:2]
            when    = c0[4:]
            if speaker:
                if speaker not in speakers: speakers[speaker] = []
                speakers[speaker].append(c1)
                continue
            if c1=='[silence]':
                continue
            errors.append("** unknown c0: {}  c1: {}".format(c0,c1))
    counts = []
    text_per_speaker = []
    qcount_per_speaker = []
    for (speaker,text) in speakers.items():
        fulltext = "".join(text)
        qcount = fulltext.count('?')
        print("{}: {} ({}?)   ".format(speaker,len(fulltext),qcount),end=' ')
        text_per_speaker.append((len(fulltext), speaker))
        qcount_per_speaker.append((qcount, speaker))
    # max_text   = max(text_per_speaker)[1]
    # Right now, assume the respondent is the person who answered the most questions
    min_qcount = min(qcount_per_speaker)[1]
    # assert max_text == min_qcount
    # print("")
    print("\n".join(errors))
    print("")
    respondent = min_qcount
    # Create the transcript with the most text
    with open(transcript_fname, "w") as f:
        f.write("\n".join(speakers[respondent]))





if __name__=="__main__":
    try:
        os.mkdir("transcripts")
    except FileExistsError:
        pass
    parser = argparse.ArgumentParser("Analyze DOCX transcript files from TranscribeMe!")
    parser.add_argument("files",help="Files or directories to analyze",nargs="+")
    args = parser.parse_args()
    for fname in args.files:
        print("f2:",fname,os.path.isdir(fname))
        if os.path.isfile(fname):
            process(fname)
        if os.path.isdir(fname):
            for (dirpath,dirnames,filenames) in os.walk(fname):
                for filename in filenames:
                    if filename.endswith(".docx"):
                        process(os.path.join(dirpath,filename))
