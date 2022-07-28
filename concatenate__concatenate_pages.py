import regex as re
import os

with open("Experiences/Expected_results/expected_results_vol155.py") as ex:
	s = "".join(ex) 
	print(s)
	for i in re.finditer(r"\D(\d+):.*?(\d+):", s, overlapped=True, flags=re.DOTALL):
		os.system(f"python3 Experiences/concatenate_pages.py {i[1]} {i[2]}")
		print(i[1], i[2])
		
