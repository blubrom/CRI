ct = 0
nb_words = 50

with open("words_148.txt", "r") as w148:
    with open("words_20.txt", "r") as w20:
        mainw148 = w148.readlines()[:nb_words]
        mainw20 = w20.readlines()[:nb_words]
        for w in mainw148:
            if w in mainw20:
                ct += 1

print(ct)
