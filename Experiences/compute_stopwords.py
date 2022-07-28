import argparse
import os
import regex as re
from os import path
import experience_functions as ex

parser = argparse.ArgumentParser(
    description="scans trough a volume and computes \
    the most frequently used words")
parser.add_argument("-v", "--volume",
                    help="if provided, the volume in wich to do the operation")
parser.add_argument("output", help="the results are printed in the file")
parser.add_argument("-p", "--path", help="the path to the volumes",
                    default=ex.volumes_path)
parser.add_argument("-n", "--number", type=int, default=25000,
                    help="the number of stopwords to keep")
parser.add_argument("-m", "--mode", choices=["word", "digrams"], default="word",
                    help="the way stopwords are generated")
parser.add_argument(
    "-w", "--words", help="the path to the file containing the words",
    default="Experiences/words_uncorrected.txt")
args = parser.parse_args()


# searches the archive for the volume numbered vol_num
# and returns the path to its pages
def get_volume_path(vol_num, vol_path):
    with os.scandir(vol_path) as it:
        for entry in it:
            if entry.is_dir():
                num_m = re.match(
                    r"^cnum_4KY28\.(?P<num>\d+)$", entry.name)
                num = num_m.group("num")
                if num == vol_num:
                    return path.join(vol_path, entry.name, "texts")
    exit(f"couldn't find the volume {vol_num} in the dir {args.path}")


punctuation_spaces = re.compile(r"\W|\s", flags=re.IGNORECASE)
digrams = re.compile(r"\w \w", flags=re.IGNORECASE)


# goes trough a page and counts the occurences of each word
# present in it then modifies words_dict accordingly
def scan_page(page_file, words_dict):
    with open(page_file, "r") as page:
        text = ("".join(page) + "").lower()
        if args.mode == "word":
            words = filter(lambda a: a, punctuation_spaces.split(text))
        elif args.mode == "digrams":
            words = digrams.finditer(text, overlapped=True)
        for word in words:
            if word not in words_dict:
                words_dict[word] = 1
            else:
                words_dict[word] += 1
    return dict


def scan_volume(volume_path, words_dict={}):
    with os.scandir(volume_path) as it:
        for entry in it:
            if entry.is_file():
                scan_page(entry, words_dict)
    return words_dict


# calculates the number of occurences for each word
# in the volumes and writes all the words
# sorted by frequency in the file given by the user
def create_word_list(volumes_path):
    words_dict = {}
    with os.scandir(volumes_path) as it:
        for entry in it:
            if entry.is_dir():
                vol_path = path.join(volumes_path, entry.name, "texts")
                scan_volume(vol_path, words_dict=words_dict)
    with open(args.words, "w") as words:
        words_list = "\n".join(
            sorted(words_dict, key=words_dict.get, reverse=True))
        words.write(words_list)


if not path.exists(args.words) and args.volume is None:
    create_word_list(args.path)
if args.volume is not None:
    volume_path = get_volume_path(args.volume, args.path)
    words_dict = scan_volume(volume_path)
    itw = sorted(words_dict, key=words_dict.get, reverse=True)
else:
    with open(args.words, "r") as words:
        text = "".join(words)
        itw = re.split("\n", text)

result = r"("
with open(args.output, "w") as out:
    ct = 0
    for word in itw:
        # do not remove single letter words
        # In prevision of serching the abreviated binoms
        if(len(word) > 1):
            result += word[0] + \
                "(?P<mid_word>" + word[1:-1] + ")" + word[-1] + "|"
        ct += 1
        if ct == args.number:
            break
    result = result[:-1] + r")"
    out.write(result)
    out.write(f"\nnumber of words : {args.number}")
