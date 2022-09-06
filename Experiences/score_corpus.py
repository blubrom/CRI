import experience_functions as ex
import argparse
import os
import re
from experience_functions import SmartFormatter
from progress.bar import Bar
from datetime import datetime
import sys

li = "----------------------------------------------------------------------------------------------------------"

parser = argparse.ArgumentParser(
    description="evaluates all of the articles \
    in the Corpus and prints the results", formatter_class=SmartFormatter)
parser.add_argument("-c", "--Corpus",
                    help="the path to the Corpus dir",
                    default=ex.corpus_path)
parser.add_argument("-e", "--Expected_results",
                    help="the path to the results dir",
                    default=ex.expected_results_path)
parser.add_argument(
    "-o", "--output",
    help="if providied, the results will be printed in this file")
parser.add_argument("-m", "--mode", type=int,
                    default=ex.default_mode,
                    help=ex.help_mode, choices=ex.mode_choices)
parser.add_argument(
    "-v", "--Verbose", help="if activated prints the results on each article",
    default=1, type=int)
parser.add_argument("-t", "--Take_traps", type=int, default=1,
                    help="consider articles with no expected output when scoring")
parser.add_argument("-cl", "--Classifier", default="CRI",
                    choices=["CRI", "LINNAEUS", "SPECIES"],
                    help="the classifier used")
parser.add_argument("-r", "--regex", help=ex.help_regex,
                    default=ex.default_regex)
parser.add_argument("-s", "--stopwords",
                    help=ex.help_stopwords, default=ex.stopwords_path)
args = parser.parse_args()

# format for the date of when the experience was carried
today = datetime.now()
daytime = today.strftime("%B %d, %Y at %H:%M:%S")


# evaluates each article in the corpus
# according to the expected results in exp
# and chosen mode
# gives the overall score using the total numbers
# of false positives, negatives and true positives
# obtained processing the corpus
def evaluation(corpus, exp, classifier, mode, expr, stopwords):
    result = ""
    nfps = nfns = ntps = 0
    with os.scandir(corpus) as it:
        count = len([entry for entry in it if entry.is_file()])
    bar = Bar('Processing ' + corpus.name, fill='#', max=count)
    with os.scandir(corpus) as it:
        for entry in it:
            if entry.is_file():
                page = re.search(
                    r"page_(?P<page>[0-9]+)\.txt", entry.name)
                if page is None:
                    exit(f"Corpus article : {entry.name}  in the wrong format")
                page = page.group("page")
                expected = exp[int(page)]
                if args.Take_traps != 0 or len(expected) > 0:
                    name = re.sub(r"\.txt", "", entry.name)
                    s, tps, fns, fps = ex.evaluate(
                        os.path.join(corpus, entry.name), name, expected,
                        classifier, stopwords, mode=mode, expr=expr)
                    if args.Verbose:
                        result += s
                    ntps += tps
                    nfps += fps
                    nfns += fns
                bar.next()
        precision, recall, fm = ex.score(nfps, nfns, ntps)
        prec = "{:.2f}".format(precision*100)
        rec = "{:.2f}".format(recall*100)
        fmes = "{:.2f}".format(fm*100)
        result += f"\noverall scores on the corpus {corpus.name}:\n\tprecision = {prec} %\n"
        if args.Verbose:
            result += f"\trecall = {rec} %\n\tF-measure = {fmes} %\n\n{li}\n{li}\n\n"
        else:
            result += f"\trecall = {rec} %\n\tF-measure = {fmes} %\n"
        bar.finish()
    return (result, nfps, nfns, ntps)


if __name__ == "__main__":
    if args.mode == 0 and args.regex == ex.default_regex:
        exit(ex.missing_regex_message)
    stopwords = ex.compile_stopwords(args.stopwords)
    sys.path.insert(0, f'./{args.Expected_results}')
    import expected_results_vol12 as vol12
    import expected_results_vol83 as vol83
    import expected_results_vol126 as vol126
    import expected_results_vol155 as vol155
    expected = {12: vol12.expected, 83: vol83.expected,
                126: vol126.expected, 155: vol155.expected}
    results = f"# {li}\nExperience launched on {daytime} with mode {args.mode}\n{li}\n"
    nfps = nfns = ntps = 0
    with os.scandir(args.Corpus) as it:
        for entry in it:
            if entry.is_dir():
                if args.Verbose:
                    results += f"## starting evaluation of volume {entry.name}\n"
                vol_num = int(re.search(r"\d+", entry.name).group(0))
                (result, fps, fns, tps) = evaluation(
                    entry, expected[vol_num], args.Classifier, args.mode, args.regex, stopwords)
                results += result
                ntps += tps
                nfps += fps
                nfns += fns
        precision, recall, fm = ex.score(nfps, nfns, ntps)
        prec = "{:.2f}".format(precision*100)
        rec = "{:.2f}".format(recall*100)
        fmes = "{:.2f}".format(fm*100)
        results += f"## overall scores on the whole corpus:\n\tprecision = {prec} %\n"
        results += f"\trecall = {rec} %\n\tF-measure = {fmes} %\n"
ex.print_res(args.output, results)
