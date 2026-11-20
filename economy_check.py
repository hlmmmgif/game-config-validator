import csv
import sys
import os
from check_config import CheckAbort

def file_dir(path):
    current_dir = os.path.dirname(os.path.abspath(__file__))#os.path.abspath()——》绝对路径，os.path.dirname()——》返回该路径所在的文件夹
    complete_dir = os.path.join(current_dir,path)
    return complete_dir

def values_check():
    values = {}
    complete_dir = file_dir("data/物品价值.csv")
    with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            values[row["物品ID"]] = int(row["价值"])
        return values


def check_economy(path = "data/sheet2.csv"):
    results = []
    try:
        values = values_check()
        complete_dir = file_dir(path)
        with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            print(f"{'物品ID':<8}{'投入成本':<8}{'期望产出':<8}{'收益比':<8}{'判定'}")
            for row in reader:
                try:
                    handling_fee = int(row["分解手续费"])
                    product1_num = int(row["产物1数量"])
                    if handling_fee < 0:
                        raise ValueError
                    input_cost = int(values[row["物品ID"]]) + handling_fee
                    if product1_num < 0:
                        raise ValueError
                    product1_value = int(values[row["分解产物1_ID"]]) * product1_num
                    if row["分解产物2_ID"] == "" or row["分解产物2_ID"] == "0":
                        output_value = product1_value
                    else:
                        product2_num = int(row["产物2数量"])
                        if product2_num < 0:
                            raise ValueError
                        product2_value = int(values[row["分解产物2_ID"]]) * product2_num
                        output_value = product1_value + product2_value
                    try:
                        rate = output_value / input_cost
                    except ZeroDivisionError:
                        print("投入成本为0")
                        continue
                    if rate > 1:
                        result = "可套利"
                    else:
                        result = "正常"
                    results.append(result)
                    print(f"{row['物品ID']:<8}{input_cost:<8}{output_value:<8}{rate:<8.2f}{result}")
                except (ValueError,KeyError):
                    print("数据异常")
                    results.append("数据异常")
    except FileNotFoundError as e:
        raise CheckAbort(f"{os.path.basename(e.filename)}文件不存在",2) from e
    return results

def verdict(results):
    if "可套利" in results or "数据异常" in results:
        return 1
    return 0

if __name__ =="__main__": 
    results = check_economy()
    code = verdict(results)
    print(f"exit = {code}")
    sys.exit(code)





