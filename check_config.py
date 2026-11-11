import csv
import sys
import logging
import os

def load_legal_ids():
    ids = set()
    current_dir = os.path.dirname(os.path.abspath(__file__))#os.path.abspath()——》绝对路径，os.path.dirname()——》返回该路径所在的文件夹
    complete_dir = os.path.join(current_dir,"物品表.csv")
    with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.add(row["物品ID"])
        return ids

def csv_print(path):
    error_list = []
    check_cols = ["物品ID","分解产物1_ID","分解产物2_ID"]
    try:
        legal_ids = load_legal_ids()
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader, start=2):
                for col_name in reader.fieldnames:
                    if row[col_name] == "":
                        error_list.append(f"行 {index} {col_name} 为空")
                        continue
                    else:
                        try:
                            val = int(row[col_name])
                            if val<0:
                                error_list.append(f"行 {index} {col_name}为负数")
                                continue
                            if col_name in check_cols:
                                if str(val) not in legal_ids:
                                    error_list.append(f"行 {index} {col_name}引用了不存在的物品ID:{val}")
                                    continue
                        except ValueError:
                            error_list.append(f"行 {index} {col_name}不是数字")
                            continue
                    logging.debug(f"行 {index} {col_name} = {repr(val)} {type(val)}")
    except FileNotFoundError as e:
        print(f"{os.path.basename(e.filename)}文件不存在")
        sys.exit(2)
    return error_list

if len(sys.argv) < 2:
    print("用法：python check_config.py <文件名>")
    sys.exit(2)
else:
    error_list = csv_print(sys.argv[1])
    print(error_list)
    print(f"发现{len(error_list)}个错误")
    if len(error_list) > 0:
        sys.exit(1)
