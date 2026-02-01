# 如何切换自定义大模型使用API

## 📚 目录

1. [整体流程概览](#整体流程概览)
2. [文件结构说明](#文件结构说明)
3. [准备工作](#准备工作)
4. [云端操作步骤](#云端操作步骤)
5. [配置详解](#配置详解)
6. [测试验证](#测试验证)
7. [常见问题](#常见问题)
8. [检查清单](#检查清单)

---

## 整体流程概览

### 这是什么？

OpenClaw/Clawdbot 支持使用第三方大语言模型 API，比如：

- **阿里云百炼**：DeepSeek、Qwen 等模型
- **OpenAI**：GPT-4、GPT-3.5 等模型
- **其他 OpenAI 兼容接口**：大多数第三方 API

**举个例子**：
- 您想使用阿里云百炼的 DeepSeek 模型
- 通过配置文件，将 API Key 和端点地址填入
- 重启网关后，AI 助手就会使用 DeepSeek 模型

---

### 工作流程图

```
第一步：了解文件结构
├─ 知道配置文件在哪里
├─ 知道环境变量文件在哪里
└─ 知道日志文件在哪里

第二步：云端准备
├─ 确认 OpenClaw 已安装
├─ 查看文件结构
└─ 备份原配置

第三步：获取 API 凭证
├─ 在阿里云百炼注册
├─ 获取 API Key
└─ 获取 API 端点地址

第四步：编辑配置文件
├─ 编辑主配置文件
├─ 添加模型配置
└─ 添加 Provider 配置

第五步：设置环境变量
├─ 创建环境变量文件
├─ 填入 API Key
└─ 填入 API 端点

第六步：重启网关
├─ 停止现有网关
├─ 加载环境变量
└─ 启动新网关

第七步：测试验证
├─ 查看模型状态
├─ 查看模型列表
└─ 测试对话
```

---

### 分工说明

| 操作 | 在哪里执行 | 说明 |
|-----|----------|------|
| **云端操作** | 云服务器 | 编辑配置文件、设置环境变量、重启网关 |
| **本地操作** | 本地电脑 | 在阿里云百炼等平台注册并获取 API 凭证 |

---

## 文件结构说明

### 这是最重要的！

OpenClaw 的所有配置都存放在云服务器的特定目录中。您需要了解这些目录的位置和作用。

---

### 完整文件结构树

```
/root/                              # 云服务器根目录
└── .openclaw/                      # OpenClaw 主目录（最重要！）
    ├── openclaw.json               # 主配置文件（必须编辑这个）
    ├── .env                        # 环境变量文件（存储 API Key 等）
    ├── agents/                     # Agent 配置目录
    │   └── main/
    │       └── agent/
    │           ├── agent.json      # Agent 配置文件
    │           ├── models.json     # 模型配置文件
    │           └── auth-profiles.json  # 认证配置文件
    ├── workspace/                  # 工作空间目录
    │   └── sessions/               # 会话文件目录
    ├── canvas/                     # Canvas 目录
    └── logs/                       # 日志目录（可选）
```

---

### 关键文件说明

#### 1. 主配置文件：`/root/.openclaw/openclaw.json`

**作用**：这是 OpenClaw 的主配置文件，所有模型和 Provider 的配置都在这里。

**位置**：`/root/.openclaw/openclaw.json`

**重要**：切换模型时，必须编辑这个文件。

---

#### 2. 环境变量文件：`/root/.openclaw/.env`

**作用**：存储敏感信息，如 API Key、密码等。

**位置**：`/root/.openclaw/.env`

**重要**：这个文件不会被提交到 Git，更安全。API Key 必须放在这里。

---

#### 3. 模型配置文件：`/root/.openclaw/agents/main/agent/models.json`

**作用**：���储模型的具体定义和参数。

**位置**：`/root/.openclaw/agents/main/agent/models.json`

**重要**：这个文件通常由主配置文件自动生成，不需要手动编辑。

---

#### 4. 认证配置文件：`/root/.openclaw/agents/main/agent/auth-profiles.json`

**作用**：存储认证信息，如 OAuth Token、API Key 等。

**位置**：`/root/.openclaw/agents/main/agent/auth-profiles.json`

**重要**：切换到 API 方式后，需要清理这个文件中的旧认证信息。

---

#### 5. 网关日志：`/tmp/openclaw/` 或 `/tmp/gateway.log`

**作用**：记录网关运行日志，用于排查问题。

**位置**：
- `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- `/tmp/gateway.log`

**重要**：遇到问题时，先查看这个文件。

---

### 文件路径速查表

| 文件/目录 | 路径 | 作用 |
|----------|------|------|
| **主配置文件** | `/root/.openclaw/openclaw.json` | 所有配置都在这里 |
| **环境变量文件** | `/root/.openclaw/.env` | 存储 API Key |
| **模型配置文件** | `/root/.openclaw/agents/main/agent/models.json` | 模型定义 |
| **认证配置文件** | `/root/.openclaw/agents/main/agent/auth-profiles.json` | 认证信息 |
| **网关日志** | `/tmp/gateway.log` | 查看运行日志 |

---

## 准备工作

### 您需要准备什么？

#### 1. 云端准备

您需要一台已经安装好 OpenClaw 的云服务器。

**如何检查**：
```bash
# 在云服务器上执行
openclaw --version
```

**如果显示版本号**（如 `2026.1.29`），说明已经安装好了。✅

**如果提示命令不存在**，需要先安装 OpenClaw。

---

#### 2. 检查文件结构

在云服务器上执行以下命令，确认文件结构：

```bash
# 查看主目录是否存在
ls -la ~/.openclaw/

# 查看主配置文件
cat ~/.openclaw/openclaw.json

# 查看环境变量文件
cat ~/.openclaw/.env 2>/dev/null || echo "文件不存在"

# 查看模型配置文件
cat ~/.openclaw/agents/main/agent/models.json 2>/dev/null || echo "文件不存在"
```

**预期结果**：
```
/root/.openclaw/
├── openclaw.json              # 存在
├── .env                       # 可能不存在
├── agents/
│   └── main/
│       └── agent/
│           ├── agent.json     # 存在
│           ├── models.json    # 存在
│           └── auth-profiles.json  # 存在
└── workspace/                 # 目录存在
```

✅ 如果看到这些目录和文件，说明 OpenClaw 已正确安装。

---

#### 3. 获取 API 凭证（以阿里云百炼为例）

##### 3.1 注册阿里云百炼

访问：https://dashscope.aliyun.com/

---

##### 3.2 创建 API Key

1. 登录阿里云百炼
2. 点击"API-KEY管理"
3. 点击"创建新的API-KEY"
4. 复制生成的 API Key

**重要提示**：
- ✅ API Key 格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- ✅ 请妥善保管，不要泄露
- ✅ 只显示一次，请立即复制保存

---

##### 3.3 获取 API 端点地址

阿里云百炼的 OpenAI 兼容端点：

```
https://dashscope.aliyuncs.com/compatible-mode/v1
```

---

### 准备工作检查清单

在开始之前，请确认：

- [ ] 云服务器上已安装 OpenClaw
- [ ] 可以正常访问云服务器
- [ ] `/root/.openclaw/` 目录存在
- [ ] `/root/.openclaw/openclaw.json` 文件存在
- [ ] `/root/.openclaw/agents/main/agent/models.json` 文件存在
- [ ] 已注册阿里云百炼账户
- [ ] 已获取 API Key
- [ ] 已获取 API 端点地址

---

## 云端操作步骤

### 第一步：确认文件结构

在云服务器上执行：

```bash
# 查看主目录
ls -la ~/.openclaw/

# 查看主配置文件
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 查看模型配置文件
cat ~/.openclaw/agents/main/agent/models.json | python3 -m json.tool
```

✅ 确认目录结构正确后，继续下一步。

---

### 第二步：备份原配置文件（推荐）

```bash
# 备份主配置文件
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 备份模型配置文件
cp ~/.openclaw/agents/main/agent/models.json ~/.openclaw/agents/main/agent/models.json.backup

# 验证备份
ls -la ~/.openclaw/*.backup
```

✅ 如果看到备份文件，说明备份成功。

---

### 第三步：编辑主配置文件

#### 3.1 打开配置文件

```bash
# 编辑主配置文件
nano ~/.openclaw/openclaw.json
```

---

#### 3.2 配置 Agent 默认模型

找到 `agents.defaults` 部分，添加或修改以下配置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai/deepseek-v3.2",
        "fallbacks": [
          "openai/qwen-plus",
          "openai/qwen-max"
        ]
      },
      "models": {
        "openai/deepseek-v3.2": {},
        "openai/qwen-plus": {},
        "openai/qwen-max": {},
        "openai/gpt-4o": {}
      }
    }
  }
}
```

**配置说明**：
- `primary`: 主模型，默认使用 `openai/deepseek-v3.2`
- `fallbacks`: 备用模型列表，主模型失败时自动切换
- `models`: 所有可用模型的映射表

---

#### 3.3 配置 OpenAI Provider

找到 `models.providers` 部分，添加或修改以下配置：

```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",
        "apiKey": "shell:OPENAI_API_KEY",
        "models": [
          {
            "id": "deepseek-v3.2",
            "name": "DeepSeek V3.2",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 8192
          },
          {
            "id": "qwen-plus",
            "name": "Qwen Plus",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 8192
          },
          {
            "id": "qwen-max",
            "name": "Qwen Max",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 8192
          },
          {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

**配置说明**：
- `baseUrl`: API 端点地址
- `api`: API 类型，固定为 `openai-completions`
- `apiKey`: API Key，`shell:OPENAI_API_KEY` 表示从环境变量读取
- `models`: 模型定义数组，每个模型必须包含完整定义

---

#### 3.4 禁用 qwen-portal-auth 插件（避免冲突）

找到 `plugins.entries` 部分，添加或修改以下配置：

```json
{
  "plugins": {
    "entries": {
      "qwen-portal-auth": {
        "enabled": false
      }
    }
  }
}
```

---

#### 3.5 保存并退出

- 按 `Ctrl + O` 保存
- 按 `Enter` 确认
- 按 `Ctrl + X` 退出

---

#### 3.6 验证配置文件

```bash
# 检查配置文件语法
cat ~/.openclaw/openclaw.json | python3 -m json.tool
```

✅ 如果没有错误提示，说明配置文件格式正确。

---

### 第四步：创建环境变量文件

#### 4.1 创建环境变量文件

```bash
# 创建环境变量文件
nano ~/.openclaw/.env
```

---

#### 4.2 添加环境变量

```bash
# 阿里云百炼配置
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**重要提示**：
- 文件路径：`/root/.openclaw/.env`
- `OPENAI_API_KEY`: 替换为您的真实 API Key
- `OPENAI_BASE_URL`: API 端点地址

---

#### 4.3 保存并退出

- 按 `Ctrl + O` 保存
- 按 `Enter` 确认
- 按 `Ctrl + X` 退出

---

#### 4.4 验证环境变量文件

```bash
# 查看环境变量文件
cat ~/.openclaw/.env
```

✅ 如果看到环境变量，说明文件创建成功。

---

### 第五步：清理旧认证信息（可选）

如果您之前使用过 qwen-portal 的 OAuth 认证，需要清理旧信息：

```bash
# 查看认证配置文件
cat ~/.openclaw/agents/main/agent/auth-profiles.json

# 如果有 qwen-portal 相关的认证，可以手动编辑删除
nano ~/.openclaw/agents/main/agent/auth-profiles.json
```

---

### 第六步：停止现有网关

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

### 第七步：加载环境变量

```bash
# 加载环境变量
source ~/.openclaw/.env

# 验证环境变量
echo "OPENAI_API_KEY: $OPENAI_API_KEY"
echo "OPENAI_BASE_URL: $OPENAI_BASE_URL"
```

✅ 如果看到环境变量的值，说明加载成功。

---

### 第八步：启动网关

#### 8.1 前台运行（测试用）

```bash
# 前台运行，查看日志
clawdbot gateway --port 18789 --verbose
```

**预期结果**：
```
🦞 OpenClaw 2026.1.29 — Gateway online
[gateway] agent model: openai/deepseek-v3.2
```

✅ 如果看到 `agent model: openai/deepseek-v3.2`，说明模型配置成功。

---

#### 8.2 后台运行（生产环境）

如果前台运行正常，可以改为后台运行：

```bash
# 按 Ctrl+C 停止前台运行

# 后台运行
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 查看日志
tail -f /tmp/gateway.log
```

---

## 配置详解

### 1. Agent 默认模型配置

**配置文件路径**：`/root/.openclaw/openclaw.json`

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai/deepseek-v3.2",
        "fallbacks": [
          "openai/qwen-plus",
          "openai/qwen-max"
        ]
      },
      "models": {
        "openai/deepseek-v3.2": {},
        "openai/qwen-plus": {},
        "openai/qwen-max": {},
        "openai/gpt-4o": {}
      }
    }
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|-----|------|------|
| `primary` | string | 主模型，默认使用的模型 |
| `fallbacks` | array | 备用模型列表，主模型失败时自动切换 |
| `models` | object | 所有可用模型的映射表 |

---

### 2. OpenAI Provider 配置（核心）

**配置文件路径**：`/root/.openclaw/openclaw.json`

```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",
        "apiKey": "shell:OPENAI_API_KEY",
        "models": [...]
      }
    }
  }
}
```

**字段说明**：

| 字段 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `baseUrl` | string | ✅ | API 端点 URL |
| `api` | string | ✅ | API 类型，通常为 `openai-completions` |
| `apiKey` | string | ✅ | API Key，`shell:OPENAI_API_KEY` 表示从环境变量读取 |
| `models` | array | ✅ | 模型定义数组 |

---

### 3. 模型定义数组

每个模型必须包含完整的定义：

```json
{
  "id": "deepseek-v3.2",
  "name": "DeepSeek V3.2",
  "reasoning": false,
  "input": ["text"],
  "cost": {
    "input": 0,
    "output": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  },
  "contextWindow": 128000,
  "maxTokens": 8192
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|-----|------|------|
| `id` | string | 模型 ID，用于识别模型 |
| `name` | string | 模型显示名称 |
| `reasoning` | boolean | 是否支持推理 |
| `input` | array | 支持的输入类型（`text`、`image` 等） |
| `cost` | object | 成本配置（输入、输出、缓存等） |
| `contextWindow` | number | 上下文窗口大小（token 数） |
| `maxTokens` | number | 最大输出 token 数 |

---

### 4. 环境变量配置

**环境变量文件路径**：`/root/.openclaw/.env`

```bash
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**环境变量说明**：

| 变量名 | 说明 |
|-------|------|
| `OPENAI_API_KEY` | API Key，从阿里云百炼获取 |
| `OPENAI_BASE_URL` | API 端点地址 |

---

## 测试验证

### 测试 1：查看文件结构

在云服务器上执行：

```bash
# 查看主配置文件
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 查看环境变量文件
cat ~/.openclaw/.env

# 查看模型配置文件
cat ~/.openclaw/agents/main/agent/models.json | python3 -m json.tool
```

✅ 如果所有文件都存在且格式正确，说明配置成功。

---

### 测试 2：查看模型状态

在云服务器上执行：

```bash
# 查看模型状态
openclaw models status
```

**预期结果**：
```
🦞 OpenClaw 2026.1.29 — Ship fast, log faster.

Config        : ~/.openclaw/openclaw.json
Agent dir     : ~/.openclaw/agents/main/agent
Default       : openai/deepseek-v3.2
Fallbacks (2) : openai/qwen-plus, openai/qwen-max
Image model   : -
Image fallbacks (0): -
Aliases (0)   : -
Configured models (4): openai/deepseek-v3.2, openai/qwen-plus, openai/qwen-max, openai/gpt-4o

Auth overview
Auth store    : ~/.openclaw/agents/main/agent/auth-profiles.json
Shell env     : on
Providers w/ OAuth/tokens (1): openai (1)
- openai effective=shell:OPENAI_API_KEY | profiles=0 (oauth=0, token=0, api_key=0) | openai:default=shell:OPENAI_API_KEY | source=config: ~/.openclaw/openclaw.json
```

✅ 如果看到 `Default: openai/deepseek-v3.2` 和 `Shell env: on`，说明配置成功。

---

### 测试 3：查看模型列表

在云服务器上执行：

```bash
# 查看模型列表
openclaw models list
```

**预期结果**：
```
🦞 OpenClaw 2026.1.29 — Ship fast, log faster.

Model                                      Input      Ctx      Local Auth  Tags
openai/deepseek-v3.2                       text       125k     no    yes   default,configured
openai/qwen-plus                           text       125k     no    yes   configured
openai/qwen-max                            text       125k     no    yes   configured
openai/gpt-4o                              text       125k     no    yes   configured
```

✅ 如果看到 `openai/deepseek-v3.2` 标记为 `default`，说明配置成功。

---

### 测试 4：测试对话

在云服务器上执行：

```bash
# 测试对话
openclaw agent --agent main --message "你好，请介绍一下你自己" --local
```

**预期结果**：
- AI 会回复消息，介绍自己

✅ 如果收到回复，说明模型配置成功并正常工作。

---

### 测试 5：查看网关日志

在云服务器上执行：

```bash
# 查看网关日志
tail -f /tmp/gateway.log
```

**预期结果**：
```
[gateway] agent model: openai/deepseek-v3.2
[agent/embedded] embedded run start: runId=xxx sessionId=xxx provider=openai model=deepseek-v3.2
```

✅ 如果看到 `provider=openai model=deepseek-v3.2`，说明正在使用新模型。

---

## 常见问题

### 问题 1：配置文件格式错误

**症状**��网关启动失败，提示配置文件格式错误

**解决方案**：

```bash
# 检查配置文件语法
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 如果有错误，恢复备份
cp ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json

# 重新编辑
nano ~/.openclaw/openclaw.json
```

---

### 问题 2：`models.providers.openai.models: Invalid input: expected array, received undefined`

**症状**：网关启动失败，提示 `models` 数组缺失

**原因**：`openai` provider 缺少 `models` 数组

**解决方案**：

```bash
# 编辑配置文件
nano ~/.openclaw/openclaw.json

# 确保 openai provider 包含 models 数组
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",
        "apiKey": "shell:OPENAI_API_KEY",
        "models": [...]  // ⚠️ 必须包含这个数组
      }
    }
  }
}
```

---

### 问题 3：`Unhandled API in mapOptionsForApi: undefined`

**症状**：网关启动失败，提示 API 类型未定义

**原因**：`openai` provider 缺少 `api` 字段

**解决方案**：

```bash
# 编辑配置文件
nano ~/.openclaw/openclaw.json

# 确保 openai provider 包含 api 字段
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",  // ⚠️ 必须包含这个字段
        "apiKey": "shell:OPENAI_API_KEY",
        "models": [...]
      }
    }
  }
}
```

---

### 问题 4：认证失败

**症状**：测试对话时提示认证失败

**原因**：API Key 配置不正确或环境变量未加载

**解决方案**：

```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $OPENAI_BASE_URL

# 如果环境变量为空，重新加载
source ~/.openclaw/.env

# 验证环境变量
echo $OPENAI_API_KEY
echo $OPENAI_BASE_URL

# 检查配置文件
cat ~/.openclaw/openclaw.json | grep -A 5 "openai"
```

---

### 问题 5：模型切换后仍然使用旧模型

**症状**：配置已更新，但 AI 仍使用旧模型

**原因**：网关未重启或配置未生效

**解决方案**：

```bash
# 停止网关
pkill -f clawdbot-gateway

# 重新加载环境变量
source ~/.openclaw/.env

# 启动网关
clawdbot gateway --port 18789 --verbose

# 查看日志，确认模型
tail -f /tmp/gateway.log | grep "agent model"
```

---

### 问题 6：API Key 无效

**症状**：测试对话时提示 API Key 无效

**原因**：API Key 错误或已过期

**解决方案**：

```bash
# 验证 API Key
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v3.2","messages":[{"role":"user","content":"Hello"}]}'

# 如果提示认证失败，需要重新获取 API Key
# 访问：https://dashscope.aliyun.com/
```

---

## 检查清单

### 文件结构检查清单

在开始之前，请确认以下目录和文件存在：

- [ ] `/root/.openclaw/` 主目录存在
- [ ] `/root/.openclaw/openclaw.json` 主配置文件存在
- [ ] `/root/.openclaw/.env` 环境变量文件存在
- [ ] `/root/.openclaw/agents/main/agent/models.json` 模型配置文件存在
- [ ] `/root/.openclaw/agents/main/agent/auth-profiles.json` 认证配置文件存在
- [ ] `/tmp/gateway.log` 网关日志文件存在（或可创建）

---

### 云端检查清单

- [ ] OpenClaw 已安装
- [ ] 主配置文件已备份
- [ ] 模型配置文件已备份
- [ ] 主配置文件已编辑
- [ ] Agent 默认模型已配置
- [ ] OpenAI Provider 已配置
- [ ] 模型定义数组已添加
- [ ] qwen-portal-auth 插件已禁用
- [ ] 环境变量文件已创建
- [ ] API Key 已填入
- [ ] API 端点已填入
- [ ] 旧认证信息已清理
- [ ] 网关已重启
- [ ] 环境变量已加载

---

### 功能测试检查清单

- [ ] 配置文件格式正确
- [ ] 环境变量已加载
- [ ] 网关日志显示模型配置成功
- [ ] 模型状态显示主模型为 `openai/deepseek-v3.2`
- [ ] 模型列表显示自定义模型
- [ ] 测试对话收到回复
- [ ] 网关日志显示使用新模型

---

## 总结

### 核心步骤

1. **了解文件结构**：知道配置文件和环境变量文件在哪里
2. **云端准备**：确认 OpenClaw 已安装，查看文件结构
3. **获取 API 凭证**：在阿里云百炼注册并获取 API Key
4. **编辑配置文件**：修改主配置文件，添加模型和 Provider 配置
5. **设置环境变量**：创建环境变量文件，填入 API Key
6. **重启网关**：停止旧网关，加载环境变量，启动新网关
7. **测试验证**：查看模型状态，测试对话

---

### 快速命令参考

```bash
# 查看文件结构
ls -la ~/.openclaw/
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 编辑配置
nano ~/.openclaw/openclaw.json

# 创建环境变量
nano ~/.openclaw/.env

# 验证配置
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 停止网关
pkill -f clawdbot-gateway

# 加载环境变量
source ~/.openclaw/.env

# 启动网关（前台）
clawdbot gateway --port 18789 --verbose

# 启动网关（后台）
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 查看日志
tail -f /tmp/gateway.log

# 查看模型状态
openclaw models status

# 查看模型列表
openclaw models list

# 测试对话
openclaw agent --agent main --message "测试" --local
```

---

### 文件路径速查

| 文件/目录 | 路径 |
|----------|------|
| **主配置文件** | `/root/.openclaw/openclaw.json` |
| **环境变量文件** | `/root/.openclaw/.env` |
| **模型配置文件** | `/root/.openclaw/agents/main/agent/models.json` |
| **认证配置文件** | `/root/.openclaw/agents/main/agent/auth-profiles.json` |
| **网关日志** | `/tmp/gateway.log` |

---

### 下一步建议

1. ✅ 了解文件结构
2. ✅ 获取 API 凭证
3. ✅ 编辑配置文件
4. ✅ 设置环境变量
5. ✅ 重启网关
6. ✅ 测试基础功能
7. ✅ 探索高级功能

---

**文档版本**: 2.0
**最后更新**: 2026-02-02
**适用版本**: OpenClaw 2026.1.29+
**测试环境**: OpenCloudOS, Node.js v22.22.0

---

祝您配置顺利！如有任何问题，欢迎随时咨询。🚀
