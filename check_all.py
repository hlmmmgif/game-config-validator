import subprocess
import sys

use_llm = "--llm" in sys.argv
args = []

for a in sys.argv[1:]:
    if a != "--llm":
        args.append(a)

if len(args) < 1:
    print("用法：python check_all.py <文件名> [--llm]")
    sys.exit(2)

filename = args[0]

res1 = subprocess.run(
    [sys.executable,"check_config.py",filename],
    capture_output=True,
    text=True,
)
print("=====格式检查=====")
print(res1.stdout)
res2 = subprocess.run(
    [sys.executable,"economy_check.py",filename],
    capture_output=True,
    text=True,
)
print("=====数值检查=====")
print(res2.stdout)

returncode = max(res1.returncode,res2.returncode)
if returncode == 0:
    print("总结果：通过")
else:
    print("总结果：不通过")

if use_llm:
    check_text = res1.stdout + res2.stdout
    print("=====报告=====")
    try:
        from report import make_report
        print(make_report(check_text))
    except Exception as e:
        print(f"报告生成失败{e}:")
sys.exit(returncode)
