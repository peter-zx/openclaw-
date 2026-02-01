# Clawdbot 自定义 API 与大模型配置指南

本文档详细说明如何在 Clawdbot 中配置和使用自定义 API 及大模型，包括阿里百炼、DeepSeek、Qwen 等第三方模型。

## 目录

- [1. 配置概述](#1-配置概述)
- [2. 配置文件结构](#2-配置文件结构)
- [3. 配置自定义模型](#3-配置自定义模型)
  - [3.1 阿里百炼（DeepSeek、Qwen 等）](#31-阿里百炼deepseekqwen-等)
  - [3.2 使用别名机制](#32-使用别名机制)
  - [3.3 配置多个模型和备用模型](#33-配置多个模型和备用模型)
- [4. 环境变量配置](#4-环境变量配置)
- [5. 认证配置](#5-认证配置)
- [6. 网关管理与启动](#6-网关管理与启动)
- [7. 测试与验证](#7-测试与验证)
- [8. 故障排除](#8-故障排除)
- [9. 完整示例脚本](#9-完整示例脚本)

## 1. 配置概述

Clawdbot 的主要配置文件位于：
- `~/.clawdbot/clawdbot.json` – 主配置文件
- `~/.clawdbot/.env` – 环境变量文件（可选，但推荐）

配置的核心部分在 `agents.defaults` 中，包括：
- `model.primary` – 主模型标识符
- `model.fallbacks` – 备用模型列表（主模型失败时自动切换）
- `models` – 模型定义映射（可包含别名、参数等）
- `workspace` – 工作目录

模型通过 **provider** 机制进行抽象，Clawdbot 内置了 `openai`、`anthropic`、`qwen-portal` 等 provider。自定义 API 通常通过 `openai` provider 的兼容模式实现。

## 2. 配置文件结构

以下是最简配置文件结构：

```json
{
  "meta": { ... },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai/deepseek-v3.2",
        "fallbacks": ["openai/qwen-plus", "openai/qwen-max"]
      },
      "models": {
        "openai/deepseek-v3.2": {},
        "openai/qwen-plus": {},
        "openai/qwen-max": {},
        "openai/gpt-4o": {}
      },
      "workspace": "/root/clawd"
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback"
  },
  "plugins": {
    "entries": {
      "feishu": { "enabled": true },
      "qwen-portal-auth": { "enabled": false }
    }
  },
  "models": {
    "providers": {}
  },
  "auth": {
    "profiles": {}
  }
}
```

## 3. 配置自定义模型

### 3.1 阿里百炼（DeepSeek、Qwen 等）

阿里百炼提供了 OpenAI 兼容的 API 端点，可以通过 `openai` provider 使用。

**关键配置步骤：**

1. **设置主模型**：使用 `openai/deepseek-v3.2` 等标识符
2. **定义模型映射**：在 `agents.defaults.models` 中添加对应条目
3. **配置环境变量**：设置 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`

**示例配置（Python 脚本）：**

```python
import json

config_path = '/root/.clawdbot/clawdbot.json'
with open(config_path, 'r') as f:
    data = json.load(f)

# 1. 设置主模型和备用模型
data['agents']['defaults']['model']['primary'] = 'openai/deepseek-v3.2'
data['agents']['defaults']['model']['fallbacks'] = [
    'openai/qwen-plus',
    'openai/qwen-max'
]

# 2. 定义模型映射（使用 openai provider）
data['agents']['defaults']['models'] = {
    'openai/deepseek-v3.2': {},
    'openai/qwen-plus': {},
    'openai/qwen-max': {},
    'openai/gpt-4o': {}
}

# 3. 移除 qwen-portal provider（避免冲突）
if 'models' in data and 'providers' in data['models']:
    data['models']['providers'].pop('qwen-portal', None)

# 4. 禁用 qwen-portal-auth 插件
if 'plugins' in data and 'entries' in data['plugins']:
    data['plugins']['entries']['qwen-portal-auth'] = {'enabled': False}

# 5. 写入配置文件
with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)

# 6. 创建环境变量文件
env_path = '/root/.clawdbot/.env'
env_content = """OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
"""
with open(env_path, 'w') as f:
    f.write(env_content)

print('✅ 配置完成')
```

### 3.2 使用别名机制

如果需要使用自定义模型名称，可以通过别名指向实际的 provider 模型。

**示例：将自定义名称 `deepseek-v3.2` 映射到 `openai/gpt-4o`**

```python
import json

with open('/root/.clawdbot/clawdbot.json','r') as f:
    data = json.load(f)

data['agents']['defaults']['model']['primary'] = 'deepseek-v3.2'
data['agents']['defaults']['models'] = {
    'deepseek-v3.2': {
        'alias': 'openai/gpt-4o'  # 实际使用 OpenAI provider
    }
}

with open('/root/.clawdbot/clawdbot.json','w') as f:
    json.dump(data, f, indent=2)

print('✅ 别名配置完成')
```

**工作原理：**
1. Clawdbot 收到 `deepseek-v3.2` 请求
2. 通过别名解析为 `openai/gpt-4o`
3. OpenAI provider 从环境变量读取 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`
4. 发送请求到阿里云兼容端点，阿里云根据 API Key 识别实际模型

### 3.3 配置多个模型和备用模型

备用模型在主模型不可用时自动使用，按列表顺序尝试。

```python
# 配置多个模型和备用链
data['agents']['defaults']['model']['primary'] = 'openai/deepseek-v3.2'
data['agents']['defaults']['model']['fallbacks'] = [
    'openai/qwen-plus',   # 第一备用
    'openai/qwen-max',    # 第二备用
    'openai/gpt-4o'       # 第三备用
]

data['agents']['defaults']['models'] = {
    'openai/deepseek-v3.2': {},
    'openai/qwen-plus': {},
    'openai/qwen-max': {},
    'openai/gpt-4o': {}
}
```

## 4. 环境变量配置

环境变量是配置 API 密钥和端点的推荐方式。

**`~/.clawdbot/.env` 文件示例：**

```bash
# 阿里百炼配置
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 其他 provider 配置（可选）
ANTHROPIC_API_KEY=your_anthropic_key
COHERE_API_KEY=your_cohere_key
```

**通过命令行设置：**

```bash
export OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
export OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

## 5. 认证配置

如果使用 OAuth 或其他认证方式，需要在 `auth.profiles` 中配置。

**清理残留的 Qwen OAuth 配置：**

```python
# 移除 qwen-portal auth profiles
if 'auth' in data and 'profiles' in data['auth']:
    keys_to_remove = [k for k in data['auth']['profiles'] if k.startswith('qwen-portal:')]
    for k in keys_to_remove:
        del data['auth']['profiles'][k]
    print(f'已移除 {len(keys_to_remove)} 个 qwen-portal auth profiles')
```

## 6. 网关管理与启动

### 6.1 启动网关

```bash
# 简单启动（默认端口 18789）
clawdbot gateway --local --port 18789

# 详细日志模式
clawdbot gateway --local --port 18789 --verbose

# 后台运行
nohup clawdbot gateway --port 18789 --verbose &
```

### 6.2 停止网关

```bash
# 停止系统服务
clawdbot gateway stop

# 或手动终止进程
pkill -f clawdbot-gateway
```

### 6.3 检查网关状态

```bash
# 检查端口监听
netstat -tulpn | grep 18789

# 检查进程
ps aux | grep -E 'clawdbot|gateway' | grep -v grep
```

## 7. 测试与验证

### 7.1 测试模型配置

```bash
# 测试主模型
export OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
export OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
clawdbot agent --agent main --message "你好" --local

# 测试备用模型（强制使用备用）
clawdbot agent --agent main --message "你好" --local --model openai/qwen-plus
```

### 7.2 验证配置

```bash
# 查看当前配置
cat ~/.clawdbot/clawdbot.json | jq '.agents.defaults.model'
cat ~/.clawdbot/clawdbot.json | jq '.agents.defaults.models'
```

## 8. 故障排除

### 8.1 常见问题

#### 问题：模型切换后仍然使用旧模型
**解决：**
1. 重启网关使配置生效
2. 检查是否有残留的 provider 配置
3. 确认环境变量已正确设置

#### 问题：OAuth 认证残留导致冲突
**解决：**
1. 禁用 `qwen-portal-auth` 插件
2. 清理 `auth.profiles` 中的 qwen-portal 条目
3. 移除 `models.providers` 中的 qwen-portal 配置

#### 问题：网关启动失败
**解决：**
1. 检查端口是否被占用：`lsof -i :18789`
2. 查看日志：`tail -f /tmp/gateway.log`
3. 使用 `--verbose` 模式启动获取详细错误信息

### 8.2 配置检查清单

- [ ] `clawdbot.json` 语法正确（可通过 `jq . clawdbot.json` 验证）
- [ ] 主模型和备用模型在 `models` 映射中有定义
- [ ] 无冲突的 provider 配置
- [ ] 环境变量文件存在且内容正确
- [ ] 网关进程正在运行
- [ ] 端口监听正常

## 9. 完整示例脚本

以下是一个完整的配置脚本，包含所有必要步骤：

```python
#!/usr/bin/env python3
"""
Clawdbot 阿里百炼模型完整配置脚本
"""

import json
import os

def configure_clawdbot():
    # 配置文件路径
    config_path = '/root/.clawdbot/clawdbot.json'
    
    # 读取现有配置
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    print('当前配置:')
    print(f"主模型: {data['agents']['defaults']['model'].get('primary', '未设置')}")
    print(f"备用模型: {data['agents']['defaults']['model'].get('fallbacks', [])}")
    
    # 1. 设置主模型和备用模型
    data['agents']['defaults']['model']['primary'] = 'openai/deepseek-v3.2'
    data['agents']['defaults']['model']['fallbacks'] = [
        'openai/qwen-plus',
        'openai/qwen-max',
        'openai/gpt-4o'
    ]
    
    # 2. 定义模型映射
    data['agents']['defaults']['models'] = {
        'openai/deepseek-v3.2': {},
        'openai/qwen-plus': {},
        'openai/qwen-max': {},
        'openai/gpt-4o': {}
    }
    
    # 3. 清理 Qwen 相关配置
    if 'models' in data and 'providers' in data['models']:
        data['models']['providers'].pop('qwen-portal', None)
    
    if 'plugins' in data and 'entries' in data['plugins']:
        data['plugins']['entries']['qwen-portal-auth'] = {'enabled': False}
    
    if 'auth' in data and 'profiles' in data['auth']:
        keys_to_remove = [k for k in data['auth']['profiles'] if k.startswith('qwen-portal:')]
        for k in keys_to_remove:
            del data['auth']['profiles'][k]
    
    # 4. 写入配置文件
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    # 5. 创建环境变量文件
    env_path = '/root/.clawdbot/.env'
    env_content = """# 阿里百炼配置
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
"""
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    # 6. 输出配置摘要
    print('\n' + '='*70)
    print('✅ Clawdbot 配置已更新')
    print('='*70)
    print(f"主模型: {data['agents']['defaults']['model']['primary']}")
    print(f"备用模型: {data['agents']['defaults']['model']['fallbacks']}")
    print(f"可用模型: {list(data['agents']['defaults']['models'].keys())}")
    print('\n环境变量:')
    print(f"OPENAI_API_KEY: sk-8e72d53f10f9450baab69f89a2e2b992")
    print(f"OPENAI_BASE_URL: https://dashscope.aliyuncs.com/compatible-mode/v1")
    print('\n下一步:')
    print('1. 重启网关: clawdbot gateway stop; nohup clawdbot gateway --port 18789 --verbose &')
    print('2. 测试配置: clawdbot agent --agent main --message "测试" --local')
    print('='*70)

if __name__ == '__main__':
    configure_clawdbot()
```

## 总结

通过以上配置，你可以：
1. 使用阿里百炼的免费模型（DeepSeek、Qwen 等）
2. 配置多个模型和自动故障转移
3. 管理认证和插件配置
4. 启动和监控网关服务

关键点：
- 使用 `openai` provider 的兼容模式对接第三方 API
- 通过环境变量管理敏感信息
- 定期清理不需要的配置避免冲突
- 重启网关使配置生效

如有问题，请检查日志文件并参考故障排除部分。