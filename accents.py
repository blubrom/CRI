import re


accent = r"[éèùüûîïêÉÈÙÜÛ]"
with open("results/accents.txt", "w") as out:
    with open("results/classification_archives.txt") as in_:
        for line in in_.readlines():
            if re.search(accent, line):
                out.write(line)
