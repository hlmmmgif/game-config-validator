import csv
import sys
def csv_print(path):
    error_list = []
    try:
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
                        except ValueError:
                            error_list.append(f"行 {index} {col_name}不是数字")
                            continue
                    print(f"行 {index} {col_name} = {repr(val)} {type(val)}")
    except FileNotFoundError:
        print(f"{path}文件不存在")
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
