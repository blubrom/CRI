import os

vol = str(83)
start = 544
starting_page = str(start)
# non inclus
end = 54

for page in range(start, end):
    cmd = f"cat archives_La_Nature/cnum_4KY28.{vol}/texts/cnum_4KY28.{vol}" + \
          f"_page_{format(page, '03d')}.txt >>" + \
          f" Corpus/vol{vol}/page_{starting_page}.txt"
    os.system(cmd)
