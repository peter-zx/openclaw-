# Clawdbot/OpenClaw 插件系统与跨设备控制实战指南

本文档整合 Clawdbot/OpenClaw 的插件安装逻辑、跨设备控制方案及自定义模型配置，提供可直接落地的实操命令和经验总结。

## 🎯 核心概念

### 插件是什么？
- **插件 = npm 包**，遵循标准 npm 规范
- 扩展 Clawdbot/OpenClaw 功能：频道集成、节点控制、模型适配等
- 安装在 `~/.clawdbot/plugins/` 或 `~/.openclaw/plugins/` 目录

### 三种扩展类型
1. **频道插件**：办公软件集成，如 `@m1heng-clawd/feishu`（飞书）
2. **节点插件**：跨设备控制，如 `openclaw-node`（远程控制客户端）
3. **模型适配器**：通过配置对接第三方模型，如阿里百炼、DeepSeek

## 📦 插件安装全方案

### 方案一：标准安装（网络正常）
```bash
# 使用 clawdbot 命令（推荐）
clawdbot plugins install @m1heng-clawd/feishu

# 使用 openclaw 命令（旧版兼容）
openclaw plugins install @m1heng-clawd/feishu
```

### 方案二：手动下载安装（网络受限/离线）
```bash
# 1. 下载插件包
curl -O https://registry.npmjs.org/@m1heng-clawd/feishu/-/feishu-0.1.3.tgz

# 2. 本地安装
clawdbot plugins install ./feishu-0.1.3.tgz
```

### 方案三：项目隔离安装（推荐用于多环境）
```bash
# 1. 创建隔离环境脚本（如已存在 install-openclaw-isolated.sh）
# 2. 运行隔离安装
cd /Users/admin/Desktop/moltbot
./install-openclaw-isolated.sh

# 3. 激活隔离环境
source ./.openclaw-isolated/env.sh

# 4. 在隔离环境中安装插件
clawdbot plugins install @m1heng-clawd/feishu
```

### 方案四：国内网络优化
```bash
# 临时使用淘宝镜像
npm install @m1heng-clawd/feishu --registry=https://registry.npmmirror.com

# 永久设置镜像源
npm config set registry https://registry.npmmirror.com
npm config set maxsockets 10
npm set progress=false

# 或使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install @m1heng-clawd/feishu
```

## 🌐 跨设备控制：云服务器 → 本地 MacBook Air

### 场景描述
- **控制端**：腾讯云服务器上的 OpenClaw
- **被控端**：本地 MacBook Air
- **目标**：通过安全通道远程执行命令、访问文件、屏幕录制等

### 实施步骤

#### 第一步：在被控端（MacBook Air）安装节点客户端
```bash
# 1. 确保 Node.js ≥ 20.x
node -v
# 如未安装：brew install node 或从 https://nodejs.org/ 下载

# 2. 全局安装 openclaw-node
npm install -g openclaw-node

# 3. 启动节点等待配对
openclaw-node start
# 输出示例：
# 🔐 Waiting for pairing... Please run `nodes approve <CODE>` in your main session.
# 记下 6 位配对码（如 A7B2C9）
```

#### 第二步：在控制端（云服务器）批准配对
```bash
# 在 OpenClaw 会话中执行
clawdbot nodes approve A7B2C9
# 或：openclaw nodes approve A7B2C9
# 成功响应：✅ Node 'MacBook-Air' paired successfully. Status: online
```

#### 第三步：验证和控制
```bash
# 查看已配对节点
clawdbot nodes status
# 或：openclaw nodes status

# 查看节点详情
clawdbot nodes describe MacBook-Air

# 基础命令测试
clawdbot nodes run MacBook-Air -- pwd
clawdbot nodes run MacBook-Air -- ls -la ~/Downloads

# 文件操作
clawdbot nodes run MacBook-Air -- cat ~/Documents/todo.md
clawdbot nodes run MacBook-Air -- echo "测试" > ~/Desktop/test.txt

# 屏幕录制（2秒）
clawdbot nodes screen_record MacBook-Air --durationMs 2000 --outPath /tmp/mac_screen.png

# 摄像头拍照
clawdbot nodes camera_snap MacBook-Air --facing back --outPath /tmp/mac_cam.jpg
```

### 安全说明
- 配对码一次性有效，需手动确认
- 通信使用 TLS + JWT 鉴权
- 敏感操作（删除文件等）仍需授权
- 可随时解除配对：`nodes reject <node-id>`

## 🤖 自定义模型配置（阿里百炼示例）

### 配置原理
通过修改 `~/.clawdbot/clawdbot.json` 配置文件，实现模型路由和适配。

### 快速配置脚本
创建 `setup_alibaba.py`：
```python
#!/usr/bin/env python3
import json
import os

config_path = '/root/.clawdbot/clawdbot.json'
with open(config_path, 'r') as f:
    data = json.load(f)

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

# 3. 清理残留配置
if 'models' in data and 'providers' in data['models']:
    data['models']['providers'].pop('qwen-portal', None)

if 'plugins' in data and 'entries' in data['plugins']:
    data['plugins']['entries']['qwen-portal-auth'] = {'enabled': False}

# 4. 保存配置
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

print('✅ 阿里百炼模型配置完成')
```

### 执行配置
```bash
# 1. 运行配置脚本
python3 setup_alibaba.py

# 2. 设置环境变量（如脚本未自动创建）
export OPENAI_API_KEY=sk-xxxxxx
export OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 3. 重启网关使配置生效
clawdbot gateway stop
nohup clawdbot gateway --port 18789 --verbose &
```

### 测试模型
```bash
# 测试主模型
clawdbot agent --agent main --message "你好" --local

# 测试备用模型
clawdbot agent --agent main --message "你好" --local --model openai/qwen-plus
```

## 🔧 插件管理命令

### 查看与维护
```bash
# 列出已安装插件
clawdbot plugins list

# 查看插件详情
clawdbot plugins info @m1heng-clawd/feishu

# 更新插件
clawdbot plugins update @m1heng-clawd/feishu

# 卸载插件
clawdbot plugins remove @m1heng-clawd/feishu
```

### 网关管理
```bash
# 启动网关（前台，查看日志）
clawdbot gateway --local --port 18789 --verbose

# 后台运行
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 停止网关
clawdbot gateway stop

# 检查状态
ps aux | grep -E 'clawdbot|gateway' | grep -v grep
netstat -tulpn | grep 18789
```

## 🚨 故障排除

### 常见问题与解决方案

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| **网关启动失败** | 端口占用或权限不足 | `lsof -i :18789` 查看占用，`kill -9 <PID>` 或更换端口 |
| **插件安装缓慢** | 网络超时或下载慢 | 使用国内镜像，或手动下载 .tgz 文件本地安装 |
| **模型调用失败** | API 密钥错误或网络问题 | 验证环境变量：`echo $OPENAI_API_KEY`，手动测试 API 连接 |
| **跨设备配对失败** | 配对码无效或网络不通 | 检查被控端防火墙，确认网关 URL 可达性 |
| **配置不生效** | 修改后仍用旧配置 | 重启网关：`clawdbot gateway stop; nohup ... &` |

### 日志查看
```bash
# 网关日志
tail -f /var/log/clawdbot_gateway.log
tail -f /tmp/gateway.log

# 系统服务日志（如使用 systemd）
sudo journalctl -u clawdbot -f

# 检查特定插件加载
grep -i feishu /var/log/clawdbot.log
```

## 📋 一键部署脚本示例

### 完整环境搭建脚本 `deploy_clawdbot.sh`
```bash
#!/bin/bash
# Clawdbot 环境一键部署脚本

set -e

echo "🚀 开始部署 Clawdbot 环境..."

# 1. 安装 Node.js（如未安装）
if ! command -v node &> /dev/null; then
    echo "📦 安装 Node.js 24..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    source ~/.bashrc
    nvm install 24
    nvm use 24
fi

# 2. 安装 Clawdbot
echo "📦 安装 Clawdbot..."
npm install -g clawdbot

# 3. 运行初始配置
echo "⚙️ 运行初始配置向导..."
clawdbot configure <<< "y
/root/clawd
local
18789
n
"

# 4. 安装飞书插件
echo "📱 安装飞书插件..."
clawdbot plugins install @m1heng-clawd/feishu

# 5. 配置阿里百炼模型
echo "🤖 配置阿里百炼模型..."
python3 << 'EOF'
import json
config_path = '/root/.clawdbot/clawdbot.json'
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
with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)
print('✅ 模型配置完成')
EOF

# 6. 创建环境变量文件
echo "🔑 创建环境变量文件..."
cat > /root/.clawdbot/.env << 'EOF'
# 阿里百炼配置
OPENAI_API_KEY=sk-8e72d53f10f9450baab69f89a2e2b992
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
EOF

# 7. 启动网关
echo "🚪 启动网关服务..."
nohup clawdbot gateway --port 18789 --verbose > /var/log/clawdbot_gateway.log 2>&1 &

echo "✅ 部署完成！"
echo "📊 检查服务状态："
ps aux | grep clawdbot | grep -v grep
echo "📝 查看日志：tail -f /var/log/clawdbot_gateway.log"
echo "🧪 测试命令：clawdbot agent --agent main --message '测试' --local"
```

## 🎯 最佳实践总结

### 安装策略选择
- **测试环境**：使用项目隔离安装，避免污染系统
- **生产环境**：全局安装 + systemd 服务管理
- **国内网络**：配置 npm 镜像源，或手动下载安装包

### 跨设备控制流程
1. **准备阶段**：确保被控端已安装 Node.js 和 openclaw-node
2. **配对阶段**：启动节点 → 获取配对码 → 云端批准
3. **测试阶段**：基础命令测试 → 文件操作 → 高级功能
4. **安全阶段**：定期检查配对节点，及时解除无用连接

### 模型配置要点
1. **清理冲突**：禁用 qwen-portal-auth 插件，移除残留 provider
2. **环境变量**：敏感信息通过 .env 文件管理，避免硬编码
3. **备用链**：配置主备模型，确保服务高可用
4. **验证测试**：配置后务必测试模型可用性

### 运维监控
- **日志轮转**：配置 logrotate 防止日志文件过大
- **健康检查**：定期 curl http://localhost:18789/health
- **资源监控**：关注内存使用，特别是多模型并发时
- **备份策略**：定期备份 `~/.clawdbot/` 配置目录

## 📚 相关资源

### 官方文档
- Clawdbot 官方文档（如提供）
- OpenClaw 安装脚本：https://openclaw.ai/install.sh

### 插件仓库
- 飞书插件：`@m1heng-clawd/feishu`
- 节点客户端：`openclaw-node`

### 模型服务
- 阿里百炼：https://dashscope.aliyuncs.com
- 通义千问模型系列

### 社区支持
- GitHub Issues（如开源）
- 官方技术社区或论坛

---

**文档版本**：v1.1  
**更新日期**：2026年2月1日  
**适用版本**：Clawdbot/OpenClaw ≥ v0.12  
**编写目的**：整合实操经验，提供可直接复用的部署方案

> 💡 **提示**：部署前请根据实际环境调整路径、端口和 API 密钥。建议先在测试环境验证，再部署到生产环境。