import csv
import sys
import os
def file_dir(path):
    current_dir = os.path.dirname(os.path.abspath(__file__))#os.path.abspath()——》绝对路径，os.path.dirname()——》返回该路径所在的文件夹
    complete_dir = os.path.join(current_dir,path)
    return complete_dir
def item_ids():
    ids = set()
    complete_dir = file_dir("物品表.csv")
    with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.add(row["物品ID"])
        return ids

def values_check():
    values = {}
    complete_dir = file_dir("物品价值.csv")
    with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            values[row["物品ID"]] = int(row["价值"])
        return values


def check_economy():
    values = values_check()
    complete_dir = file_dir("sheet2.csv")
    with open(complete_dir, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        print(f"{'物品ID':<8}{'投入成本':<8}{'期望产出':<8}{'收益比':<8}{'判定'}")
        for row in reader:
            input_cost = int(values[row["物品ID"]]) + int(row["分解手续费"])
            product1_value = int(values[row["分解产物1_ID"]]) * int(row["产物1数量"])
            if row["分解产物2_ID"] == "" or row["分解产物2_ID"] == "0":
                output_value = product1_value
            elif row["分解产物2_ID"] not in values:
                output_value = product1_value
                print(f"{row['物品ID']:<8}{input_cost:<8}{output_value:<8}无效 数据不全")
                continue
            else:
                product2_value = int(values[row["分解产物2_ID"]]) * int(row["产物2数量"])
                output_value = product1_value + product2_value
            try:
                rate = output_value / input_cost
            except ZeroDivisionError:
                print("投入成本为0")
                continue
            if rate > 1:
                result = "可套利"
                print(f"{row['物品ID']:<8}{input_cost:<8}{output_value:<8}{rate:<8.2f}{result}")
            else:
                result = "正常"
                print(f"{row['物品ID']:<8}{input_cost:<8}{output_value:<8}{rate:<8.2f}{result}")
check_economy()            
            




