import regex as re
import json
import Levenshtein as le
import os
import pandas as pd

import argparse


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


lower_case = r"[a-zæœ-]"
upper_case = r"[A-ZŒÆ]"
a_case = f"({lower_case}|{upper_case})"
acword = a_case + lower_case + "+"
lcword = lower_case + "+"
ucword = upper_case + lcword
# leave the possibility for a subgenus
# binom = ucword + r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + lcword
# lbinom = lcword + r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + lcword
# min_maj = lcword + r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + ucword
#
# stopwords = r"\s€€\s"
# acbutstop = "(?!" + stopwords + ")" + acword
# binombutstop = "(?!" + stopwords + ")" + ucword + \
#                  "(?!" + stopwords + ")" + r"\s" + lcword


def tables_relachee():
    nom_nominatif = [("us", 'M'), ("us", 'F'), ("a", 'F'), ("ma", 'N'),
                     ("er", 'M'), ("um", 'N'), ("ago", 'F'), ("is", 'F'),
                     ("ys", 'F'), ("ix", 'F'), ("oides", 'F'), ("e", 'F'),
                     ("dendron", 'N'), ("ma", 'N'), ("er", 'M'), ("er", 'N'),
                     ("es", 'M'), ("es", 'F'), ("es", 'N'), ("ex", 'M'),
                     ("ex", 'F'), ("on", 'M'), ("on", 'N'), ("io", 'M'),
                     ("ops", 'M'), ("ox", 'M'), ("as", 'F'), ("r", 'M'),
                     ("r", 'N'), ("s", 'M'), ("s", 'F'), ("s", 'N'),
                     ("o", 'N'), ("ax", 'F')]

    nom_genitif = ["i", "ii", "ae", "orum", "ium", "um", "is", "us", "ei"]

    adj_nominatif = [("us", 'M'), ("er", 'M'), ("a", 'F'), ("um", 'N'),
                     ("is", 'M'), ("is", 'F'), ("ior", 'M'), ("e", 'F'),
                     ("ior", 'F'), ("ius", 'N'), ("minor", 'M'),
                     ("minor", 'F'), ("minus", 'N'), ("major", 'M'),
                     ("major", 'F'), ("majus", 'N'), ("ans", 'M'),
                     ("ans", 'F'), ("ans", 'N'), ("ens", 'M'), ("ens", 'F'),
                     ("ens", 'N'), ("oides", 'M'), ("oides", 'F'),
                     ("oides", 'N')]
    return (nom_nominatif, nom_genitif, adj_nominatif)


def tables_restreintes():
    nom_nominatif = [("us", 'M'), ("us", 'F'), ("a", 'F'), ("ma", 'N'),
                     ("er", 'M'), ("um", 'N'), ("ago", 'F'), ("is", 'F'),
                     ("ys", 'F'), ("oides", 'F'),
                     ("dendron", 'N'), ("ma", 'N'), ("er", 'M'), ("er", 'N'),
                     ("or", 'M'), ("or", 'N'),
                     ("on", 'M'), ("on", 'N'), ("o", 'M'),
                     ("ps", 'M'), ("ex", 'M'), ("ex", 'F'), ("ex", 'N'),
                     ("ox", 'M'), ("ox", 'F'), ("ox", 'N'),
                     # ("ix", 'M'), ("ix", 'F'), ("ix", 'N'),
                     ("ax", 'M'), ("ax", 'F'), ("ax", 'N'),
                     ("yx", 'M'), ("yx", 'F'), ("yx", 'N')]

    nom_genitif = ["i", "ii", "ae", "orum", "ium", "um", "is", "us", "ei"]

    adj_nominatif = [("us", 'M'), ("er", 'M'), ("a", 'F'), ("um", 'N'),
                     ("is", 'M'), ("is", 'F'), ("ior", 'M'),
                     ("ior", 'F'), ("ius", 'N'), ("minor", 'M'),
                     ("minor", 'F'), ("minus", 'N'), ("major", 'M'),
                     ("major", 'F'), ("majus", 'N'), ("ans", 'M'),
                     ("ans", 'F'), ("ans", 'N'), ("ens", 'M'), ("ens", 'F'),
                     ("ens", 'N'), ("oides", 'M'), ("oides", 'F'),
                     ("oides", 'N')]
    return (nom_nominatif, nom_genitif, adj_nominatif)


# returns a regex that matches binoms
# (with upper_case letters at arbitrary positions) in latin form
# according to the tables inputed
def get_latin_expr(tables, case_genus, case_species):
    nom_nominatif, nom_genitif, adj_nominatif = tables
    latin_binom = r""
    # leave the possibility of a subgenus in parentheses
    # between the genus and the species name
    mid = r"\s([\(\[{]" + acword + r"[\)\]}]\s)?" + case_species
    # mid = rf"\s{case_species}"
    for t, g in nom_nominatif:
        genre_name = case_genus + t
        for tp, _ in nom_nominatif:
            species_names = mid + tp
            latin_binom += f"({genre_name}{species_names})|"
        for tp in nom_genitif:
            species_names = mid + tp
            latin_binom += f"({genre_name}{species_names})|"
        for tp, gp in adj_nominatif:
            if g == gp:
                species_names = mid + tp
                latin_binom += f"({genre_name}{species_names})|"
    # remplacer le dernier | par la parenthèse qui ferme le groupe
    return latin_binom[:-1]


# returns the pattern for recognising binoms preceding a famous naturalist
def get_names():
    linn = r"(L|l)inn(aeus)?"
    buffon = r"(B|b)uffon"
    lamarck = r"(L|l)amarck"
    humboldt = r"(H|h)umboldt"
    prec = rf"{acword}\s{acword}"
    names = rf"(?=\s({linn}|{buffon}|{lamarck}|{humboldt}))"
    return prec + names


latin_binom = get_latin_expr(tables_relachee(), ucword, lcword)
re_latin = re.compile(latin_binom)

t = tables_restreintes()
latin_focused_min_min = get_latin_expr(t, lcword, lcword)
latin_focused_maj_maj = get_latin_expr(t, ucword, ucword)
re_latin_focused = re.compile(latin_focused_maj_maj)

pattern_name = get_names()

Mm = re.compile(
    rf"(?<=\W)({latin_binom})(?!-)(?=\W)")

MmMM = re.compile(
    rf"(?<=\W)({latin_binom}|{latin_focused_maj_maj})(?!-)(?=\W)")

Mmmm = re.compile(
    rf"(?<=\W)({latin_binom}|{latin_focused_min_min})(?!-)(?=\W)")

MmMMmm = re.compile(
    rf"(?<=\W)({latin_binom}|{latin_focused_maj_maj}|{latin_focused_min_min})(?!-)(?=\W)")


def compile_stopwords(stopwords_path):
    # get the list of frequent words to remove and compile it to a regex
    with open(stopwords_path, "r") as stops:
        words = stops.readline()
        stopwords = re.compile(
            rf"(?<=\W){words.strip()}(?=\W)", flags=re.IGNORECASE)
        return stopwords


def clear_stopwords(stopwords, article):
    return stopwords.sub(r"€\g<mid_word>€", article)


def contextualize(m, s, start, end, context, size):
    return (m, s[max(start-size, 0):min(end+size, len(s))]) if context else m


def update_results(s, context, size, result, match):
    m = match[0]
    c = contextualize(m, s, match.start(), match.end(), context, size)
    result.append(c)


# evaluates the article according with the asked mode
def classify(article, stopwords, context=False, size=30, mode=3, expr=""):
    if mode >= 3:
        abbrev = True
    else:
        abbrev = False
    if mode == 0:  # User regex
        matcher = re.compile(expr)
    if mode == 1:  # Mm
        matcher = Mm
    elif mode == 2:  # Mm MM
        matcher = MmMM
    elif mode == 3:  # Mm A
        matcher = Mm
    elif mode == 4:  # Mm MM A
        matcher = MmMM
    elif mode == 5:  # Mm mm A
        matcher = Mmmm
    elif mode == 6:  # Mm MM mm A
        matcher = MmMMmm
    else:
        # should not arrive but if the modes change will allow to see it quickly
        exit("unexpected mode")
    s = clear_stopwords(stopwords, article)
    result = []
    r = r"(?<=\W)("
    b = False
    for match in matcher.finditer(s):
        update_results(s, context, size, result, match)
        # if the binom starts with a capitalized letter,
        # add the possibility to match a binom with thid genus abreviated
        if abbrev:
            a = re.match(upper_case, match[0])
            if a and a[0] != 'M':
                b = True
                r += rf"{a[0]}\.\s{acword}|"
    # try to find all the abreviated binoms in the page
    r = r[:-1] + r")(?=\W)"
    # do the search only if there are geni that can be abreviated
    if b:
        for match in re.finditer(r, s):
            update_results(s, context, size, result, match)
    return result


def handle_linnaeus(article):
    os.system(
        f"java -jar linnaeus/bin/linnaeus-2.0.jar --text {article} --out tmp")
    df = pd.read_csv('tmp', delimiter='\t')
    res = df["text"].tolist()
    os.system("rm -f tmp")
    return res


def handle_species(article):
    return []


# given an article, the chosen mode of recognition and
# the expected results for this article
# returns the false positives, false negatives and true positives
# when recognisiong with the mode mode
def check(article, expected, classifier, stopwords, mode=3, expr=""):
    with open(article) as in_:
        text = in_.read()
    if classifier == "CRI":
        finds = classify(text, stopwords, context=True, mode=mode, expr=expr)
    elif classifier == "LINNAEUS":
        finds = handle_linnaeus(article)
    elif classifier == "SPECIES":
        finds = handle_species(article)
    fps = []
    fns = []
    tps = []
    # get the positions in the original article of all matches
    matches = []
    prec_pos = 0
    for n, _ in finds:
        # escape the pattern so that Genus (subgenus) species is
        # correctly recognized et the parentheses
        p = re.escape(n)
        m = re.search(p, text, pos=prec_pos)
        # if the match is not in the rest of the article
        # it must be that we are looking at the abreviated binoms
        # so we have to start again from the beginning of the file
        if not m:
            m = re.search(p, text)
        matches.append((m[0], m.start(), m.end()))
        prec_pos = m.end()
    # score using the positions of the matches
    # and no more using exact matches
    for (n, b, e) in matches:
        # if there exists an expected binom in wich the current match is included
        if len(list(filter((lambda x: b >= x[1] and e <= x[2]), expected))) > 0:
            tps.append((n, b, e))
        else:
            fps.append((n, b, e))
    for (m, b, e) in expected:
        # if there does not exist a match that in included in the current expected binom
        if len(list(filter((lambda x: x[1] >= b and x[2] <= e), matches))) == 0:
            fns.append((m, b, e))
    # for tp in expected:
    #     if tp in finds:
    #         tps.append(tp)
    #     else:
    #         fns.append(tp)
    # for f in finds:
    #     if f not in tps:
    #         fps.append(f)
    return (fps, fns, tps)


# calculates the precision, recall and f_measure considering the numbers
# of false positives, false negatives and true positives given
def score(fps, fns, tps):
    if(tps == 0 and fps == 0 and fns == 0):
        precision = 1
        recall = 1
    elif(tps == 0 and fps == 0):
        precision = 1
        recall = 0
    elif(tps == 0 and fns == 0):
        precision = 0
        recall = 1
    else:
        precision = tps / (tps + fps)
        recall = tps / (tps + fns)
    fm = f_measure(precision, recall)
    return (precision, recall, fm)


# takes an article, its name, the expected matches
#  and the chosen mode of recognition
#  and return the effective matches the number of
# true positives, false negatives and false positives
def evaluate(article, name, expected, classifier, stopwords, mode=3, expr=""):
    (fps, fns, tps) = check(article, expected, classifier, stopwords, mode, expr)
    (precision, recall, fm) = score(len(fps), len(fns), len(tps))
    prec = "{:.2f}".format(precision*100)
    rec = "{:.2f}".format(recall*100)
    fmes = "{:.2f}".format(fm*100)
    res = "Evaluation of the article : " + name + " :\n"
    res += f"\ttrue positives : {json.dumps(tps)} \n"
    res += f"\tfalse positives : {json.dumps(fps)} \n"
    res += f"\tfalse negatives : {json.dumps(fns)} \n"
    res += f"\tprecision = {prec} %\n"
    res += f"\trecall = {rec} %\n"
    res += f"\tF-measure = {fmes} %\n"
    return res, len(tps), len(fns), len(fps)


# prints the results or writes it in the file output if provided
def print_res(output, result):
    if output:
        with open(output, "a") as out:
            out.write(result)
    else:
        print(result)


# list of common things used in each application
# to be able to modify them in one place
stopwords_path = "Experiences/stopwords.txt"
help_stopwords = f"if provided, the path to the stopwords file, else {stopwords_path}"
corpus_path = "Processed_corpus"
expected_results_path = "Experiences/Expected_results_position"
default_mode = 1
help_mode = '''R|\
choose the recognition mode:
    0: Inputed regex
    1: Mm
    2: Mm MM
    3: Mm A
    4: Mm MM A
    5: Mm mm A
    6: Mm MM mm A'''
mode_choices = range(0, 7)
volumes_path = "archives_pretraitees/"
help_regex = "input a regex to be used in the classifier"
default_regex = ""
missing_regex_message = "user chose mode 0 and did not input a regex"


def f_measure(precision, recall):
    if(precision == 0 and recall == 0):
        return -1
    return 2 * precision * recall / (precision + recall)


def match_dist(pattern, word):
    # taux d'erreur de 10 %
    return le.distance(pattern, word) < 1 + len(pattern)//10
