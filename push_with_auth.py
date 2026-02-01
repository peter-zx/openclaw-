#!/usr/bin/env python3
import subprocess
import os

os.chdir('/Users/admin/Desktop/moltbot')

print("尝试推送到 GitHub...")
print("如果弹出认证窗口，请在 VSCode 中完成登录。")
print("")

# 尝试推送
result = subprocess.run(
    ['git', 'push', '-u', 'origin', 'main'],
    capture_output=True,
    text=True
)

print("标准输出:")
print(result.stdout)
print("\n标准错误:")
print(result.stderr)
print(f"\n返回码: {result.returncode}")

if result.returncode == 0:
    print("\n✅ 推送成功！")
else:
    print("\n❌ 推送失败")
