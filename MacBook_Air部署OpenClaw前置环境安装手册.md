# MacBook Air 部署 OpenClaw 前置环境（Homebrew/Git/Node.js）安装手册

## 📚 目录

1. [文档说明](#文档说明)
2. [准备工作](#准备工作)
3. [核心安装步骤](#核心安装步骤)
4. [避坑指南](#避坑指南)
5. [验证步骤](#验证步骤)
6. [完整指令合集](#完整指令合集)
7. [文件保存方法](#文件保存方法)
8. [总结](#总结)

---

## 文档说明

本手册汇总 MacBook Air（macOS 13+）下 OpenClaw 本地节点所需基础环境（Homebrew/Git/Node.js）的完整安装、更新、避坑步骤，适配国内网络，避免重复踩错，可直接复制指令执行。

---

## 准备工作

### 设备要求

- **设备**：MacBook Air（Apple Silicon/M1/M2/M3 芯片）
- **系统**：macOS 13.0 或更高版本
- **权限**：拥有 Mac 管理员权限（可输入开机密码）
- **网络**：可访问外网（已配置国内镜像加速）
- **工具**：系统自带「终端」（启动台→其他→终端）

### 检查系统版本

```bash
# 查看系统版本
sw_vers

# 查看芯片架构
uname -m
```

**预期结果**：
```
ProductName:    macOS
ProductVersion: 13.x.x / 14.x.x / 15.x.x
BuildVersion:   xxxxx

arm64  # Apple Silicon 芯片
```

---

## 核心安装步骤

### 步骤 1：安装并配置 Homebrew（国内镜像加速）

#### 1.1 基础安装

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**安装过程中**：
- 系统会提示输入密码，输入您的 Mac 登录密码（输入时不会显示字符）
- 按 `Enter` 键确认安装
- 等待 5-10 分钟（取决于网络速度）

---

#### 1.2 配置路径（解决 brew: command not found）

```bash
# 临时添加到 PATH
export PATH="/opt/homebrew/bin:$PATH"

# 永久添加到 PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 验证安装
brew --version
```

**预期结果**：
```
Homebrew 4.x.x
```

✅ 如果看到版本号，说明 Homebrew 安装成功。

---

#### 1.3 配置国内镜像（中科大源，解决下载慢）

```bash
# 配置 Homebrew 镜像
git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git

# 配置 Homebrew Bottles 镜像
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

---

#### 1.4 强制更新（跳过无关提示）

```bash
# 强制更新 Homebrew
brew update --force --quiet
```

---

#### 1.5 权限修复（若遇权限错误）

```bash
# 修复 Homebrew 目录权限
sudo chown -R $(whoami) /opt/homebrew

# 验证权限
ls -la /opt/homebrew
```

---

### 步骤 2：安装新版 Git（替换系统自带旧版）

#### 2.1 跳过自动更新，快速安装 Git

```bash
# 跳过自动更新，快速安装
HOMEBREW_NO_AUTO_UPDATE=1 brew install git
```

---

#### 2.2 验证新版 Git

```bash
# 验证新版 Git（需输出 ≥2.45 版本）
/opt/homebrew/bin/git --version
```

**预期结果**：
```
git version 2.45.x 或更高
```

✅ 如果看到版本号 ≥2.45，说明新版 Git 安装成功。

---

#### 2.3 配置 Git 全局信息

```bash
# 配置 Git 用户名（替换为你的名字）
git config --global user.name "你的名字"

# 配置 Git 邮箱（替换为你的邮箱）
git config --global user.email "你的邮箱@xxx.com"

# 验证配置
git config --global --list
```

**预期结果**：
```
user.name=你的名字
user.email=你的邮箱@xxx.com
```

---

### 步骤 3：安装 Node.js v22（OpenClaw Node 核心依赖）

#### 3.1 安装 Node.js v22

```bash
# 安装 Node.js 22
HOMEBREW_NO_AUTO_UPDATE=1 brew install node@22
```

**预计时间**：5-10 分钟（取决于网络速度）

---

#### 3.2 配置 Node.js 路径（永久生效）

```bash
# 添加 Node.js 到 PATH
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

---

#### 3.3 验证版本

```bash
# 验证 Node.js 版本（需 ≥v22）
node --version

# 验证 npm 版本（需 ≥v10）
npm --version
```

**预期结果**：
```
v22.x.x
10.x.x
```

✅ 如果看到版本号符合要求，说明 Node.js 安装成功。

---

## 避坑指南

### 常见问题与解决方案

| 常见问题 | 原因 | 解决方案 |
|---------|------|---------|
| `brew: command not found` | 路径未加载 | 执行 `export PATH="/opt/homebrew/bin:$PATH"` + 写入 `~/.zshrc` |
| Git 版本显示 2.39.x | 系统自带旧版未被替换 | 用 `/opt/homebrew/bin/git --version` 验证，而非直接 `git --version` |
| `brew update` 卡顿 / 超时 | 官方源国内访问慢 | 配置中科大镜像（步骤 1.3）+ 用 `brew update --force --quiet` 强制更新 |
| macOS 13 版本警告 | 系统版本较旧，Homebrew 提示 | 忽略即可，不影响功能使用 |
| 权限错误（Permission denied） | 目录归属非当前用户 | 执行 `sudo chown -R $(whoami) /opt/homebrew` |

---

### 问题 1：brew: command not found

**症状**：执行 `brew` 命令提示找不到命令

**解决方案**：

```bash
# 临时添加到 PATH
export PATH="/opt/homebrew/bin:$PATH"

# 验证
brew --version

# 永久添加到 PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

---

### 问题 2：Git 版本显示旧版

**症状**：执行 `git --version` 显示 2.39.x（系统自带旧版）

**解决方案**：

```bash
# 使用新版 Git 验证
/opt/homebrew/bin/git --version

# 如果新版 Git 存在，可以创建别名
echo 'alias git="/opt/homebrew/bin/git"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 验证
git --version
```

---

### 问题 3：brew update 卡顿

**症状**：执行 `brew update` 卡住或超时

**解决方案**：

```bash
# 配置国内镜像
git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git

# 强制更新
brew update --force --quiet
```

---

### 问题 4：权限错误

**症状**：执行 `brew install` 时提示 `Permission denied`

**解决方案**：

```bash
# 修复 Homebrew 目录权限
sudo chown -R $(whoami) /opt/homebrew

# 验证权限
ls -la /opt/homebrew
```

---

## 验证步骤

### 确认环境安装成功

```bash
# 1. 验证 Homebrew
brew --version

# 2. 验证 Git（新版）
/opt/homebrew/bin/git --version

# 3. 验证 Node.js/npm
node --version
npm --version
```

**预期结果**：
```
Homebrew 4.x.x
git version 2.45.x
v22.x.x
10.x.x
```

✅ 如果所有版本号都符合要求，说明环境配置成功！

---

## 完整指令合集

### 一键复制执行（推荐）

```bash
# 全量指令：Homebrew + Git + Node.js 完整配置

# 1. 配置 Homebrew 路径
export PATH="/opt/homebrew/bin:$PATH"
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 2. 配置国内镜像
git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc

# 3. 强制更新 Homebrew
brew update --force --quiet

# 4. 修复权限
sudo chown -R $(whoami) /opt/homebrew

# 5. 安装 Git
HOMEBREW_NO_AUTO_UPDATE=1 brew install git

# 6. 验证 Git
/opt/homebrew/bin/git --version

# 7. 配置 Git（替换为你的信息）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@xxx.com"

# 8. 安装 Node.js
HOMEBREW_NO_AUTO_UPDATE=1 brew install node@22

# 9. 配置 Node.js 路径
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 10. 验证 Node.js/npm
node --version
npm --version
```

---

## 文件保存方法

### 下载使用

1. 打开 Mac 「文本编辑」软件
2. 复制本手册所有内容
3. 粘贴到文本编辑中
4. 点击「文件」→「存储」
5. 命名为「Mac OpenClaw 环境安装手册.md」
6. 存储格式选择「纯文本」
7. 保存到桌面 / 常用目录

后续可随时打开复制指令。

---

## 总结

### 核心逻辑

1. **先配置 Homebrew 国内镜像**，再安装 Git/Node.js，避免网络 / 权限问题
2. **关键避坑**：新版 Homebrew 无需手动 tap homebrew/core，用 `HOMEBREW_NO_AUTO_UPDATE=1` 跳过自动更新加速安装
3. **验证标准**：所有验证指令能输出版本号，即环境配置成功，可继续安装 OpenClaw Node

---

### 快速命令参考

```bash
# 验证 Homebrew
brew --version

# 验证 Git
/opt/homebrew/bin/git --version

# 验证 Node.js
node --version
npm --version

# 重新加载配置
source ~/.zshrc
```

---

### 下一步

环境配置完成后，可以继续：

1. ✅ 安装 OpenClaw Node
2. ✅ 配置本地节点
3. ✅ 连接云端服务器
4. ✅ 测试跨设备协作

---

**文档版本**: 1.0
**最后更新**: 2026-02-02
**适用版本**: macOS 13.0+, Homebrew 4.x+, Node.js v22+

---

祝您安装顺利！如有任何问题，欢迎随时咨询。🚀
