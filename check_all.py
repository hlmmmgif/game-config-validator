import sys
import io,contextlib
from check_config import csv_print,CheckAbort,format_errors,format_for_ai
from economy_check import check_economy, verdict

def main():
    use_llm = "--llm" in sys.argv
    args = []

    for a in sys.argv[1:]:
        if a != "--llm":
            args.append(a)

    if len(args) < 1:
        print("用法：python check_all.py <文件名> [--llm]")
        return 2
    
    try:
        filename = args[0]
        error_list = csv_print(filename)
        print("=====格式检查=====")
        print(format_errors(error_list))#列表变为文字
        print(f"发现{len(error_list)}个错误")
    except CheckAbort as e:
        print(e)
        return e.code

    print("=====数值检查=====")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        results = check_economy(filename)
    print(buf.getvalue(),end="")

    returncode = max(1 if error_list else 0,verdict(results))#格式退出码

    if returncode == 0:
        print("总结果：通过")
    else:
        print("总结果：不通过")

    if use_llm:
        print("=====报告=====")
        try:
            value_check = len(results)
            value_error = results.count('数据异常')
            profit_count = results.count('可套利')    
            if '可套利' in results or '数据异常' in results:
                tag = "【必须改】"
            else:
                tag = "【建议改】"
            check_text = (
                "\n".join(format_for_ai(error_list)) 
                + f"\n{tag} 数值检查共{value_check}行，数据异常{value_error}行，可套利{profit_count}行\n" 
                + buf.getvalue()
            )
            from report import make_report
            print(make_report(check_text))
        except Exception as e:
            print(f"报告生成失败:{e}")
    return returncode

if __name__ == "__main__":
    sys.exit(main())
