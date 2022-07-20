import random as rd
import re

size = 27805
index_list = sorted([rd.randint(0, size) for _ in range(5 * size//100)])

with open("results/sondage(1).txt", "w") as out:
    with open("results/classification_conventionnal_binoms_sorted.txt") as in_:
        ct = 0
        for line in in_.readlines():
            if ct in index_list:
                out.write(line)
            ct += 1
