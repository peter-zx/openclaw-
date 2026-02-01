# 如何切换自定义大模型使用API

## 概述

本文档详细说明如何在 OpenClaw/Clawdbot 中切换到自定义大模型（如阿里云百炼的 deepseek-v3.2），通过 API 方式调用第三方大语言模型。

## 前置条件

- ✅ 已安装 OpenClaw/Clawdbot（版本 2026.1.29+）
- ✅ 已获取第三方 API Key（如阿里云百炼）
- ✅ Node.js v22.22.0+
- ✅ Python 3（用于配置脚本）

---

## 核心原理

OpenClaw 通过 **Provider 机制** 对接不同的大模型 API。自定义模型通常通过 `openai` provider 的兼容模式实现，因为大多数第三方 API 都提供了 OpenAI 兼容接口。

### 关键配置字段

```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",  // API 端点
        "api": "openai-completions",                                      // API 类型
        "apiKey": "shell:OPENAI_API_KEY",                                 // 认证方式
        "models": [...]                                                    // 模型定义数组
      }
    }
  }
}
```

---

## 完整配置步骤

### 步骤 1：准备配置脚本

创建 Python 脚本来自动化配置过程：

```bash
cat > ~/setup_custom_model.py << 'EOF'
#!/usr/bin/env python3
import json
import os

config_path = os.path.expanduser('~/.openclaw/openclaw.json')
env_path = os.path.expanduser('~/.openclaw/.env')

# 读取配置
with open(config_path, 'r') as f:
    data = json.load(f)

print('当前配置:')
print(f"主模型: {data['agents']['defaults']['model'].get('primary', '未设置')}")
print(f"备用模型: {data['agents']['defaults']['model'].get('fallbacks', [])}")

# 1. 设置主模型和备用模型
data['agents']['defaults']['model']['primary'] = 'openai/deepseek-v3.2'
data['agents']['defaults']['model']['fallbacks'] = [
    'openai/qwen-plus',
    'openai/qwen-max'
]

# 2. 定义模型映射
data['agents']['defaults']['models'] = {
    'openai/deepseek-v3.2': {},
    'openai/qwen-plus': {},
    'openai/qwen-max': {},
    'openai/gpt-4o': {}
}

# 3. 配置 openai provider（关键步骤）
if 'models' not in data:
    data['models'] = {}
if 'providers' not in data['models']:
    data['models']['providers'] = {}

data['models']['providers']['openai'] = {
    'baseUrl': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'api': 'openai-completions',           # ⚠️ 必需：指定 API 类型
    'apiKey': 'shell:OPENAI_API_KEY',     # ⚠️ 必需：从环境变量读取
    'models': [                            # ⚠️ 必需：模型定义数组
        {
            "id": "deepseek-v3.2",
            "name": "DeepSeek V3.2",
            "reasoning": False,
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
            "reasoning": False,
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
            "reasoning": False,
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
            "reasoning": False,
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

# 4. 禁用 qwen-portal-auth 插件（避免冲突）
if 'plugins' not in data:
    data['plugins'] = {}
if 'entries' not in data['plugins']:
    data['plugins']['entries'] = {}
data['plugins']['entries']['qwen-portal-auth'] = {'enabled': False}

# 5. 清理 qwen-portal 认证（避免冲突）
if 'auth' in data and 'profiles' in data['auth']:
    keys_to_remove = [k for k in data['auth']['profiles'] if k.startswith('qwen-portal:')]
    for k in keys_to_remove:
        del data['auth']['profiles'][k]
    if keys_to_remove:
        print(f'已移除 {len(keys_to_remove)} 个 qwen-portal auth profiles')

# 6. 保存配置文件
with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)

# 7. 创建环境变量文件
with open(env_path, 'w') as f:
    f.write('OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')  # 替换为你的 API Key
    f.write('OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1\n')

# 8. 输出配置摘要
print('\n' + '='*70)
print('✅ 自定义模型配置已更新')
print('='*70)
print(f"主模型: {data['agents']['defaults']['model']['primary']}")
print(f"备用模型: {data['agents']['defaults']['model']['fallbacks']}")
print(f"可用模型: {list(data['agents']['defaults']['models'].keys())}")
print('\n环境变量:')
print(f"OPENAI_API_KEY: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(f"OPENAI_BASE_URL: https://dashscope.aliyuncs.com/compatible-mode/v1")
print('\n下一步:')
print('1. 编辑 ~/.openclaw/.env，填入真实的 API Key')
print('2. 停止网关: pkill -f clawdbot-gateway')
print('3. 加载环境变量: source ~/.openclaw/.env')
print('4. 启动网关: clawdbot gateway --port 18789 --verbose')
print('5. 验证配置: openclaw models status')
print('='*70)
EOF

python3 ~/setup_custom_model.py
```

---

### 步骤 2：编辑环境变量文件

```bash
# 编辑环境变量文件
vi ~/.openclaw/.env
```

将 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 替换为你的真实 API Key：

```bash
# 阿里云百炼配置
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

---

### 步骤 3：停止现有网关

```bash
# 查找并停止网关进程
ps aux | grep clawdbot
pkill -f clawdbot-gateway

# 或使用命令
clawdbot gateway stop 2>/dev/null || true
```

---

### 步骤 4：加载环境变量

```bash
# 加载环境变量
source ~/.openclaw/.env

# 验证环境变量
echo "OPENAI_API_KEY: $OPENAI_API_KEY"
echo "OPENAI_BASE_URL: $OPENAI_BASE_URL"
```

---

### 步骤 5：启动网关

```bash
# 前台运行（查看日志）
clawdbot gateway --port 18789 --verbose

# 或后台运行
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &
```

---

### 步骤 6：验证配置

```bash
# 查看模型状态
openclaw models status

# 查看模型列表
openclaw models list

# 测试对话
openclaw agent --agent main --message "你好，请介绍一下你自己" --local
```

---

## 关键配置详解

### 1. Agent 默认模型配置

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai/deepseek-v3.2",      // 主模型
        "fallbacks": [                          // 备用模型列表
          "openai/qwen-plus",
          "openai/qwen-max"
        ]
      },
      "models": {                                // 模型映射
        "openai/deepseek-v3.2": {},
        "openai/qwen-plus": {},
        "openai/qwen-max": {},
        "openai/gpt-4o": {}
      }
    }
  }
}
```

**说明**：
- `primary`: 默认使用的模型
- `fallbacks`: 主模型失败时自动切换的备用模型
- `models`: 所有可用模型的映射表

---

### 2. OpenAI Provider 配置（核心）

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

**关键字段说明**：

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

## 常见问题与解决方案

### 问题 1：`models.providers.openai.models: Invalid input: expected array, received undefined`

**原因**：`openai` provider 缺少 `models` 数组

**解决**：
```python
data['models']['providers']['openai']['models'] = [...]
```

---

### 问题 2：`Unhandled API in mapOptionsForApi: undefined`

**原因**：`openai` provider 缺少 `api` 字段

**解决**：
```python
data['models']['providers']['openai']['api'] = 'openai-completions'
```

---

### 问题 3：认证失败

**原因**：`apiKey` 配置不正确或环境变量未加载

**解决**：
```python
data['models']['providers']['openai']['apiKey'] = 'shell:OPENAI_API_KEY'
```

然后确保环境变量已加载：
```bash
source ~/.openclaw/.env
echo $OPENAI_API_KEY
```

---

### 问题 4：网关启动失败

**原因**：配置文件语法错误或端口被占用

**解决**：
```bash
# 检查配置文件语法
cat ~/.openclaw/openclaw.json | python3 -m json.tool

# 检查端口占用
lsof -i :18789

# 使用 verbose 模式查看详细错误
clawdbot gateway --port 18789 --verbose
```

---

### 问题 5：模型切换后仍然使用旧模型

**原因**：网关未重启或配置未生效

**解决**：
```bash
# 停止网关
pkill -f clawdbot-gateway

# 重新加载环境变量
source ~/.openclaw/.env

# 启动网关
clawdbot gateway --port 18789 --verbose
```

---

## 配置检查清单

在完成配置后，请确认以下项：

- [ ] 配置文件 `~/.openclaw/openclaw.json` 已更新
- [ ] 主模型设置为 `openai/deepseek-v3.2`
- [ ] 备用模型已配置
- [ ] `openai` provider 包含 `api` 字段
- [ ] `openai` provider 包含 `models` 数组
- [ ] `openai` provider 的 `apiKey` 设置为 `shell:OPENAI_API_KEY`
- [ ] 环境变量文件 `~/.openclaw/.env` 已创建
- [ ] `OPENAI_API_KEY` 已设置为真实值
- [ ] `OPENAI_BASE_URL` 已设置
- [ ] qwen-portal-auth 插件已禁用
- [ ] qwen-portal 认证已清理
- [ ] 网关已重启
- [ ] 模型列表中显示自定义模型
- [ ] 测试对话成功

---

## 完整一键脚本

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "配置自定义大模型（阿里云百炼）"
echo "=========================================="

# 1. 创建配置脚本
cat > ~/setup_custom_model.py << 'PYEOF'
#!/usr/bin/env python3
import json
import os

config_path = os.path.expanduser('~/.openclaw/openclaw.json')
env_path = os.path.expanduser('~/.openclaw/.env')

with open(config_path, 'r') as f:
    data = json.load(f)

data['agents']['defaults']['model']['primary'] = 'openai/deepseek-v3.2'
data['agents']['defaults']['model']['fallbacks'] = ['openai/qwen-plus', 'openai/qwen-max']
data['agents']['defaults']['models'] = {
    'openai/deepseek-v3.2': {},
    'openai/qwen-plus': {},
    'openai/qwen-max': {},
    'openai/gpt-4o': {}
}

if 'models' not in data:
    data['models'] = {}
if 'providers' not in data['models']:
    data['models']['providers'] = {}

data['models']['providers']['openai'] = {
    'baseUrl': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'api': 'openai-completions',
    'apiKey': 'shell:OPENAI_API_KEY',
    'models': [
        {
            "id": "deepseek-v3.2",
            "name": "DeepSeek V3.2",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 128000,
            "maxTokens": 8192
        },
        {
            "id": "qwen-plus",
            "name": "Qwen Plus",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 128000,
            "maxTokens": 8192
        },
        {
            "id": "qwen-max",
            "name": "Qwen Max",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 128000,
            "maxTokens": 8192
        },
        {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "reasoning": False,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
            "contextWindow": 128000,
            "maxTokens": 8192
        }
    ]
}

if 'plugins' not in data:
    data['plugins'] = {}
if 'entries' not in data['plugins']:
    data['plugins']['entries'] = {}
data['plugins']['entries']['qwen-portal-auth'] = {'enabled': False}

if 'auth' in data and 'profiles' in data['auth']:
    keys_to_remove = [k for k in data['auth']['profiles'] if k.startswith('qwen-portal:')]
    for k in keys_to_remove:
        del data['auth']['profiles'][k]

with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)

with open(env_path, 'w') as f:
    f.write('OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992\n')
    f.write('OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1\n')

print('✅ 配置完成')
PYEOF

# 2. 执行配置脚本
python3 ~/setup_custom_model.py

# 3. 停止网关
echo "停止网关..."
pkill -f clawdbot-gateway
sleep 2

# 4. 加载环境变量
echo "加载环境变量..."
source ~/.openclaw/.env

# 5. 启动网关
echo "启动网关..."
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &
sleep 3

# 6. 验证配置
echo "=========================================="
echo "验证配置..."
echo "=========================================="
openclaw models status

echo ""
echo "=========================================="
echo "✅ 配置完成！"
echo "=========================================="
echo "查看网关日志: tail -f /tmp/gateway.log"
echo "测试对话: openclaw agent --agent main --message \"测试\" --local"
echo "=========================================="
```

---

## 配置文件位置汇总

| 配置项 | 路径 |
|-------|------|
| 主配置文件 | `~/.openclaw/openclaw.json` |
| 环境变量文件 | `~/.openclaw/.env` |
| Agent 目录 | `~/.openclaw/agents/main/agent` |
| 认证配置 | `~/.openclaw/agents/main/agent/auth-profiles.json` |
| 网关日志 | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |

---

## 支持的第三方 API

### 阿里云百炼

```json
{
  "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "api": "openai-completions",
  "apiKey": "shell:OPENAI_API_KEY"
}
```

### 其他 OpenAI 兼容接口

大多数提供 OpenAI 兼容接口的第三方服务都可以使用相同的方式配置，只需修改 `baseUrl` 和 `apiKey`。

---

## 总结

### 核心要点

1. **使用 `openai` provider**：通过 OpenAI 兼容模式对接第三方 API
2. **必须配置三个关键字段**：
   - `api`: `openai-completions`
   - `apiKey`: `shell:OPENAI_API_KEY`
   - `models`: 模型定义数组
3. **环境变量管理**：API Key 通过环境变量传递，更安全
4. **清理冲突配置**：禁用其他 provider 的认证，避免冲突
5. **重启网关生效**：配置修改后必须重启网关

### 快速命令速查

```bash
# 配置模型
python3 ~/setup_custom_model.py

# 停止网关
pkill -f clawdbot-gateway

# 加载环境变量
source ~/.openclaw/.env

# 启动网关
clawdbot gateway --port 18789 --verbose

# 验证配置
openclaw models status

# 测试对话
openclaw agent --agent main --message "测试" --local
```

---

**文档版本**: 1.0
**最后更新**: 2026-02-02
**适用版本**: OpenClaw 2026.1.29+
**测试环境**: OpenCloudOS, Node.js v22.22.0
