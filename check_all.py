import subprocess
import sys

if len(sys.argv) < 2:
    print("用法：python check_all.py <文件名>")
    sys.exit(2)

res1 = subprocess.run(
    [sys.executable,"check_config.py",sys.argv[1]],
    capture_output=True,
    text=True,
)
print("=====格式检查=====")
print(res1.stdout)
res2 = subprocess.run(
    [sys.executable,"economy_check.py",sys.argv[1]],
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
sys.exit(returncode)
