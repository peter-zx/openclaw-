# Clawdbot 插件安装使用指南

## 📚 目录

1. [整体流程概览](#整体流程概览)
2. [文件结构说明](#文件结构说明)
3. [准备工作](#准备工作)
4. [云端操作步骤](#云端操作步骤)
5. [本地操作步骤](#本地操作步骤)
6. [插件配置](#插件配置)
7. [测试验证](#测试验证)
8. [常用插件](#常用插件)
9. [故障排除](#故障排除)
10. [检查清单](#检查清单)

---

## 整体流程概览

### 这是什么？

Clawdbot 的插件系统可以让您为 AI 助手添加各种功能，比如：

- **飞书集成**：在飞书群里 @机器人，让它回复消息
- **钉钉集成**：在钉钉群里使用 AI 助手
- **企业微信集成**：在企业微信中使用 AI 功能
- **QQ 机器人**：在 QQ 群中使用 AI 助手

**举个例子**：
- 您安装了飞书插件
- 在飞书群里 @机器人：帮我写一份周报
- 机器人会自动生成周报并发送到群里

---

### 工作流程图

```
第一步：了解文件结构
├─ 知道配置文件在哪里
├─ 知道插件文件在哪里
└─ 知道日志文件在哪里

第二步：云端准备
├─ 确认 Clawdbot 已安装
└─ 查看文件结构

第三步：安装插件
├─ 下载插件包
└─ 解压到正确位置

第四步：配置插件
├─ 编辑配置文件
└─ 设置应用信息

第五步：配置第三方平台
├─ 在飞书/钉钉等平台创建应用
├─ 获取 App ID 和 Secret
└─ 配置回调地址

第六步：重启网关
├─ 停止现有网关
└─ 启动新网关

第七步：测试使用
├─ 在飞书/钉钉等平台测试
└─ 验证功能正常
```

---

### 分工说明

| 操作 | 在哪里执行 | 说明 |
|-----|----------|------|
| **云端操作** | 云服务器 | 安装插件、配置文件、重启网关 |
| **本地操作** | 本地电脑 | 在飞书/钉钉等平台配置应用（可选） |
| **第三方平台** | 飞书/钉钉等 | 创建应用、获取凭证、设置回调 |

---

## 文件结构说明

### 这是最重要的！

Clawdbot 的所有文件都存放在云服务器的特定目录中。您需要了解这些目录的位置和作用。

---

### 完整文件结构树

```
/root/                              # 云服务器根目录
└── .clawdbot/                      # Clawdbot 主目录（最重要！）
    ├── clawdbot.json              # 主配置文件（必须编辑这个）
    ├── .env                       # 环境变量文件（存储 API Key 等）
    ├── extensions/                # 插件安装目录（插件文件放这里）
    │   ├── feishu/                # 飞书插件目录
    │   │   ├── dist/              # 插件程序文件
    │   │   │   └── index.js       # 插件主程序
    │   │   ├── package.json       # 插件配置文件
    │   │   └── README.md          # 插件说明文档
    │   ├── dingtalk/              # 钉钉插件目录
    │   │   ├── dist/
    │   │   │   └── index.js
    │   │   ├── package.json
    │   │   └── README.md
    │   ├── wecom/                 # 企业微信插件目录
    │   │   ├── dist/
    │   │   │   └── index.js
    │   │   ├── package.json
    │   │   └── README.md
    │   └── qqbot/                 # QQ 机器人插件目录
    │       ├── dist/
    │       │   └── index.js
    │       ├── package.json
    │       └── README.md
    ├── agents/                    # Agent 配置目录
    │   └── main/
    │       └── agent/
    │           ├── agent.json     # Agent 配置文件
    │           ├── models.json    # 模型配置文件
    │           └── auth-profiles.json  # 认证配置文件
    ├── workspace/                 # 工作空间目录
    │   └── sessions/              # 会话文件目录
    ├── canvas/                    # Canvas 目录
    └── logs/                      # 日志目录（可选）
```

---

### 关键文件说明

#### 1. 主配置文件：`/root/.clawdbot/clawdbot.json`

**作用**：这是 Clawdbot 的主配置文件，所有插件和频道的配置都在这里。

**位置**：`/root/.clawdbot/clawdbot.json`

**重要**：安装插件后，必须编辑这个文件来启用插件。

---

#### 2. 插件目录：`/root/.clawdbot/extensions/`

**作用**：所有插件文件都存放在这个目录下。

**位置**：`/root/.clawdbot/extensions/`

**结构**：
```
/root/.clawdbot/extensions/
├── feishu/          # 飞书插件
├── dingtalk/        # 钉钉插件
├── wecom/           # 企业微信插件
└── qqbot/           # QQ 机器人插件
```

**重要**：插件必须解压到这个目录下，否则无法加载。

---

#### 3. 环境变量文件：`/root/.clawdbot/.env`

**作用**：存储敏感信息，如 API Key、密码等。

**位置**：`/root/.clawdbot/.env`

**重要**：这个文件不会被提交到 Git，更安全。

---

#### 4. 日志文件：`/tmp/openclaw/` 或 `/tmp/gateway.log`

**作用**：记录网关运行日志，用于排查问题。

**位置**：
- `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- `/tmp/gateway.log`

**重要**：遇到问题时，先查看这个文件。

---

### 文件路径速查表

| 文件/目录 | 路径 | 作用 |
|----------|------|------|
| **主配置文件** | `/root/.clawdbot/clawdbot.json` | 所有配置都在这里 |
| **插件目录** | `/root/.clawdbot/extensions/` | 插件文件存放位置 |
| **环境变量** | `/root/.clawdbot/.env` | 存储敏感信息 |
| **网关日志** | `/tmp/gateway.log` | 查看运行日志 |
| **飞书插件** | `/root/.clawdbot/extensions/feishu/` | 飞书插件文件 |
| **钉钉插件** | `/root/.clawdbot/extensions/dingtalk/` | 钉钉插件文件 |
| **企业微信插件** | `/root/.clawdbot/extensions/wecom/` | 企业微信插件文件 |
| **QQ 机器人插件** | `/root/.clawdbot/extensions/qqbot/` | QQ 机器人插件文件 |

---

## 准备工作

### 您需要准备什么？

#### 1. 云端准备

您需要一台已经安装好 Clawdbot 的云服务器。

**如何检查**：
```bash
# 在云服务器上执行
clawdbot --version
```

**如果显示版本号**（如 `2026.1.29`），说明已经安装好了。✅

**如果提示命令不存在**，需要先安装 Clawdbot。

---

#### 2. 检查文件结构

在云服务器上执行以下命令，确认文件结构：

```bash
# 查看主目录是否存在
ls -la ~/.clawdbot/

# 查看主配置文件
cat ~/.clawdbot/clawdbot.json

# 查看插件目录
ls -la ~/.clawdbot/extensions/

# 查看环境变量文件
cat ~/.clawdbot/.env 2>/dev/null || echo "文件不存在"
```

**预期结果**：
```
/root/.clawdbot/
├── clawdbot.json              # 存在
├── .env                       # 可能不存在
├── extensions/                # 目录存在
├── agents/                    # 目录存在
└── workspace/                 # 目录存在
```

✅ 如果看到这些目录和文件，说明 Clawdbot 已正确安装。

---

#### 3. 插件准备

您需要知道要安装哪个插件：

| 插件名称 | 功能 | 插件目录 |
|---------|------|---------|
| `@m1heng-clawd/feishu` | 飞书集成 | `/root/.clawdbot/extensions/feishu/` |
| `@m1heng-clawd/dingtalk` | 钉钉集成 | `/root/.clawdbot/extensions/dingtalk/` |
| `@m1heng-clawd/wecom` | 企业微信集成 | `/root/.clawdbot/extensions/wecom/` |
| `@m1heng-clawd/qqbot` | QQ 机器人 | `/root/.clawdbot/extensions/qqbot/` |

---

#### 4. 第三方平台准备（以飞书为例）

您需要在飞书开放平台创建企业自建应用：

- 访问：https://open.feishu.cn/
- 登录您的飞书账号
- 创建企业自建应用
- 获取 `App ID` 和 `App Secret`

---

### 准备工作检查清单

在开始之前，请确认：

- [ ] 云服务器上已安装 Clawdbot
- [ ] 可以正常访问云服务器
- [ ] `/root/.clawdbot/` 目录存在
- [ ] `/root/.clawdbot/clawdbot.json` 文件存在
- [ ] `/root/.clawdbot/extensions/` 目录存在
- [ ] 确定要安装的插件类型
- [ ] 已在第三方平台创建应用（如飞书）
- [ ] 已获取 App ID 和 App Secret

---

## 云端操作步骤

### 第一步：确认文件结构

在云服务器上执行：

```bash
# 查看主目录
ls -la ~/.clawdbot/

# 查看插件目录
ls -la ~/.clawdbot/extensions/

# 查看主配置文件
cat ~/.clawdbot/clawdbot.json
```

**预期结果**：
```
/root/.clawdbot/
├── clawdbot.json
├── .env
├── extensions/
├── agents/
└── workspace/

/root/.clawdbot/extensions/
（可能为空，或已有其他插件）
```

✅ 确认目录结构正确后，继续下一步。

---

### 第二步：安装插件（方法一：使用命令）

以飞书插件为例：

```bash
# 安装飞书插件
clawdbot plugins install @m1heng-clawd/feishu
```

**预期结果**：
```
✅ Plugin installed successfully
📁 Plugin location: /root/.clawdbot/extensions/feishu
```

**验证安装**：
```bash
# 查看插件目录
ls -la ~/.clawdbot/extensions/feishu/

# 应该看到：
# dist/
# package.json
# README.md
```

✅ 如果看到插件目录，说明安装成功。

---

### 第三步：安装插件（方法二：手动下载解压）

如果命令安装失败，可以手动下载并解压：

#### 3.1 下载插件包

```bash
# 创建临时目录
mkdir -p /tmp/plugins
cd /tmp/plugins

# 下载插件包（根据实际情况调整 URL）
wget https://example.com/feishu.tgz

# 或使用 curl
curl -O https://example.com/feishu.tgz
```

---

#### 3.2 解压到正确位置

```bash
# 解压插件包
tar -xzf feishu.tgz

# 查看解压后的文件
ls -la

# 移动到插件目录
mv feishu ~/.clawdbot/extensions/

# 验证
ls -la ~/.clawdbot/extensions/feishu/
```

**预期结果**：
```
/root/.clawdbot/extensions/feishu/
├── dist/
│   └── index.js
├── package.json
└── README.md
```

✅ 如果看到这些文件，说明解压成功。

---

### 第四步：编辑主配置文件

#### 4.1 备份配置文件（推荐）

```bash
# 备份原配置
cp ~/.clawdbot/clawdbot.json ~/.clawdbot/clawdbot.json.backup

# 验证备份
ls -la ~/.clawdbot/clawdbot.json.backup
```

---

#### 4.2 编辑配置文件

```bash
# 编辑配置文件
nano ~/.clawdbot/clawdbot.json
```

---

#### 4.3 添加插件配置

找到 `plugins` 部分，添加飞书配置：

```json
{
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  }
}
```

**重要提示**：
- 文件路径：`/root/.clawdbot/clawdbot.json`
- 必须添加到 `plugins.entries` 部分
- `enabled` 设置为 `true` 启用插件

---

#### 4.4 添加频道配置

找到 `channels` 部分，添加飞书频道配置：

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

**重要提示**：
- 文件路径：`/root/.clawdbot/clawdbot.json`
- 必须添加到 `channels` 部分
- `appId` 和 `appSecret` 从飞书开放平台获取

---

#### 4.5 保存并退出

- 按 `Ctrl + O` 保存
- 按 `Enter` 确认
- 按 `Ctrl + X` 退出

---

#### 4.6 验证配置文件

```bash
# 检查配置文件语法
cat ~/.clawdbot/clawdbot.json | python3 -m json.tool
```

✅ 如果没有错误提示，说明配置文件格式正确。

---

### 第五步：停止现有网关

```bash
# 停止网关
clawdbot gateway stop

# 或手动终止进程
pkill -f clawdbot-gateway

# 确认已停止
ps aux | grep clawdbot
```

✅ 如果没有输出，说明网关已停止。

---

### 第六步：启动网关

#### 6.1 前台运行（测试用）

```bash
# 前台运行，查看日志
clawdbot gateway --port 18789 --verbose
```

**预期结果**：
```
🦞 OpenClaw 2026.1.29 — Gateway online
[feishu:default] logged in to feishu as cli_a9f1348c21781cd5
```

✅ 如果看到 `logged in to feishu`，说明插件加载成功。

---

#### 6.2 后台运行（生产环境）

如果前台运行正常，可以改为后台运行：

```bash
# 按 Ctrl+C 停止前台运行

# 后台运行
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 查看日志
tail -f /tmp/gateway.log
```

---

## 本地操作步骤（配置飞书应用）

### 第一步：登录飞书开放平台

访问：https://open.feishu.cn/

---

### 第二步：创建企业自建应用

1. 点击"创建企业自建应用"
2. 填写应用名称（如：AI 助手）
3. 选择应用图标
4. 点击"创建"

---

### 第三步：获取凭证

1. 在应用页面，点击"凭证与基础信息"
2. 复制 `App ID`
3. 复制 `App Secret`

**重要提示**：
- ✅ 将这两个值保存到云服务器的配置文件中
- ✅ 配置文件路径：`/root/.clawdbot/clawdbot.json`
- ✅ App Secret 只显示一次，请妥善保管

---

### 第四步：配置权限

1. 点击"权限管理"
2. 搜索并添加以下权限：
   - `im:message` - 发送消息
   - `im:message.group_at_msg` - 接收群组@消息
   - `im:message:send_as_bot` - 以机器人身份发送消息

3. 点击"申请权限"

---

### 第五步：配置事件订阅

1. 点击"事件订阅"
2. 添加事件：`im.message.receive_v1`
3. 设置回调 URL：`http://你的服务器IP:18789/feishu/events`

**重要提示**：
- 回调 URL 必须是公网可访问的地址
- 如果使用 Tailscale，需要配置端口转发

---

### 第六步：配置安全设置（可选）

1. 点击"安全设置"
2. 启用"数据加密"
3. 复制"Encrypt Key"
4. 在配置文件中添加：

```json
{
  "channels": {
    "feishu": {
      "encryptKey": "your_encrypt_key_here"
    }
  }
}
```

配置文件路径：`/root/.clawdbot/clawdbot.json`

---

### 第七步：发布应用

1. 点击"版本管理与发布"
2. 点击"创建版本"
3. 填写版本号和更新说明
4. 点击"申请发布"
5. 等待审核通过（通常几分钟）

---

## 插件配置

### 飞书插件完整配置示例

**配置文件路径**：`/root/.clawdbot/clawdbot.json`

```json
{
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a9f1348c21781cd5",
      "appSecret": "xqn5eFPnmf8xuueYKReuJcBZ0KYSgXd5",
      "encryptKey": "your_encrypt_key_here"
    }
  }
}
```

---

### 钉钉插件完整配置示例

**配置文件路径**：`/root/.clawdbot/clawdbot.json`

```json
{
  "plugins": {
    "entries": {
      "dingtalk": {
        "enabled": true
      }
    }
  },
  "channels": {
    "dingtalk": {
      "enabled": true,
      "appKey": "your_app_key",
      "appSecret": "your_app_secret"
    }
  }
}
```

---

### 企业微信插件完整配置示例

**配置文件路径**：`/root/.clawdbot/clawdbot.json`

```json
{
  "plugins": {
    "entries": {
      "wecom": {
        "enabled": true
      }
    }
  },
  "channels": {
    "wecom": {
      "enabled": true,
      "corpId": "your_corp_id",
      "agentId": "your_agent_id",
      "secret": "your_secret"
    }
  }
}
```

---

### QQ 机器人插件完整配置示例

**配置文件路径**：`/root/.clawdbot/clawdbot.json`

```json
{
  "plugins": {
    "entries": {
      "qqbot": {
        "enabled": true
      }
    }
  },
  "channels": {
    "qqbot": {
      "enabled": true,
      "uin": "your_qq_number",
      "password": "your_qq_password"
    }
  }
}
```

---

## 测试验证

### 测试 1：查看文件结构

在云服务器上执行：

```bash
# 查看插件目录
ls -la ~/.clawdbot/extensions/

# 应该看到：
# feishu/
# （或其他插件目录）

# 查看插件文件
ls -la ~/.clawdbot/extensions/feishu/

# 应该看到：
# dist/
# package.json
# README.md
```

✅ 如果看到这些文件，说明插件已正确安装。

---

### 测试 2：查看配置文件

在云服务器上执行：

```bash
# 查看主配置文件
cat ~/.clawdbot/clawdbot.json | python3 -m json.tool

# 检查插件配置
cat ~/.clawdbot/clawdbot.json | grep -A 5 "plugins"

# 检查频道配置
cat ~/.clawdbot/clawdbot.json | grep -A 10 "channels"
```

✅ 如果看到插件和频道配置，说明配置正确。

---

### 测试 3：查看网关日志

在云服务器上执行：

```bash
# 查看网关日志
tail -f /tmp/gateway.log
```

**预期结果**：
```
[feishu:default] logged in to feishu as cli_a9f1348c21781cd5
```

✅ 如果看到这个提示，说明插件已成功加载。

---

### 测试 4：在飞书中测试

1. 打开飞书
2. 进入安装了应用的群聊
3. @机器人，发送消息：你好

**预期结果**：
- 机器人会回复消息

---

### 测试 5：验证回调 URL

在云服务器上执行：

```bash
# 测试回调 URL 是否可访问
curl -X POST http://localhost:18789/feishu/events \
  -H "Content-Type: application/json" \
  -d '{"test":"event"}'
```

**预期结果**：
```
{"status":"ok"}
```

✅ 如果返回这个结果，说明回调 URL 配置正确。

---

## 常用插件

### 飞书插件

**插件名称**：`@m1heng-clawd/feishu`

**插件目录**：`/root/.clawdbot/extensions/feishu/`

**功能**：
- 在飞书群聊中使用 AI 助手
- 支持 @机器人交互
- 支持图片识别
- 支持文件处理

**安装命令**：
```bash
clawdbot plugins install @m1heng-clawd/feishu
```

**配置文档**：https://open.feishu.cn/

---

### 钉钉插件

**插件名称**：`@m1heng-clawd/dingtalk`

**插件目录**：`/root/.clawdbot/extensions/dingtalk/`

**功能**：
- 在钉钉群聊中使用 AI 助手
- 支持 @机器人交互
- 支持卡片消息

**安装命令**：
```bash
clawdbot plugins install @m1heng-clawd/dingtalk
```

**配置文档**：https://open.dingtalk.com/

---

### 企业微信插件

**插件名称**：`@m1heng-clawd/wecom`

**插件目录**：`/root/.clawdbot/extensions/wecom/`

**功能**：
- 在企业微信群聊中使用 AI 助手
- 支持 @机器人交互
- 支持图文消息

**安装命令**：
```bash
clawdbot plugins install @m1heng-clawd/wecom
```

**配置文档**：https://developer.work.weixin.qq.com/

---

### QQ 机器人插件

**插件名称**：`@m1heng-clawd/qqbot`

**插件目录**：`/root/.clawdbot/extensions/qqbot/`

**功能**：
- 在 QQ 群聊中使用 AI 助手
- 支持 @机器人交互
- 支持私聊

**安装命令**：
```bash
clawdbot plugins install @m1heng-clawd/qqbot
```

---

## 故障排除

### 问题 1：插件目录不存在

**症状**：执行 `ls ~/.clawdbot/extensions/` 提示目录不存在

**解决方案**：

```bash
# 创建插件目录
mkdir -p ~/.clawdbot/extensions

# 验证
ls -la ~/.clawdbot/extensions/
```

---

### 问题 2：插件文件缺失

**症状**：插件目录存在，但缺少必要文件

**解决方案**：

```bash
# 查看插件目录
ls -la ~/.clawdbot/extensions/feishu/

# 应该看到：
# dist/
# package.json
# README.md

# 如果文件缺失，重新安装
clawdbot plugins install @m1heng-clawd/feishu
```

---

### 问题 3：配置文件格式错误

**症状**：网关启动失败，提示配置文件格式错误

**解决方案**：

```bash
# 检查配置文件语法
cat ~/.clawdbot/clawdbot.json | python3 -m json.tool

# 如果有错误，恢复备份
cp ~/.clawdbot/clawdbot.json.backup ~/.clawdbot/clawdbot.json

# 重新编辑
nano ~/.clawdbot/clawdbot.json
```

---

### 问题 4：插件加载失败

**症状**：网关启动时提示插件加载失败

**解决方案**：

```bash
# 查看详细日志
clawdbot gateway --port 18789 --verbose

# 检查插件文件
ls -la ~/.clawdbot/extensions/feishu/

# 检查配置文件
cat ~/.clawdbot/clawdbot.json | grep -A 5 "plugins"

# 重新安装插件
rm -rf ~/.clawdbot/extensions/feishu
clawdbot plugins install @m1heng-clawd/feishu
```

---

### 问题 5：飞书消息不回复

**症状**：在飞书中 @机器人，但没有回复

**解决方案**：

```bash
# 检查网关日志
tail -f /tmp/gateway.log | grep feishu

# 检查回调 URL 配置
curl -X POST http://localhost:18789/feishu/events \
  -H "Content-Type: application/json" \
  -d '{"test":"event"}'

# 检查飞书应用配置
# - 权限是否已授予
# - 事件订阅是否已配置
# - 应用是否已发布
```

---

## 检查清单

### 文件结构检查清单

在开始之前，请确认以下目录和文件存在：

- [ ] `/root/.clawdbot/` 主目录存在
- [ ] `/root/.clawdbot/clawdbot.json` 主配置文件存在
- [ ] `/root/.clawdbot/extensions/` 插件目录存在
- [ ] `/root/.clawdbot/extensions/feishu/` 飞书插件目录存在
- [ ] `/root/.clawdbot/extensions/feishu/dist/` 插件程序目录存在
- [ ] `/root/.clawdbot/extensions/feishu/package.json` 插件配置文件存在
- [ ] `/root/.clawdbot/.env` 环境变量文件存在（可选）

---

### 云端检查清单

- [ ] Clawdbot 已安装
- [ ] 插件已安装到正确目录
- [ ] 配置文件已编辑
- [ ] App ID 和 App Secret 已填写
- [ ] 网关已重启
- [ ] 网关日志显示插件加载成功
- [ ] 端口 18789 已开放
- [ ] 防火墙规则已配置

---

### 第三方平台检查清单（以飞书为例）

- [ ] 已创建企业自建应用
- [ ] 已获取 App ID 和 App Secret
- [ ] 已添加必要权限
- [ ] 已配置事件订阅
- [ ] 回调 URL 已填写
- [ ] 应用已发布
- [ ] 应用已添加到群聊

---

### 功能测试检查清单

- [ ] 插件目录存在且文件完整
- [ ] 配置文件格式正确
- [ ] 网关日志显示插件加载成功
- [ ] 回调 URL 验证通过
- [ ] 在飞书中 @机器人有回复
- [ ] 机器人可以正常对话
- [ ] 图片识别功能正常
- [ ] 文件处理功能正常

---

## 总结

### 核心步骤

1. **了解文件结构**：知道配置文件和插件文件在哪里
2. **云端准备**：确认 Clawdbot 已安装，查看文件结构
3. **安装插件**：下载插件包并解压到正确位置
4. **配置插件**：编辑配置文件，添加应用信息
5. **配置平台**：在第三方平台创建应用，获取凭证
6. **重启网关**：停止旧网关，启动新网关
7. **测试使用**：在第三方平台测试功能

---

### 快速命令参考

```bash
# 查看文件结构
ls -la ~/.clawdbot/
ls -la ~/.clawdbot/extensions/

# 安装插件
clawdbot plugins install @m1heng-clawd/feishu

# 编辑配置
nano ~/.clawdbot/clawdbot.json

# 验证配置
cat ~/.clawdbot/clawdbot.json | python3 -m json.tool

# 停止网关
clawdbot gateway stop

# 启动网关（前台）
clawdbot gateway --port 18789 --verbose

# 启动网关（后台）
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 查看日志
tail -f /tmp/gateway.log

# 测试回调 URL
curl -X POST http://localhost:18789/feishu/events \
  -H "Content-Type: application/json" \
  -d '{"test":"event"}'
```

---

### 文件路径速查

| 文件/目录 | 路径 |
|----------|------|
| **主配置文件** | `/root/.clawdbot/clawdbot.json` |
| **插件目录** | `/root/.clawdbot/extensions/` |
| **飞书插件** | `/root/.clawdbot/extensions/feishu/` |
| **钉钉插件** | `/root/.clawdbot/extensions/dingtalk/` |
| **企业微信插件** | `/root/.clawdbot/extensions/wecom/` |
| **QQ 机器人插件** | `/root/.clawdbot/extensions/qqbot/` |
| **环境变量** | `/root/.clawdbot/.env` |
| **网关日志** | `/tmp/gateway.log` |

---

### 下一步建议

1. ✅ 了解文件结构
2. ✅ 安装插件到正确位置
3. ✅ 编辑配置文件
4. ✅ 配置第三方平台
5. ✅ 测试基础功能
6. ✅ 探索高级功能
7. ✅ 配置自动化规则

---

**文档版本**: 3.0
**最后更新**: 2026-02-02
**适用版本**: Clawdbot 2026.1.29+

---

祝您使用顺利！如有任何问题，欢迎随时咨询。🚀
