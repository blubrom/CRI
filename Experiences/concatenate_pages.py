import os
import argparse


parser = argparse.ArgumentParser(
    description="concatenates pages, used to create corpus")
parser.add_argument(
    "-n", "--number",
    help="if providied, the volume number")
parser.add_argument("start", type=int, help="starting page")
parser.add_argument("end", type=int, help="end_page, excluded")

args = parser.parse_args()

vol = str(155)
if args.number:
	vol = args.number
start = args.start
starting_page = str(start)
# non inclus
end = args.end

for page in range(start, end):
    cmd = f"cat archives_La_Nature/cnum_4KY28.{vol}/texts/cnum_4KY28.{vol}" + \
          f"_page_{format(page, '03d')}.txt >>" + \
          f" Corpus/vol{vol}/page_{starting_page}.txt"
    os.system(cmd)
    os.system(f"echo '\n' >> Corpus/vol{vol}/page_{starting_page}.txt")
