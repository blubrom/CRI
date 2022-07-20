import argparse
import re
import json

parser = argparse.ArgumentParser(
    description="verifies that all of the names in  \
    the list appear in the right order in the article")
parser.add_argument("article", help="the article in wich to check")
parser.add_argument("names", help="the list of names to check, \
                    provided in a file in json format")
args = parser.parse_args()

with open(args.article, "r") as article:
    s = re.sub(r"\n", " ", "".join(article))

names = json.load(open(args.names, "r"))

start = 0
for name in names:
    r = re.compile(name)
    m = r.search(s, start)
    if not m:
        exit(
            f"Error: couldn't find: {name} starting at position \
            {start} in file: {args.article}")
    else:
        start = m.start()

print("Success !!")
