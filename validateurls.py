#!/usr/bin/env python3.5
#
# validate the URLs in a docx text file

import argparse
import re
import urllib
import urllib.request
import urllib.response
from zipfile import ZipFile


# http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
def process(fname):
    z = ZipFile(fname)
    assert isinstance(z, ZipFile)
    footnotes = z.open("word/footnotes.xml").read().decode('utf-8')
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', footnotes)
    for url in urls:
        if '<' in url: url = url[0:url.find("<")]
        if "schemas.microsoft.com" in url: continue
        if "schemas.openxmlformats.org" in url: continue
        print(url)
        try:
            u = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(" *** bogus URL: {}: {}".format(url, e))
        except urllib.error.URLError as e:
            print(" *** bogus URL: {}: {}".format(url, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Analyze DOCX transcript files from TranscribeMe!")
    parser.add_argument("files", help="Files or directories to analyze", nargs="+")
    args = parser.parse_args()

    for fname in args.files:
        process(fname)
