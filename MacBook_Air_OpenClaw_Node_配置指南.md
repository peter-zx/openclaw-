# MacBook Air OpenClaw Node 配置指南

## 🎯 文档概述

### 一、这是什么？
本文档详细指导如何将 **MacBook Air** 配置为 OpenClaw 的本地节点，实现云端 AI 助手对 Mac 设备的远程控制。通过此配置，你可以从云服务器安全地操控 MacBook Air 执行文件操作、浏览器控制、应用启动等任务。

### 二、为什么需要这个配置？
1. **跨设备协同**：让云端的 AI 助手拥有"手和眼"，能够操作本地设备
2. **自动化任务**：远程执行重复性工作，如文件整理、数据收集等
3. **安全连接**：通过加密隧道建立安全的远程控制通道
4. **平台兼容性**：macOS 是 OpenClaw Node 最稳定、最兼容的平台之一

### 三、工作原理
1. **本地节点**：在 MacBook Air 上运行 `openclaw-node` 服务
2. **云端控制端**：在云服务器上运行 OpenClaw 网关
3. **配对连接**：通过配对码建立安全连接
4. **网络通道**：通过 Tailscale 或 SSH 隧道实现网络互通
5. **权限控制**：按需授权访问权限，确保系统安全

---

## 📋 准备工作

### 一、硬件需求
| 设备 | 要求 | 说明 |
|------|------|------|
| **MacBook Air** | macOS 10.15+ | 作为本地节点设备 |
| **云服务器** | Linux 系统 | 运行 OpenClaw 网关 |
| **网络** | 稳定的互联网连接 | 两端设备都能上网 |

### 二、软件准备
#### MacBook Air 端：
- ✅ **Homebrew** - macOS 包管理器
- ✅ **Node.js v22+** - 运行环境
- ✅ **OpenClaw Node CLI** - 节点程序
- ✅ **Tailscale** (推荐) - 虚拟专用网络

#### 云服务器端：
- ✅ **Node.js v22+** - 运行环境
- ✅ **OpenClaw CLI** - 主程序
- ✅ **Tailscale** (推荐) - 虚拟专用网络

### 三、账户与凭证
1. **GitHub 账户** (已登录 VS Code)
2. **Tailscale 账户** (免费版即可)
3. **云服务器访问权限** (SSH 密钥/密码)

---

## 🍎 MacBook Air 配置步骤

### ✅ 阶段一：安装必备工具

#### 1. 安装 Homebrew（包管理器）
```bash
# 打开终端，粘贴以下命令：
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装完成后重启终端，运行：
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证安装
brew --version
```

#### 2. 安装 Node.js v22+
```bash
# 使用 Homebrew 安装 Node.js
brew install node@22

# 添加到 PATH 环境变量
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证安装
node --version  # 应显示 v22.x
npm --version   # 应显示 10.x+
```

#### 3. 安装 OpenClaw Node CLI
```bash
# 全局安装 OpenClaw Node
npm install -g openclaw-node@latest

# 验证安装
openclaw-node --version
```

### ✅ 阶段二：启动本地节点

#### 1. 创建专用工作目录
```bash
# 创建一个专门的目录用于节点管理
mkdir -p ~/openclaw-node
cd ~/openclaw-node

# 初始化节点配置
openclaw-node init --name "MacBook-Air" --tags "mac,personal,work"
```

#### 2. 启动节点服务
```bash
# 启动节点（保持终端运行）
openclaw-node start
```

首次启动会显示类似信息：
```
🖥️ Node ID: mac-abc123-xyz789
🔑 Pairing code: ABC-123-XYZ
📡 Waiting for approval from gateway...
```

**重要**：记下 **Pairing code**（配对码），如 `ABC-123-XYZ`，用于后续云端配对。

#### 3. 后台运行选项（可选）
```bash
# 使用 tmux 保持节点后台运行
brew install tmux
tmux new -s openclaw-node
openclaw-node start
# 按 Ctrl+B, 然后按 D 退出 tmux，节点继续运行
# 重新连接：tmux attach -t openclaw-node
```

---

## ☁️ 云服务器配置步骤

### ✅ 阶段一：安装 OpenClaw

#### 1. 检查 Node.js 环境
```bash
# 验证 Node.js 版本
node --version
npm --version

# 如未安装，使用对应包管理器安装
# Ubuntu/Debian: apt install nodejs npm
# CentOS/RHEL: yum install nodejs npm
```

#### 2. 安装 OpenClaw CLI
```bash
# 全局安装 OpenClaw
npm install -g openclaw@latest

# 验证安装
openclaw --version
```

#### 3. 启动网关服务
```bash
# 启动网关（前台运行，测试用）
openclaw gateway start

# 或后台运行
nohup openclaw gateway start > /tmp/openclaw.log 2>&1 &
```

### ✅ 阶段二：配对 Mac 节点

#### 1. 列出待配对节点
```bash
# 查看可配对的节点
openclaw nodes list
```

#### 2. 批准配对
```bash
# 使用 Mac 上获取的配对码
openclaw nodes approve ABC-123-XYZ

# 成功响应：
# ✅ Node 'MacBook-Air' paired successfully. Status: online
```

#### 3. 验证配对状态
```bash
# 查看所有已配对节点
openclaw nodes list

# 查看节点详情
openclaw nodes describe MacBook-Air
```

---

## 🔗 网络连接配置（关键步骤）

### 🛡️ 方案一：Tailscale（推荐，最安全简单）

#### 1. 在 MacBook Air 上安装 Tailscale
```bash
# 安装 Tailscale
brew install tailscale

# 启动并登录
tailscale up
# 会打开浏览器进行登录，使用你的账户
```

#### 2. 在云服务器上安装 Tailscale
```bash
# Ubuntu/Debian 系统：
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# CentOS/RHEL 系统：
sudo yum install yum-utils
sudo yum-config-manager --add-repo https://pkgs.tailscale.com/stable/centos/7/tailscale.repo
sudo yum install tailscale
sudo systemctl enable --now tailscaled
tailscale up
```

#### 3. 获取 Tailscale IP 地址
```bash
# 在 Mac 上获取 IP
tailscale ip -4  # 例如：100.64.0.1

# 在云服务器上获取 IP
tailscale ip -4  # 例如：100.64.0.2
```

#### 4. 配置 OpenClaw 使用 Tailscale
```bash
# 在云服务器上编辑 OpenClaw 配置
nano ~/.openclaw/openclaw.json
```

添加以下配置：
```json
{
  "gateway": {
    "tailscale": {
      "mode": "enabled",
      "enableIngress": false,
      "resetOnExit": false
    }
  }
}
```

重启网关服务：
```bash
openclaw gateway restart
```

### 🌐 方案二：SSH 反向隧道（备用方案）

如果你有云服务器的公网 IP：

```bash
# 在 MacBook Air 上创建 SSH 反向隧道（保持运行）
ssh -N -R 8080:localhost:8080 user@your-server-ip

# 在云服务器上更新节点地址
openclaw nodes update MacBook-Air --address "http://localhost:8080"
```

---

## 📱 权限授权配置

在云服务器上执行以下命令，为 Mac 节点授权相应权限：

### 1. 基础文件系统权限
```bash
# 允许读取和写入文件系统
openclaw nodes run MacBook-Air -- command="openclaw-node permissions add filesystem read-write"
```

### 2. 浏览器控制权限
```bash
# 允许控制 Safari/Chrome 浏览器
openclaw nodes run MacBookAir -- command="openclaw-node permissions add browser control"
```

### 3. 应用程序启动权限
```bash
# 允许启动应用程序
openclaw nodes run MacBook-Air -- command="openclaw-node permissions add apps launch"
```

### 4. 系统通知权限
```bash
# 允许发送系统通知
openclaw nodes run MacBook-Air -- command="openclaw-node permissions add notification send"
```

### 5. 邮件客户端权限（可选）
```bash
# 允许访问邮件客户端
openclaw nodes run MacBook-Air -- command="openclaw-node permissions add email access"
```

---

## 🧪 连接测试与验证

### 1. 基础连接测试
```bash
# 查看节点详细信息
openclaw nodes describe MacBook-Air

# 运行简单命令测试
openclaw nodes run MacBook-Air -- command="pwd"

# 获取系统信息
openclaw nodes run MacBook-Air -- command="uname -a"
```

### 2. 文件操作测试
```bash
# 查看家目录文件
openclaw nodes run MacBook-Air -- command="ls -la ~/"

# 查看文档目录
openclaw nodes run MacBook-Air -- command="ls -la ~/Documents"

# 创建测试文件
openclaw nodes run MacBook-Air -- command="echo '测试内容' > ~/Desktop/test.txt"

# 查看文件内容
openclaw nodes run MacBook-Air -- command="cat ~/Desktop/test.txt"
```

### 3. 高级功能测试
```bash
# 获取系统负载信息
openclaw nodes run MacBook-Air -- command="uptime"

# 查看磁盘使用情况
openclaw nodes run MacBook-Air -- command="df -h"

# 查看网络连接
openclaw nodes run MacBook-Air -- command="ifconfig | grep inet"
```

---

## 🛠️ Mac 专有能力配置

### 安装 macOS 特有插件
```bash
# 在 MacBook Air 上运行
openclaw-node plugins install @openclaw/macos-tools
```

### 插件提供的功能
| 功能 | 命令示例 | 说明 |
|------|----------|------|
| **浏览器控制** | `macos/open-browser` | 打开/控制 Safari/Chrome |
| **日历读取** | `macos/read-calendar` | 读取 iCal 日程 |
| **系统通知** | `macos/send-notification` | 发送系统通知 |
| **屏幕截图** | `macos/capture-screen` | 截取屏幕 |
| **通讯录读取** | `macos/read-contacts` | 读取通讯录信息 |
| **AppleScript** | `macos/run-applescript` | 执行 AppleScript 自动化 |

### 实际用例示例
```bash
# 用例1：查看未来3天的日程
openclaw nodes run MacBook-Air -- script="macos/read-calendar" -- args='{"days": 3}'

# 用例2：在浏览器中打开网页
openclaw nodes run MacBook-Air -- script="macos/open-browser" -- args='{"url": "https://12306.cn"}'

# 用例3：打开邮件客户端
openclaw nodes run MacBook-Air -- script="macos/open-app" -- args='{"app": "Mail"}'
```

---

## 🚨 安全配置（必须执行）

### 一、MacBook Air 端安全配置
```bash
# 1. 创建命令白名单
openclaw-node config set security.allowedCommands ["ls", "pwd", "open", "screencapture", "cat", "echo"]

# 2. 限制文件访问范围
openclaw-node config set security.allowedPaths ["~/Documents", "~/Downloads", "~/Desktop", "~/openclaw-node"]

# 3. 启用详细日志
openclaw-node config set logging.level "info"

# 4. 设置会话超时（单位：毫秒）
openclaw-node config set security.sessionTimeout 3600000  # 1小时
```

### 二、云服务器端安全配置
编辑 `~/.openclaw/openclaw.json` 添加：
```json
{
  "security": {
    "remoteAccess": {
      "requireAuth": true,
      "allowedCommands": ["filesystem.read", "browser.open", "apps.launch"],
      "maxExecutionTime": 30000,
      "requireApproval": true
    },
    "audit": {
      "enabled": true,
      "logLevel": "info"
    }
  }
}
```

### 三、最佳安全实践
1. **定期更新**：保持 Node.js 和 OpenClaw 为最新版本
2. **最小权限**：只授予必要的操作权限
3. **网络隔离**：使用 Tailscale 等 VPN 隔离网络
4. **日志监控**：定期检查操作日志
5. **定期审查**：定期审查授权配置

---

## 📝 故障排除指南

### 常见问题及解决方法

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| **配对失败** | 网络不通、配对码错误 | 1. 检查两端网络连接<br>2. 确认配对码正确<br>3. 重启节点服务 |
| **连接超时** | 防火墙阻挡、端口未开 | 1. 检查防火墙设置<br>2. 确认 Tailscale 连接正常<br>3. 尝试 SSH 隧道方案 |
| **权限被拒** | 未授权相应权限 | 1. 重新执行权限授权命令<br>2. 检查安全配置白名单 |
| **节点离线** | 节点服务停止 | 1. 在 Mac 上重启节点服务<br>2. 检查进程状态：`ps aux \| grep openclaw-node` |
| **命令执行失败** | 命令不在白名单中 | 1. 添加到安全配置白名单<br>2. 检查命令语法正确性 |

### 诊断命令
```bash
# 1. 检查节点状态
openclaw nodes status

# 2. 查看网关日志
tail -f /tmp/openclaw.log

# 3. 测试网络连通性
ping <对方设备IP>

# 4. 检查 Tailscale 状态
tailscale status

# 5. 验证 Node.js 环境
node --version
npm list -g | grep openclaw
```

---

## 📌 快速检查清单

### 安装前检查
- [ ] MacBook Air 运行 macOS 10.15+
- [ ] 云服务器已安装 Linux 系统
- [ ] 两端设备都能访问互联网
- [ ] GitHub 账户已登录 VS Code

### MacBook Air 配置检查
- [ ] Homebrew 安装成功
- [ ] Node.js v22+ 安装成功
- [ ] OpenClaw Node CLI 安装成功
- [ ] 节点成功启动并获得配对码
- [ ] Tailscale 安装并登录

### 云服务器配置检查
- [ ] Node.js v22+ 安装成功
- [ ] OpenClaw CLI 安装成功
- [ ] 网关服务正常启动
- [ ] Tailscale 安装并登录

### 连接与测试检查
- [ ] 成功配对节点
- [ ] 网络连接正常（Tailscale 或隧道）
- [ ] 权限授权完成
- [ ] 基础命令测试通过
- [ ] 安全配置已设置

---

## 🔄 日常维护指南

### 1. 启动/停止节点
```bash
# 启动节点
openclaw-node start

# 停止节点
openclaw-node stop

# 重启节点
openclaw-node restart
```

### 2. 查看节点状态
```bash
# 查看节点信息
openclaw-node status

# 查看运行日志
openclaw-node logs

# 查看系统资源占用
openclaw-node stats
```

### 3. 更新软件
```bash
# 更新 Node.js（通过 Homebrew）
brew upgrade node@22

# 更新 OpenClaw Node
npm update -g openclaw-node

# 更新 Tailscale
brew upgrade tailscale
```

### 4. 备份与恢复
```bash
# 备份配置文件
cp -r ~/.openclaw-node ~/openclaw-node-backup/

# 恢复配置文件
cp -r ~/openclaw-node-backup/ ~/.openclaw-node/
```

---

## 📚 延伸学习资源

### 官方文档
- [OpenClaw 官方文档](https://docs.openclaw.dev)
- [OpenClaw Node GitHub](https://github.com/openclaw/openclaw-node)
- [Tailscale 文档](https://tailscale.com/kb/)

### 相关工具
- **Homebrew**：macOS 包管理器
- **Node.js**：JavaScript 运行环境
- **Tailscale**：零配置 VPN
- **tmux**：终端复用器

### 进阶主题
1. **自动化脚本编写**：使用 OpenClaw Node API
2. **自定义插件开发**：扩展节点功能
3. **多节点管理**：同时控制多个设备
4. **安全加固**：高级安全配置技巧

---

**文档版本**：v1.0  
**更新日期**：2026年2月1日  
**适用系统**：macOS 10.15+，Linux 服务器  
**文档目的**：提供完整的 MacBook Air OpenClaw Node 配置指南

> 💡 **提示**：建议按照步骤顺序操作，每完成一个阶段后进行验证测试，确保每一步都正确无误后再继续下一步。如遇到问题，参考故障排除章节或查看相关日志。