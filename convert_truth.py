import sys
import os
import re
import json

if __name__ == "__main__":
    sys.path.insert(0, './Experiences/Expected_results')
    import expected_results_vol12 as vol12
    import expected_results_vol83 as vol83
    import expected_results_vol126 as vol126
    old_expected = {12: vol12.expected,
                    83: vol83.expected, 126: vol126.expected}
    with os.scandir("Processed_corpus") as it:
        for entry in it:
            if entry.is_dir():
                expected = {}
                vol_num = int(re.search(r"\d+", entry.name).group(0))
                exp = old_expected[vol_num]
                with os.scandir(entry) as it:
                    for f in it:
                        if f.is_file():
                            page = re.search(
                                r"page_(?P<page>[0-9]+)\.txt", f.name)
                            if page is None:
                                exit(
                                    f"Corpus article : {f.name}  in the wrong format")
                            page = page.group("page")
                            expect = exp[int(page)]
                            new_expected = []
                            with open(f) as article:
                                text = article.read()
                            for i in expect:
                                for m in re.finditer(re.escape(i), text):
                                    r = (m[0], m.span())
                                    if r not in new_expected:
                                        new_expected.append(r)
                            if(len(expect) > len(new_expected)):
                                print(f"Problem {vol_num} {f.name}")
                            if(len(expect) < len(new_expected)):
                                print(f"Rofl {vol_num} {f.name}")
                            expected[int(page)] = new_expected

                with open(f"./Experiences/Expected_results_position/expected_results_vol{vol_num}.py", "w") as out:
                    json.dump(expected, out, sort_keys=True, indent=4)

# \[\s+(".*"),\s+\[\s+(\d+),\s+(\d+)\s+\]\s+\]
