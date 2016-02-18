#!/usr/bin/env python3.5

import docx
import docx.enum.text
import argparse
import os, os.path


def process(fname):
    if os.path.basename(fname).startswith("~") or not fname.endswith(".docx"):
        return
    d = docx.Document(fname)
    assert d.tables[0].rows[0].cells[0].text == 'Date:'
    date = d.tables[0].rows[0].cells[1].text
    print("{} {}".format(os.path.basename(fname),date),end='   ')
    speakers = {}
    errors = []
    for row in d.tables[1].rows:
        c0 = row.cells[0].text
        c1 = row.cells[1].text
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
    for (speaker,text) in speakers.items():
        fulltext = "".join(text)
        qcount = fulltext.count('?')
        print("{}: {} ({}?)   ".format(speaker,len(fulltext),qcount),end=' ')
        counts.append((qcount,speaker))
    print("")
    print("\n".join(errors))
    print("")





if __name__=="__main__":
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
