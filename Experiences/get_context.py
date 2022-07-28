import re
import os

size = 30


with open("results/classification_conventionnal_binoms.txt") as in_:
    with open("results/classification_conventionnal_binoms_context.txt", "w") as out:
        for line in in_:
            r = re.match(r"(.+) in: ((cnum_4KY28.\d+)_page_\d+.txt)", line)
            with open(os.path.join("archives_pretraitees", r[3], "texts", r[2])) as article:
                s = article.read()
                m = re.search(re.escape(r[1]), s)
                out.write(r[0] + " context: "
                          + s[max(m.start()-size, 0):min(m.end()+size, len(s))] + "\n")
