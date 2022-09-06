import argparse
import os
import regex as re
import experience_functions as ex
from experience_functions import SmartFormatter
from progress.bar import Bar
from multiprocessing import Pool
import numpy
from pathlib import Path

parser = argparse.ArgumentParser(
    description="scans trough a volume and finds the binoms", formatter_class=SmartFormatter)
parser.add_argument("-v", "--volume",
                    help="if provided, the volume number in wich to do the\
                    operation, else scans trough the whole archive")
parser.add_argument(
    "-o", "--output",
    help="if providied, the results will be printed in this file")
parser.add_argument("-i", "--input", help="the file or directory to classify")
parser.add_argument("-p", "--path", help="the path to the volumes",
                    default=ex.volumes_path)
parser.add_argument("-m", "--mode", type=int,
                    default=ex.default_mode,
                    help=ex.help_mode, choices=ex.mode_choices)
parser.add_argument("-r", "--regex", help=ex.help_regex,
                    default=ex.default_regex)
parser.add_argument("-s", "--stopwords",
                    help=ex.help_stopwords, default=ex.stopwords_path)

args = parser.parse_args()


# searches the archive for the volume numbered vol_num
# and returns the path to its pages
def get_volume_path(vol_num, path):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                num_m = re.match(
                    r"^cnum_4KY28\.(?P<num>\d+)$", entry.name)
                num = num_m.group("num")
                if num == vol_num:
                    return os.path.join(path, entry.name, "texts")
    exit(f"couldn't find the volume {vol_num} in the dir {args.path}")


punctuation_spaces = re.compile(r"\W|\s", flags=re.IGNORECASE)


# given a page, returns the list of matches
def scan_page(p, stopwords, mode, expr):
    with open(p, "r") as page:
        res = ex.classify(
            page.read(), stopwords, context=True, mode=mode, expr=expr)
        return [r[0] + " in: " + p.name + " context: " + r[1] for r in res]


def scan_volume(volume_path, mode, expr, stopwords):
    # with Pool() as pool:
    #     pages = [os.path.join(volume_path, p) for p in os.listdir(volume_path)]
    #     matches = pool.imap(scan_page, pages, 4)
    # return list(numpy.concatenate(matches).flat)

    # with os.scandir(volume_path) as it:
    #     nb = len([entry for entry in it if entry.is_file()])
    # count = 0
    # percent = nb // 100 if nb > 100 else nb
    # bar = Bar('Processing ' + volume_path, fill='#', suffix='%(percent)d%%')
    matches = []
    with os.scandir(volume_path) as it:
        for entry in it:
            # if count == 0:
            #     bar.next()
            if entry.is_file():
                matches += scan_page(entry, stopwords, mode, expr)
    #         count = (count + 1) % percent
    # bar.finish()
    print("finished scanning volume " + volume_path)
    return matches


# get all the matches for the volume entry
# used to process the different volumes in paralell with Pool.map
def process_volume(volume_name, stopwords):
    vol_p = os.path.join(args.path, volume_name, "texts")
    matches = scan_volume(vol_p, args.mode, args.regex, stopwords)
    print(f"finished processing {volume_name}")
    return matches


def reccursively_process(entry, path, stopwords, mode, expr):
    for f in os.scandir(entry):
        p = os.path.join(path, f.name)
        if f.is_dir():
            # create the directory where output will be
            #  stored if non-already existing
            cmd = "mkdir -p " + p
            os.system(cmd)
            reccursively_process(f, p, stopwords, mode, expr)
        if f.is_file():
            r = scan_page(f, stopwords, mode, expr)
            res = "\n".join(r)
            with open(p, "a") as out:
                out.write(res)


if __name__ == "__main__":
    if args.mode == 0 and args.regex == ex.default_regex:
        exit(ex.missing_regex_message)
    stopwords = ex.compile_stopwords(args.stopwords)
    matches = []
    if args.input:
        i = Path(args.input)
        if i.is_file():
            matches = scan_page(i, stopwords, args.mode, args.regex)
            res = "\n".join(matches)
            ex.print_res(args.output, res)
        else:
            cmd = "mkdir -p " + args.output
            os.system(cmd)
            reccursively_process(
                args.input, args.output, stopwords, args.mode, args.regex)
    else:
        if args.volume:
            volume_path = get_volume_path(args.volume, args.path)
            matches = scan_volume(volume_path, args.mode)
        else:
            # # actuellement très inneficace, trouver pourquoi.
            # with Pool() as pool:
            #     volume_names = os.listdir(args.path)
            #     matches = pool.map(process_volume, volume_names)
            #     # flatten the list
            #     matches = list(numpy.concatenate(matches).flat)
            #     # sort the results by alphabetical order of genre names
            #     # then species name (then volume/page)
            #     matches = sorted(matches)
            with os.scandir(args.path) as it:
                nb = len([entry for entry in it if entry.is_dir()])
            count = 0
            percent = nb // 100 if nb > 100 else nb
            bar = Bar('Processing archive',
                      fill='#', suffix='%(percent)d%%')
            matches = []
            with os.scandir(args.path) as it:
                for entry in it:
                    if count == 0:
                        bar.next()
                    if entry.is_dir():
                        matches += scan_volume(os.path.join(entry,
                                                            "texts"), args.mode, args.regex, stopwords)
                    count = (count + 1) % percent
            bar.finish()
        # print the results as a string of all results, one match per line
        res = "\n".join(matches)
        ex.print_res(args.output, res)
