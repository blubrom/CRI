import argparse
import json
import experience_functions as ex
import os
import re

parser = argparse.ArgumentParser(
    description="Retrieve the pairs of the form specified by MODE")
parser.add_argument("article", help="the article in wich to do the operation")
parser.add_argument(
    "-o", "--output", help="If provided the results are printed in the file")
parser.add_argument("-m", "--mode", choices=ex.modes,
                    default=ex.default_mode,
                    help="choose the mode of recognition")
parser.add_argument("-r", "--Expected_results",
                    help="the path to the results dir",
                    default=ex.expected_results_path)
args = parser.parse_args()

with open(args.article, "r") as article:
    art_name = os.path.basename(args.article)
    page = re.match(
        r"[A-Za-z_-]+_(?P<page>p[0-9]+)\.txt", art_name)
    if not page:
        exit(f"Corpus article : {art_name} in the wrong format")
    page = page.group("page")
    with open(os.path.join(args.Expected_results, page + ".json")) as x:
        expected = json.load(x)
    result, _, _, _ = ex.evaluate(article, art_name, expected, args.mode)
    ex.print_res(args.output, f"chosen mode : {args.mode}\n {result}")
