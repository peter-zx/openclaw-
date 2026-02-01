# OpenClaw 模型配置与切换完全指南

本文档详细说明如何在 OpenClaw 中识别当前模型、配置新模型提供商以及在不同平台模型间切换，特别针对阿里百炼平台的集成。

## 1. 识别当前模型配置

### 查看运行时信息
检查当前会话使用的模型：
```bash
# 查看模型信息
session_status | grep model

# 或直接检查运行时输出
# 典型输出示例：
# model=qwen-portal/vision-model
# default_model=qwen-portal/vision-model
```

### 理解模型标识
- **`qwen-portal/vision-model`**：OpenClaw 内置的 Qwen-VL（多模态视觉语言模型）别名
- **`qwen-portal/*`**：指向本地/网关托管的 Qwen 模型服务的路由前缀
- **`openai/gpt-4o`**：标准的 OpenAI API 格式

## 2. 阿里百炼平台模型配置

### 2.1 准备工作
1. 登录 [阿里云百炼控制台](https://dashscope.aliyuncs.com)
2. 获取 **API Key**（格式如：`sk-8e72d53f10f9450baab69f89a2e2b992`）
3. 确定要使用的模型：
   - `qwen-max`：最强版，128K上下文
   - `qwen-plus`：增强版，32K上下文
   - `qwen-turbo`：快速版，8K上下文
   - `qwen-vl-chat`：多模态版，支持图像理解
   - `qwen-audio`：语音模型

### 2.2 API 端点信息
```
文本生成：https://dashscope.aliyuncs.com/compatible-mode/v1
多模态：https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

### 2.3 配置方法

#### 方法一：通过 `config.patch` 注入（推荐）
```bash
clawdbot gateway config.patch --raw '{
  "models": {
    "providers": {
      "dashscope": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "sk-your-api-key-here",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-max",
            "name": "Qwen Max",
            "reasoning": false,
            "contextWindow": 128000,
            "input": ["text"]
          },
          {
            "id": "qwen-plus",
            "name": "Qwen Plus",
            "reasoning": false,
            "contextWindow": 32000
          },
          {
            "id": "qwen-vl-chat",
            "name": "Qwen VL Chat",
            "reasoning": false,
            "contextWindow": 32000,
            "input": ["text", "image"]
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "models": {
        "dashscope/qwen-max": {},
        "dashscope/qwen-plus": {},
        "dashscope/qwen-vl-chat": {}
      },
      "model": {
        "primary": "dashscope/qwen-max",
        "fallbacks": ["dashscope/qwen-plus", "dashscope/qwen-turbo"]
      }
    }
  }
}'
# 或：openclaw gateway config.patch --raw '...'
```

#### 方法二：编辑配置文件
编辑 `~/.openclaw/openclaw.json` 或 `~/.clawdbot/clawdbot.json`：
```json
{
  "models": {
    "providers": {
      "dashscope": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "${DASHSCOPE_API_KEY}",
        "api": "openai-completions"
      }
    }
  }
}
```

设置环境变量：
```bash
export DASHSCOPE_API_KEY="sk-your-api-key-here"
```

#### 方法三：使用环境变量直接配置
```bash
# 临时测试用
export OPENAI_API_KEY="sk-your-bailian-key"
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

# 然后重启网关
gateway restart
```

### 2.4 验证配置
```bash
# 验证 API Key 有效性
curl https://dashscope.aliyuncs.com/api/v1/status \
  -H "Authorization: Bearer sk-your-api-key"

# 测试模型连通性
session_status --model=dashscope/qwen-max

# 或在工具中指定模型
web_search query="测试查询" --model=dashscope/qwen-plus
```

## 3. 通用模型配置规则

### 3.1 配置要求
| 规则 | 说明 | 示例 |
|------|------|------|
| **模型别名唯一** | 每个模型必须有唯一标识 | `dashscope/qwen-max`、`openai/gpt-4o` |
| **Provider 匹配适配器** | 需使用内置支持的 provider | `openai`、`ollama`、`dashscope`、`anthropic` |
| **敏感信息保护** | API Key 避免硬编码 | 使用环境变量 `${API_KEY}` |
| **配置后验证** | 必须测试模型可用性 | `session_status --model=xxx` |

### 3.2 查看支持的 Provider
```bash
# 查看配置 schema
clawdbot gateway config.schema | grep -A 20 "models.*provider"
# 或：openclaw gateway config.schema | grep -A 20 "models.*provider"

# 或查看当前已配置的 providers
clawdbot gateway config.get models.providers
```

## 4. 切换模型完整流程

### 4.1 当当前模型 Token 用完时
```bash
# 1. 查看当前模型状态
openclaw models list
openclaw models status

# 2. 查看可用模型
clawdbot gateway config.get models.providers

# 3. 编辑配置文件
vi ~/.openclaw/openclaw.json
# 或
vi ~/.clawdbot/clawdbot.json

# 4. 添加/修改模型配置
# 参考第 2.3 节的配置示例

# 5. 重启网关服务
openclaw gateway restart
# 或
clawdbot gateway restart

# 6. 切换默认模型
openclaw models set dashscope/qwen-max

# 7. 验证切换结果
openclaw models status
session_status
```

### 4.2 快速切换脚本
创建 `switch_model.sh`：
```bash
#!/bin/bash
# 快速切换 OpenClaw 模型

MODEL_NAME=$1
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

if [ -z "$MODEL_NAME" ]; then
    echo "使用方法: $0 <模型名称>"
    echo "可用模型:"
    grep -o '"id":"[^"]*"' $CONFIG_FILE | cut -d'"' -f4
    exit 1
fi

# 更新默认模型
jq '.agents.defaults.model.primary = "'$MODEL_NAME'"' $CONFIG_FILE > /tmp/openclaw.tmp
mv /tmp/openclaw.tmp $CONFIG_FILE

# 重启网关
openclaw gateway restart

echo "✅ 已切换到模型: $MODEL_NAME"
```

## 5. 其他模型平台配置示例

### 5.1 OpenAI 兼容服务
```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "apiKey": "${OPENAI_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "reasoning": false,
            "contextWindow": 128000
          },
          {
            "id": "gpt-4-turbo",
            "name": "GPT-4 Turbo",
            "contextWindow": 128000
          }
        ]
      }
    }
  }
}
```

### 5.2 Ollama（本地部署）
```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434/api",
        "api": "ollama-completions",
        "models": [
          {
            "id": "llama3.1:latest",
            "name": "Llama 3.1",
            "reasoning": false,
            "contextWindow": 128000
          },
          {
            "id": "qwen2.5:7b",
            "name": "Qwen 2.5 7B",
            "contextWindow": 32768
          }
        ]
      }
    }
  }
}
```

### 5.3 Anthropic Claude
```json
{
  "models": {
    "providers": {
      "anthropic": {
        "baseUrl": "https://api.anthropic.com/v1",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "api": "anthropic-completions",
        "models": [
          {
            "id": "claude-3-5-sonnet-20241022",
            "name": "Claude 3.5 Sonnet",
            "reasoning": false,
            "contextWindow": 200000
          }
        ]
      }
    }
  }
}
```

## 6. 自定义模型适配器开发

### 6.1 创建插件目录结构
```bash
mkdir -p ~/.openclaw/extensions/my-model-provider
cd ~/.openclaw/extensions/my-model-provider
```

### 6.2 创建插件清单
`openclaw.plugin.json`：
```json
{
  "id": "my-model-provider",
  "name": "自定义模型提供商",
  "version": "1.0.0",
  "description": "为 OpenClaw 添加自定义模型提供商支持",
  "configSchema": {
    "type": "object",
    "properties": {
      "baseUrl": {
        "type": "string",
        "description": "API 基础 URL"
      },
      "apiKey": {
        "type": "string",
        "description": "API 密钥",
        "sensitive": true
      }
    },
    "required": ["baseUrl"]
  }
}
```

### 6.3 创建适配器实现
`index.js`：
```javascript
module.exports = {
  async init(config) {
    // 初始化逻辑
    return {
      name: config.name || '自定义模型',
      models: async () => {
        // 返回模型列表
        return [
          {
            id: 'custom-model-1',
            name: '自定义模型 1',
            capabilities: ['chat', 'completion'],
            maxTokens: 4096
          }
        ];
      },
      createCompletion: async (params) => {
        // 实现 API 调用
        const response = await fetch(`${config.baseUrl}/completions`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${config.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            model: params.model,
            messages: params.messages,
            max_tokens: params.max_tokens
          })
        });
        
        return response.json();
      }
    };
  }
};
```

## 7. 故障排除与常见问题

### 7.1 模型调用失败
```bash
# 1. 检查网络连接
curl -v https://dashscope.aliyuncs.com/api/v1/status

# 2. 验证 API Key
echo $DASHSCOPE_API_KEY

# 3. 查看网关日志
tail -f /var/log/openclaw/gateway.log

# 4. 检查模型配置
clawdbot gateway config.get models.providers.dashscope
```

### 7.2 配置不生效
```bash
# 1. 确认配置文件路径
ls -la ~/.openclaw/
ls -la ~/.clawdbot/

# 2. 重启网关服务
openclaw gateway stop
sleep 2
openclaw gateway start

# 3. 清除缓存
rm -rf ~/.openclaw/cache/*

# 4. 检查版本兼容性
openclaw --version
gateway --version
```

### 7.3 多模态模型问题
```bash
# 1. 确认模型支持多模态
clawdbot gateway config.get models.providers.dashscope.models

# 2. 测试图片上传
clawdbot session_status --model=dashscope/qwen-vl-chat --image /path/to/image.jpg

# 3. 检查文件大小限制
# 通常限制：20MB 以内，支持 JPG/PNG/WebP
```

## 8. 最佳实践

### 8.1 安全建议
1. **使用环境变量**存储 API Key
2. **定期轮换** API 密钥
3. **限制权限**，按需分配模型访问
4. **记录审计日志**，跟踪模型使用情况

### 8.2 性能优化
1. **设置合理的超时时间**
2. **启用模型缓存**（如支持）
3. **使用连接池**管理 API 连接
4. **监控 Token 使用**，避免超额

### 8.3 配置管理
1. **版本控制**配置文件
2. **分离环境配置**（开发/测试/生产）
3. **定期备份**重要配置
4. **文档化**自定义模型配置

## 9. 快速参考命令

```bash
# 模型管理
openclaw models list                  # 列出所有模型
openclaw models set <model-id>        # 设置默认模型
openclaw models status                # 查看模型状态

# 网关管理
openclaw gateway restart              # 重启网关
openclaw gateway logs                 # 查看日志
openclaw gateway config.get <path>    # 获取配置
openclaw gateway config.patch         # 更新配置

# 会话测试
session_status --model=<model-id>     # 测试特定模型
session_status --verbose              # 详细输出
```

## 10. 总结

通过本文档，你可以：

1. **识别**当前 OpenClaw 使用的模型
2. **配置**阿里百炼等第三方模型平台
3. **切换**不同模型提供商
4. **开发**自定义模型适配器
5. **解决**配置过程中的常见问题

建议按照以下顺序操作：
1. 先验证当前模型配置
2. 准备新模型的 API 凭证
3. 使用 `config.patch` 或编辑配置文件添加新模型
4. 重启网关服务
5. 测试新模型可用性
6. 切换默认模型（可选）

遇到问题时，参考第 7 节故障排除指南，或检查网关日志获取详细错误信息。