import re
import argparse
import os

parser = argparse.ArgumentParser(
    description="preprocessing the corpus")
parser.add_argument("-c", "--Corpus",
                    help="the path to the Corpus dir",
                    default="Corpus")
parser.add_argument("-o", "--output",
                    help="the path to the processed corpus",
                    default="Processed_corpus")
args = parser.parse_args()

li = [rf"({i}(?=\D)(?=\w)|(?<=\D)(?<=\w){i})" for i in range(10)]
nested0 = re.compile(li[0])
nested1 = re.compile(li[1])
nested2 = re.compile(li[2])
nested3 = re.compile(li[3])
nested4 = re.compile(li[4])
nested5 = re.compile(li[5])
nested6 = re.compile(li[6])
nested7 = re.compile(li[7])
nested8 = re.compile(li[8])
nested9 = re.compile(li[9])
ja = re.compile(r"(?<=\W)(j|J|h|H|I|i|f|F|t|T)a(?=\W)")


def pretraitement(article):
    corrections = re.sub(r"-(\s+)", "", article)
    corrections = re.sub(r"\s+", " ", corrections)
    corrections = nested2.sub("s", corrections)
    corrections = nested3.sub("B", corrections)
    corrections = nested4.sub("", corrections)
    corrections = nested5.sub("s", corrections)
    corrections = nested6.sub("b", corrections)
    corrections = nested7.sub("l", corrections)
    corrections = nested8.sub("b", corrections)
    corrections = nested9.sub("", corrections)
    corrections = nested1.sub("l", corrections)
    corrections = nested0.sub("o", corrections)
    corrections = ja.sub("la", corrections)
    corrections = re.sub("$", "s", corrections)
    corrections = re.sub("£", "l", corrections)
    return corrections


def reccursively_process(entry, path):
    for f in os.scandir(entry):
        if f.is_dir():
            # create the directory where output will be
            #  stored if non-already existing
            p = os.path.join(path, f.name)
            cmd = "mkdir -p " + p
            os.system(cmd)
            reccursively_process(f, p)
        if f.is_file():
            with open(f, "r") as in_:
                r = pretraitement(" ".join(in_) + " ")
            p = os.path.join(path, f.name)
            with open(p, "w") as out:
                out.write(r)


reccursively_process(args.Corpus, args.output)

# for entry in os.scandir(args.Corpus):
#     if entry.is_dir():
#         # create the directory where output will be
#         #  stored if non-already existing
#         cmd = "mkdir -p " + os.path.join(args.output, entry.name)
#         os.system(cmd)
#     for f in os.scandir(entry):
#         if f.is_file():
#             with open(f, "r") as in_:
#                 r = pretraitement(" ".join(in_) + " ")
#             p = os.path.join(args.output, entry.name, f.name)
#             with open(p, "w") as out:
#                 out.write(r)
