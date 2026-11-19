import csv
import sys
import logging
import os


def load_legal_ids():
    ids = set()
    current_dir = os.path.dirname(os.path.abspath(__file__))#os.path.abspath()——》绝对路径，os.path.dirname()——》返回该路径所在的文件夹
    complete_dir = os.path.join(current_dir,"data","物品表.csv")
    with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.add(row["物品ID"])
        return ids

def add_error(error_list, row, col, level, reason):
    error_list.append({
        "行": row,
        "列": col,
        "等级": level,
        "问题": reason,
    })

def csv_print(path):
    error_list = []
    check_cols = ["物品ID","分解产物1_ID","分解产物2_ID"]
    try:
        if os.path.getsize(path) == 0:
            print("文件为空")
            sys.exit(2)
        legal_ids = load_legal_ids()
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader, start=2):#行循环
                if row["分解产物2_ID"] in ["","0"] and row["产物2数量"] not in ["","0"]:
                    add_error(error_list,index,"分解产物2_ID","必须改","为空，但是产物2数量不为空")
                for col_name in reader.fieldnames:#列循环
                    if row[col_name] in ["","0"]:
                        if col_name == "分解产物2_ID":
                            continue
                        if col_name == "产物2数量" and row["分解产物2_ID"] in ["","0"]:
                            continue
                        else:
                            add_error(error_list,index,col_name,"建议改","为空")
                            continue
                    try:
                        val = int(row[col_name])
                        if val<0:
                            add_error(error_list,index,col_name,"必须改","为负数")
                            continue
                        if col_name in check_cols:
                            if str(val) not in legal_ids:
                                add_error(error_list,index,col_name,"必须改",f"引用了不存在的物品ID:{val}")
                                continue
                    except ValueError:
                        add_error(error_list,index,col_name,"必须改","不是数字")
                        continue
                logging.debug(f"行 {index} {col_name} = {repr(val)} {type(val)}")
            if reader.line_num == 1:
                print("文件只有表头")
                sys.exit(1)
    except FileNotFoundError as e:
        print(f"{os.path.basename(e.filename)}文件不存在")
        sys.exit(2)
    return error_list

if __name__ == "__main__":
    json_out = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]
    if len(args) < 2:
        print("用法：python check_config.py <文件名>")
        sys.exit(2)
    else:
        error_list = csv_print(args[0])
        if json_out:
            import json
            print(json.dumps(error_list,ensure_ascii=False))
        else:
            lines = [f"行 {e['行']} {e['列']}{e['问题']}" for e in error_list]
            print(lines)
            print(f"发现{len(error_list)}个错误")
        if len(error_list) > 0:
            sys.exit(1)
