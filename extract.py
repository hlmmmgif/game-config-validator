from check_config import CheckAbort
import os
import csv
import sys

def input_check(path="data/sheet2.csv"):
    try:
        if os.path.getsize(path) == 0:
            raise CheckAbort("文件为空",2)
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
    except FileNotFoundError as e:
            raise CheckAbort(f"{os.path.basename(e.filename)}文件不存在",2) from e 
    return header


def load_name_to_id(path="data/物品表.csv"):
    name_ID = {}
    posttion = []
    try:
        if os.path.getsize(path) == 0:
            raise CheckAbort("文件为空",2)
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name_ID[row["物品名"]] = row["物品ID"]
    except FileNotFoundError as e:
        raise CheckAbort(f"{os.path.basename(e.filename)}文件不存在",2) from e 
    if name in name_ID.keys():
        pos = sentence.find()
        r = {pos:item}
        posttion.append(r)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sentence = "".join(args)

def parse_sentence(sentence):
     
