"""设置Windows定时任务：每天早上8:05自动更新APEC看板"""
import subprocess

bat_path = r"C:\Users\Lenovo\Desktop\更新APEC动态.bat"
cmd = [
    "schtasks",
    "/create",
    "/tn", "APEC动态追踪",
    "/tr", bat_path,
    "/sc", "daily",
    "/st", "08:05",
    "/f",
]
result = subprocess.run(cmd, capture_output=True, text=True, encoding="gbk")
print(result.stdout or "OK")
if result.returncode != 0:
    print(result.stderr)
