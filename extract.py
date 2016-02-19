#!/usr/bin/env python3.5

import argparse
import os
import os.path

import docx
import docx.enum.text

overrides = {}
clean = True

def process(fname):
    """Process file fname.docx and create a transcript file fname.txt that has just the text of
    the respondent. The respondent is determined by linguistic analysis---it's the person who said
    the most, unless there is an overrride."""

    # Remove trans filenames
    fbase = os.path.basename(fname)
    if fbase.startswith("~") or not fname.endswith(".docx"):
        return
    if "NOTES" in fname.upper():
        return
    transcript_fname = fname.replace(".docx", ".txt")
    # don't create a transcript that already exists...
    if os.path.exists(transcript_fname) and os.path.getsize(transcript_fname) > 0 and not clean:
        return
    print(fname)
    d = docx.Document(fname)
    # Make sure transcript file is properly encoded
    assert d.tables[0].rows[0].cells[0].text == 'Date:'
    date = d.tables[0].rows[0].cells[1].text
    print("{} {}".format(os.path.basename(fname),date),end='   ')

    # Remember output for each speaker.
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

    # After examining several approaches for distinguishing the respondent
    # (vocab, # of question marks, etc),
    # we decided to go with the longest characters.

    if fbase in overrides:
        respondent = overrides[fbase]
        rtext = "\n".join(speakers[respondent])
    else:
        text_per_speaker = ["\n".join(speakers[speaker]) for speaker in speakers.keys()]
        (length, rtext) = max([(len(text), text) for text in text_per_speaker])
    with open(transcript_fname, "w") as f:
        f.write(rtext)

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
