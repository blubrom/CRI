import argparse
import re
import experience_functions as ex

parser = argparse.ArgumentParser(
    description="sort the classification")
parser.add_argument(
    "-o", "--output",
    help="if providied, the results will be printed in this file")
parser.add_argument("-p", "--path", help="the path to the classification",
                    default="results/classification_archives.txt")
parser.add_argument("mode", choices=["species", "year", "page"],
                    help="choose the sort mode")

args = parser.parse_args()

re_year = re.compile(r"cnum_4KY28\.(?P<a>\d+)")
re_species = re.compile(r"\w+ (?P<a>\w+)")
re_page = re.compile(r"cnum_4KY28\.(\d+)_page_(\d+)")


# define the sorting key
# according to the users demand
def key_s(s):
    if args.mode == "species":
        return re_species.search(s).group("a")
    if args.mode == "year":
        return int(re_year.search(s).group("a"))
    if args.mode == "page":
        r = re_page.search(s)
        return (int(r[1]), int(r[2]))


res = ""
with open(args.path, "r") as in_:
    lines = in_.readlines()
for line in sorted(lines, key=key_s):
    res += line

ex.print_res(args.output, res)
