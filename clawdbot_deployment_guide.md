# Clawdbot 部署指南

本文档提供在本地或服务器上部署 Clawdbot 的完整教程。Clawdbot 是一个支持多模型、多频道的 AI 助手平台，可以集成飞书、钉钉等办公应用。

## 目录

- [准备工作](#准备工作)
- [快速开始（本地测试）](#快速开始本地测试)
- [服务器部署](#服务器部署)
- [配置自定义模型（阿里百炼示例）](#配置自定义模型阿里百炼示例)
- [配置飞书频道](#配置飞书频道)
- [常用命令速查](#常用命令速查)
- [进程管理与持久化](#进程管理与持久化)
- [测试与验证](#测试与验证)
- [故障排除](#故障排除)

## 准备工作

### 1. 系统要求

- **Node.js** ≥ 24.0.0（推荐 24+）
- **npm** 或 **pnpm**（推荐使用 nvm 管理 Node.js 版本）
- **Python 3**（可选，用于脚本配置）
- 至少 1GB 可用内存
- 开放端口（默认 18789）

### 2. 环境配置

#### 本地电脑环境配置

在开始部署前，请确保本地电脑已安装以下软件：

1. **Node.js 24+**：
   ```bash
   # 使用 nvm（推荐）
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   source ~/.bashrc  # 或 ~/.zshrc（根据你的 shell）
   nvm install 24
   nvm use 24
   
   # 验证安装
   node --version  # 应显示 v24.x.x
   npm --version   # 应显示 10.x.x+
   ```

2. **Python 3**（用于脚本配置）：
   ```bash
   # macOS
   brew install python@3
   
   # Ubuntu/Debian
   sudo apt install python3 python3-pip
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   ```

3. **Git**（可选，用于克隆仓库）：
   ```bash
   # macOS
   brew install git
   
   # Ubuntu/Debian
   sudo apt install git
   
   # CentOS/RHEL
   sudo yum install git
   ```

#### 新服务器环境配置

如果是全新服务器，请按顺序执行以下环境准备：

```bash
# 1. 系统更新
apt update && apt upgrade -y  # Debian/Ubuntu
# 或
yum update -y                 # CentOS/RHEL

# 2. 安装基础工具
apt install -y curl wget git python3 python3-pip  # Debian/Ubuntu
# 或
yum install -y curl wget git python3 python3-pip  # CentOS/RHEL

# 3. 安装 Node.js 24+（使用 nvm）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24

# 4. 验证环境
node --version  # 应为 v24.x.x
npm --version   # 应为 10.x.x+
python3 --version  # 应为 3.8+
```

**重要提示**：只有在完成上述环境配置后，才能继续安装和配置 Clawdbot。

### 3. 获取 API 密钥

根据你计划使用的模型，提前准备好相应的 API 密钥：

- **阿里百炼**（免费模型）：在 [阿里云百炼平台](https://dashscope.aliyun.com/) 申请 API Key
- **OpenAI**：在 [OpenAI Platform](https://platform.openai.com/) 获取 API Key
- **其他模型**：根据 provider 要求准备

### 4. 创建飞书应用（如需集成）

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`
4. 配置权限和事件订阅（需要回调 URL）

## 快速开始（本地测试）

> **重要提醒**：在开始本节前，请确保已完成 [准备工作](#准备工作) 中的环境配置，特别是 Node.js 24+ 的安装。新服务器必须先配置环境才能使用 Clawdbot。

### 1. 安装 Clawdbot

Clawdbot 可以通过 npm 全局安装：

```bash
# 使用 npm
npm install -g clawdbot

# 或使用 npx（无需安装）
npx clawdbot --help
```

验证安装：

```bash
clawdbot --version
# 应输出类似：2026.1.24-3
```

### 2. 初始配置

运行交互式配置向导：

```bash
clawdbot configure
```

按照提示设置：
- **工作目录**：存放会话和数据的路径（如 `~/clawd`）
- **网关模式**：选择 `local`（本地运行）
- **端口**：默认 18789
- **模型提供商**：初次可选择 `OpenAI` 或跳过

### 3. 启动网关

```bash
# 前台运行（查看日志）
clawdbot gateway --local --port 18789 --verbose

# 后台运行
nohup clawdbot gateway --port 18789 --verbose &
```

### 4. 测试 Agent

```bash
# 设置环境变量（如果使用 OpenAI）
export OPENAI_API_KEY=your_key_here

# 发送测试消息
clawdbot agent --agent main --message "你好" --local
```

如果一切正常，你将看到 AI 的回复。

## 服务器部署

本节适用于在新服务器上部署生产环境。**重要**：新服务器必须先完成环境配置才能使用 Clawdbot。如果你已经通过 [准备工作](#准备工作) 完成了环境配置，可以跳过步骤1。

### 1. 服务器准备

```bash
# 更新系统
apt update && apt upgrade -y  # Debian/Ubuntu
# 或
yum update -y                 # CentOS/RHEL

# 安装 Node.js（使用 nvm）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24

# 验证安装
node --version
npm --version
```

### 2. 安装 Clawdbot

```bash
# 全局安装
npm install -g clawdbot

# 或使用特定版本
npm install -g clawdbot@2026.1.24-3
```

### 3. 创建专用用户（可选但推荐）

```bash
# 创建用户
useradd -m -s /bin/bash clawdbot
usermod -aG sudo clawdbot

# 切换用户
su - clawdbot
```

### 4. 运行配置向导

```bash
clawdbot configure
```

配置建议：
- **工作目录**：`/home/clawdbot/clawd`
- **网关模式**：`local`
- **端口**：18789（确保防火墙开放）
- **绑定地址**：`loopback`（仅本地）或 `all`（所有接口）

### 5. 启动网关服务

```bash
# 使用 nohup 保持运行
cd ~
nohup clawdbot gateway --port 18789 --verbose > /var/log/clawdbot_gateway.log 2>&1 &

# 检查进程
ps aux | grep clawdbot

# 检查端口
netstat -tulpn | grep 18789
```

## 配置自定义模型（阿里百炼示例）

### 1. 准备配置文件

Clawdbot 配置文件位于 `~/.clawdbot/clawdbot.json`。以下是配置阿里百炼模型的示例：

```python
#!/usr/bin/env python3
import json
import os

config_path = '/root/.clawdbot/clawdbot.json'
with open(config_path, 'r') as f:
    data = json.load(f)

# 设置主模型和备用模型
data['agents']['defaults']['model']['primary'] = 'openai/deepseek-v3.2'
data['agents']['defaults']['model']['fallbacks'] = [
    'openai/qwen-plus',
    'openai/qwen-max'
]

# 定义模型映射（使用 openai provider）
data['agents']['defaults']['models'] = {
    'openai/deepseek-v3.2': {},
    'openai/qwen-plus': {},
    'openai/qwen-max': {},
    'openai/gpt-4o': {}
}

# 清理不需要的 provider
if 'models' in data and 'providers' in data['models']:
    data['models']['providers'].pop('qwen-portal', None)

# 禁用相关插件
if 'plugins' in data and 'entries' in data['plugins']:
    data['plugins']['entries']['qwen-portal-auth'] = {'enabled': False}

# 保存配置
with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)

print('✅ 阿里百炼模型配置完成')
```

将上述脚本保存为 `setup_alibaba.py` 并运行。

### 2. 设置环境变量

创建环境变量文件 `~/.clawdbot/.env`：

```bash
# 阿里百炼配置
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 其他可选配置
# ANTHROPIC_API_KEY=your_key
# COHERE_API_KEY=your_key
```

### 3. 重启网关

```bash
# 停止现有网关
pkill -f clawdbot-gateway
sleep 2

# 启动新网关
clawdbot gateway --local --port 18789 --verbose &
```

## 配置飞书频道

### 1. 安装飞书插件

Clawdbot 通过插件系统支持飞书集成。首先安装飞书插件：

```bash
# 使用 clawdbot 命令安装（推荐）
clawdbot plugins install @m1heng-clawd/feishu

# 或使用 npm 安装
npm install @m1heng-clawd/feishu

# 旧版命令（部分环境可能有效）
openclaw plugins install @m1heng-clawd/feishu
```

插件安装后，Clawdbot 会自动检测并启用飞书频道功能。

### 2. 快速安装流程（如果菜单中没有飞书选项）

如果在运行 `clawdbot configure` 或 `clawdbot channels add` 时看不到飞书选项，按顺序执行以下4条指令即可：

```bash
# 1. 安装飞书插件
clawdbot plugins install @m1heng-clawd/feishu

# 2. 停止现有网关（如果正在运行）
clawdbot gateway stop

# 3. 启动网关（临时测试）
clawdbot gateway --local --port 18789 --verbose

# 4. 重新进入通道配置菜单
clawdbot channels add
```

执行完成后，再次运行 `clawdbot channels add` 应该能看到飞书选项。

### 3. 安装速度优化（可选）

如果 `npm install` 命令执行缓慢，可以使用以下方法提速：

> **注意**：以下优化主要针对 `npm install` 命令。如果使用 `clawdbot plugins install` 命令，插件系统可能会自动处理依赖下载，但镜像设置仍有帮助。

#### 方案一：使用国内镜像（推荐）
```bash
# 临时使用淘宝镜像
npm install @m1heng-clawd/feishu --registry=https://registry.npmmirror.com

# 永久设置镜像源
npm config set registry https://registry.npmmirror.com
npm config set maxsockets 10
npm set progress=false

# 或使用 cnpm（淘宝官方客户端）
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install @m1heng-clawd/feishu
```

#### 方案二：使用更快的包管理器
```bash
# 安装 yarn
npm install -g yarn
yarn add @m1heng-clawd/feishu

# 或安装 pnpm
npm install -g pnpm
pnpm add @m1heng-clawd/feishu
```

#### 方案三：优化 npm 配置
```bash
# 使用离线模式（如果已有缓存）
npm install @m1heng-clawd/feishu --prefer-offline

# 清理并重建缓存
npm cache clean --force
npm install @m1heng-clawd/feishu
```

### 4. 编辑配置文件

在 `clawdbot.json` 中添加飞书配置：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a9f1348c21781cd5",
      "appSecret": "xqn5eFPnmf8xuueYKReuJcBZ0KYSgXd5"
    }
  }
}
```

### 5. 配置飞书应用

在飞书开放平台：
1. **权限管理**：添加 `im:message`、`im:message.group_at_msg` 等权限
2. **事件订阅**：添加 `im.message.receive_v1` 事件
3. **回调 URL**：`http://你的服务器IP:18789/feishu/events`
4. **安全设置**：添加加密密钥（如需）

### 6. 重启并验证

```bash
# 停止现有网关
clawdbot gateway stop
# 或手动终止
pkill -f clawdbot-gateway

# 临时启动网关（前台运行，查看日志）
clawdbot gateway --local --port 18789 --verbose

# 持久化启动网关（后台运行）
nohup clawdbot gateway --local --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 查看日志，确认飞书插件加载
tail -f /tmp/gateway.log
```

## 常用命令速查

### 网关管理命令

```bash
# 临时启动网关（前台运行，查看日志）
clawdbot gateway --local --port 18789 --verbose

# 持久化启动网关（后台运行）
nohup clawdbot gateway --local --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 停止网关
clawdbot gateway stop
# 或手动终止
pkill -f clawdbot-gateway
```

### 初始配置命令

```bash
# 运行交互式配置向导
clawdbot configure

# 初始引导（如果可用）
clawdbot onboard
```

### 通道管理命令

```bash
# 添加新通道（如飞书）
clawdbot channels add

# 列出已配置的通道
clawdbot channels list

# 移除通道
clawdbot channels remove <channel-name>

# 查看通道配置
clawdbot channels show <channel-name>
```

### 测试与验证命令

```bash
# 测试 AI 代理
clawdbot agent --agent main --message "你好" --local

# 查看版本
clawdbot --version

# 查看帮助
clawdbot --help
clawdbot gateway --help
```

## 进程管理与持久化

### 方案一：Systemd 服务（推荐）

创建服务文件 `/etc/systemd/system/clawdbot.service`：

```ini
[Unit]
Description=Clawdbot Gateway Service
After=network.target

[Service]
Type=simple
User=clawdbot
WorkingDirectory=/home/clawdbot
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="NODE_ENV=production"
ExecStart=/usr/local/bin/clawdbot gateway --local --port 18789 --verbose
Restart=on-failure
RestartSec=10
StandardOutput=append:/var/log/clawdbot.log
StandardError=append:/var/log/clawdbot_error.log

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable clawdbot
sudo systemctl start clawdbot
sudo systemctl status clawdbot
```

### 方案二：PM2 管理

```bash
# 安装 PM2
npm install -g pm2

# 启动服务
pm2 start clawdbot -- gateway --local --port 18789 --verbose

# 设置开机自启
pm2 startup
pm2 save
```

### 方案三：Docker 容器

创建 `Dockerfile`：

```dockerfile
FROM node:24-alpine
RUN npm install -g clawdbot
USER node
WORKDIR /home/node
CMD ["clawdbot", "gateway", "--local", "--port", "18789", "--verbose"]
```

构建并运行：

```bash
docker build -t clawdbot .
docker run -d -p 18789:18789 --name clawdbot \
  -v ~/.clawdbot:/home/node/.clawdbot \
  clawdbot
```

## 测试与验证

### 1. 基础功能测试

```bash
# 测试网关连通性
curl http://localhost:18789/health

# 测试 agent 响应
export OPENAI_API_KEY=your_key
clawdbot agent --agent main --message "你好，测试一下" --local --verbose on
```

### 2. 飞书集成测试

1. 在飞书群聊中 @你的机器人
2. 发送消息："测试"
3. 查看服务器日志确认消息处理
4. 机器人应回复确认信息

### 3. 配置验证

```bash
# 查看当前配置
cat ~/.clawdbot/clawdbot.json | jq '.agents.defaults.model'
cat ~/.clawdbot/clawdbot.json | jq '.agents.defaults.models'

# 检查环境变量
cat ~/.clawdbot/.env
```

## 故障排除

### 常见问题

#### 1. 网关启动失败

**症状**：端口已被占用或权限不足

```bash
# 检查端口占用
sudo lsof -i :18789

# 停止冲突进程
sudo kill -9 <PID>

# 或更换端口
clawdbot gateway --local --port 18790 --verbose
```

#### 2. 模型调用失败

**症状**：API 密钥错误或网络问题

```bash
# 验证环境变量
echo $OPENAI_API_KEY
echo $OPENAI_BASE_URL

# 手动测试 API 连接
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello"}]}'
```

#### 3. 飞书消息不回复

**症状**：事件订阅未生效或回调 URL 错误

```bash
# 检查飞书插件状态
grep -i feishu /var/log/clawdbot.log

# 验证回调 URL 可达性
curl -X POST http://localhost:18789/feishu/events \
  -H "Content-Type: application/json" \
  -d '{"test":"event"}'
```

#### 4. 进程意外退出

**症状**：服务自动停止

```bash
# 查看系统日志
sudo journalctl -u clawdbot -f

# 检查内存使用
free -h
top -p $(pgrep -f clawdbot)

# 增加重启策略（systemd）
# 修改 Restart=always
```

### 日志文件位置

- **网关日志**：`/var/log/clawdbot_gateway.log`
- **Systemd 日志**：`sudo journalctl -u clawdbot -f`
- **PM2 日志**：`pm2 logs clawdbot`
- **Docker 日志**：`docker logs clawdbot`

### 获取帮助

1. **查看命令帮助**：`clawdbot --help`
2. **查看网关选项**：`clawdbot gateway --help`
3. **查看配置文档**：访问 `~/.clawdbot/clawdbot.json` 注释
4. **社区支持**：查阅 Clawdbot 官方文档

---

## 总结

按照本指南，你可以：

1. ✅ 在本地快速测试 Clawdbot 功能
2. ✅ 在服务器上稳定部署生产环境
3. ✅ 配置阿里百炼等自定义模型
4. ✅ 集成飞书频道实现办公自动化
5. ✅ 使用 systemd/PM2/Docker 管理进程
6. ✅ 排查常见问题确保服务稳定

建议首次部署时按顺序执行每个章节，并验证每个步骤的成功状态。遇到问题时，参考故障排除章节或查看相关日志文件。

祝你部署顺利！ 🚀