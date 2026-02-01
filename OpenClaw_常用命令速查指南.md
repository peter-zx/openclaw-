# OpenClaw/Clawdbot 常用命令速查指南

本文档汇总 OpenClaw/Clawdbot 的日常操作命令，按功能分类组织，便于快速查阅和执行。

## 📋 快速导航

| 类别 | 主要命令 | 用途 |
|------|----------|------|
| 🔍 **系统状态** | `session_status`, `models list` | 查看运行状态和模型信息 |
| 🤖 **模型管理** | `models set`, `models status` | 切换、查看模型配置 |
| ⚙️ **配置管理** | `configure`, `config.patch` | 修改系统配置 |
| 📦 **插件管理** | `plugins install`, `plugins list` | 安装、管理插件 |
| 🚪 **网关控制** | `gateway restart`, `gateway stop` | 启停网关服务 |
| 🌐 **跨设备控制** | `nodes approve`, `nodes run` | 远程设备管理 |
| 🔍 **端口检查** | `lsof`, `netstat`, `curl` | 检查服务状态 |
| 🛠️ **故障排查** | 日志查看、缓存清理 | 问题诊断与修复 |

---

## 🚨 重要：命令调用方式

**核心规则**：`clawdbot`（或 `openclaw`）是主程序，其他所有功能都是其子命令。  
**错误示例**：直接运行 `session_status`、`gateway`、`nodes` 等会得到 `command not found` 错误。  
**正确调用**：必须通过主命令调用，格式为 `clawdbot <子命令>` 或 `openclaw <子命令>`。

### ✅ 正确示例
```bash
# 查看会话状态
clawdbot session_status
openclaw session_status

# 管理网关
clawdbot gateway --version
clawdbot gateway restart

# 节点管理
clawdbot nodes approve A7B2C9
clawdbot nodes status
```

### ❌ 错误示例
```bash
session_status                 # 错误：直接运行子命令
gateway --version              # 错误：直接运行子命令
nodes approve A7B2C9          # 错误：直接运行子命令
```

### 🔍 验证命令是否存在
```bash
# 检查主命令
which clawdbot
which openclaw

# 查看所有可用子命令
clawdbot --help
openclaw --help
```

> 💡 **提示**：本文档后续所有命令示例均假定您已理解此规则，并会正确使用 `clawdbot` 或 `openclaw` 前缀。部分示例可能为简洁省略前缀，但实际执行时请务必加上。

## 🔍 系统状态与信息查看

### 会话状态
```bash
# 查看当前会话状态
clawdbot session_status
# 或：openclaw session_status

# 查看详细运行时信息（包含模型、配置等）
clawdbot session_status --verbose

# 仅查看模型信息
clawdbot session_status | grep model

# 查看模型标识
# 典型输出示例：
# model=qwen-portal/vision-model
# default_model=qwen-portal/vision-model
```

### 版本信息
```bash
# 查看各组件版本
openclaw --version
clawdbot --version
clawdbot gateway --version
# 或：openclaw gateway --version

# 查看 Node.js 版本（依赖检查）
node -v
npm -v
```

---

## 🤖 模型管理

### 模型列表与状态
```bash
# 列出所有可用模型
openclaw models list
clawdbot models list

# 查看当前模型状态
openclaw models status
clawdbot models status

# 查看模型配置详情
clawdbot gateway config.get models.providers
# 或：openclaw gateway config.get models.providers
```

### 模型切换
```bash
# 设置默认模型
openclaw models set <模型ID>
clawdbot models set <模型ID>

# 示例：切换到阿里百炼 Qwen-Max
openclaw models set dashscope/qwen-max

# 示例：切换到 OpenAI GPT-4o
openclaw models set openai/gpt-4o
```

### 模型测试
```bash
# 测试特定模型
session_status --model=<模型ID>

# 示例：测试阿里百炼 Qwen-Plus
session_status --model=dashscope/qwen-plus

# 示例：测试多模态模型
session_status --model=dashscope/qwen-vl-chat --image /path/to/image.jpg
```

---

## ⚙️ 配置管理

### 交互式配置
```bash
# 启动交互式配置向导
clawdbot configure
openclaw configure

# 按向导提示设置：
# 1. 工作目录（默认：/root/clawd）
# 2. 网关类型（本地/远程）
# 3. 网关端口（默认：18789）
# 4. 是否启用调试模式
```

### 配置文件操作
```bash
# 查看完整配置
clawdbot gateway config.get
# 或：openclaw gateway config.get

# 查看特定配置项
clawdbot gateway config.get models.providers.dashscope
clawdbot gateway config.get agents.defaults.model

# 更新配置（推荐方式）
clawdbot gateway config.patch --raw '{"字段": "值"}'

# 示例：修改默认模型
clawdbot gateway config.patch --raw '{
  "agents": {
    "defaults": {
      "model": {
        "primary": "dashscope/qwen-max"
      }
    }
  }
}'

# 直接编辑配置文件
vi ~/.clawdbot/clawdbot.json
vi ~/.openclaw/openclaw.json
```

### 环境变量配置
```bash
# 设置 API Key 环境变量
export DASHSCOPE_API_KEY="sk-your-api-key-here"
export OPENAI_API_KEY="sk-your-openai-key"

# 设置 API 端点
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

# 持久化到配置文件
echo 'export DASHSCOPE_API_KEY="sk-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📦 插件管理

### 插件安装
```bash
# 安装插件（标准方式）
clawdbot plugins install <插件名>
openclaw plugins install <插件名>

# 示例：安装飞书插件
clawdbot plugins install @m1heng-clawd/feishu

# 本地安装插件包
clawdbot plugins install ./feishu-0.1.3.tgz

# 国内网络优化安装
npm install @m1heng-clawd/feishu --registry=https://registry.npmmirror.com
```

### 插件管理
```bash
# 列出已安装插件
clawdbot plugins list
openclaw plugins list

# 查看插件详细信息
clawdbot plugins info @m1heng-clawd/feishu

# 更新插件
clawdbot plugins update @m1heng-clawd/feishu

# 卸载插件
clawdbot plugins remove @m1heng-clawd/feishu
```

---

## 🚪 网关与服务控制

### 网关启停
```bash
# 启动网关（前台运行，查看日志）
clawdbot gateway --local --port 18789 --verbose
openclaw gateway --local --port 18789 --verbose

# 启动网关（后台运行）
nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &
nohup openclaw gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 停止网关
clawdbot gateway stop
openclaw gateway stop

# 重启网关
clawdbot gateway restart
openclaw gateway restart
```

### 服务状态检查
```bash
# 查看网关进程
ps aux | grep -E 'clawdbot|openclaw|gateway' | grep -v grep

# 健康检查
curl http://localhost:18789/health
curl http://localhost:18789/status

# 查看网关配置
clawdbot gateway config.get gateway
# 或：openclaw gateway config.get gateway
```

### 日志管理
```bash
# 实时查看日志
tail -f /tmp/gateway.log
tail -f /var/log/clawdbot_gateway.log

# 查看最后100行日志
tail -n 100 /tmp/gateway.log

# 搜索特定错误
grep -i error /tmp/gateway.log
grep -i "failed" /var/log/clawdbot_gateway.log
```

---

## 🌐 跨设备节点控制

### 节点配对流程
```bash
# 在被控端（如 MacBook）启动节点
openclaw-node start
# 输出：🔐 Waiting for pairing... Please run `nodes approve <CODE>`
# 记下 6 位配对码（如 A7B2C9）

# 在主控端（如云服务器）批准配对
clawdbot nodes approve A7B2C9
# 或：openclaw nodes approve A7B2C9
# 成功响应：✅ Node 'MacBook-Air' paired successfully. Status: online
```

### 节点管理
```bash
# 查看所有节点状态
clawdbot nodes status
# 或：openclaw nodes status

# 查看特定节点详情
clawdbot nodes describe MacBook-Air
clawdbot nodes describe node-id-123

# 拒绝/解除节点配对
clawdbot nodes reject MacBook-Air
clawdbot nodes reject <节点ID>
```

### 远程执行命令
```bash
# 在远程节点执行命令
clawdbot nodes run <节点名> -- <命令>
# 或：openclaw nodes run <节点名> -- <命令>

# 示例：查看远程节点当前目录
clawdbot nodes run MacBook-Air -- pwd

# 示例：查看远程文件
clawdbot nodes run MacBook-Air -- ls -la ~/Downloads

# 示例：创建远程文件
clawdbot nodes run MacBook-Air -- echo "测试内容" > ~/Desktop/test.txt

# 示例：查看文件内容
clawdbot nodes run MacBook-Air -- cat ~/Documents/todo.md
```

### 高级功能
```bash
# 屏幕录制（2秒）
clawdbot nodes screen_record MacBook-Air --durationMs 2000 --outPath /tmp/mac_screen.png
# 或：openclaw nodes screen_record MacBook-Air ...

# 摄像头拍照
clawdbot nodes camera_snap MacBook-Air --facing back --outPath /tmp/mac_cam.jpg

# 连续执行多个命令
clawdbot nodes run MacBook-Air -- "cd /tmp && mkdir test && ls -la"
```

---

## 🔍 端口与网络检查

### 端口占用检查
```bash
# 检查网关端口（默认18789）
lsof -i :18789
lsof -i :18789 | grep LISTEN

# 使用 netstat 检查
netstat -tulpn | grep 18789
netstat -tulpn | grep -E "18789|gateway"

# 使用 ss 检查（现代替代）
ss -tulpn | grep 18789
```

### 网络连通性
```bash
# 检查本地服务
curl -v http://localhost:18789/health
curl -s http://localhost:18789/status | jq .

# 检查外部 API 连通性
curl -v https://dashscope.aliyuncs.com/api/v1/status
curl -s https://dashscope.aliyuncs.com/api/v1/status -H "Authorization: Bearer sk-your-key"

# 测试延迟
ping -c 4 dashscope.aliyuncs.com
```

### 进程资源检查
```bash
# 查看进程资源占用
top -o cpu | grep -E "clawdbot|openclaw"
htop

# 查看特定进程
ps aux | grep clawdbot | grep -v grep
ps -ef | grep gateway

# 查看内存使用
free -h
vmstat 1 5

# 查看磁盘空间
df -h
du -sh ~/.clawdbot/
```

---

## 🛠️ 故障排查与维护

### 常见问题诊断
```bash
# 1. 网关启动失败
lsof -i :18789                     # 检查端口占用
kill -9 <占用PID>                   # 强制结束占用进程
clawdbot gateway restart --port 18888  # 更换端口启动

# 2. 模型调用失败
echo $DASHSCOPE_API_KEY            # 检查 API Key
curl https://dashscope.aliyuncs.com/api/v1/status -H "Authorization: Bearer sk-your-key"
clawdbot gateway config.get models.providers.dashscope  # 检查配置

# 3. 插件加载失败
clawdbot plugins list              # 检查插件状态
ls -la ~/.clawdbot/plugins/        # 检查插件目录
tail -f /tmp/gateway.log | grep -i plugin  # 查看插件日志
```

### 缓存与数据清理
```bash
# 清理缓存
rm -rf ~/.clawdbot/cache/*
rm -rf ~/.openclaw/cache/*

# 清理临时文件
rm -f /tmp/gateway.log
rm -f /tmp/clawdbot_*.log

# 清理下载的插件包
rm -f ~/Downloads/*.tgz
```

### 日志分析技巧
```bash
# 查看最近错误
tail -n 50 /tmp/gateway.log | grep -E "error|failed|exception" -i

# 查看特定时间段的日志
grep "2025-01-" /tmp/gateway.log | head -20

# 统计错误次数
grep -c "error" /tmp/gateway.log

# 查看插件相关日志
grep -i "plugin\|@m1heng" /var/log/clawdbot_gateway.log
```

---

## ⚡ 快速操作组合

### 环境检查三步曲
```bash
# 一键检查版本、状态、进程
openclaw --version && session_status && ps aux | grep gateway
```

### 重启服务并监控
```bash
# 停止、启动、查看日志
clawdbot gateway stop && sleep 2 && nohup clawdbot gateway --port 18789 --verbose > /tmp/gateway.log 2>&1 && tail -f /tmp/gateway.log
```

### 切换模型并验证
```bash
# 切换模型后立即测试
openclaw models set dashscope/qwen-max && clawdbot session_status --model=dashscope/qwen-max
```

### 节点连接与测试
```bash
# 连接节点并执行测试命令
clawdbot nodes approve A7B2C9 && sleep 1 && clawdbot nodes run MacBook-Air -- "uname -a && date"
```

---

## 📚 使用提示与最佳实践

### 命令选择指南
- **`clawdbot` vs `openclaw`**：两者通常可以互换，`clawdbot` 是新版推荐
- **`gateway` 命令**：用于网关配置和管理，不影响当前会话
- **`session_` 命令**：用于当前会话的操作和状态查看

### 配置文件位置
```bash
# 主要配置文件
~/.clawdbot/clawdbot.json          # 新版推荐
~/.openclaw/openclaw.json          # 旧版兼容

# 插件目录
~/.clawdbot/plugins/
~/.openclaw/plugins/

# 缓存目录
~/.clawdbot/cache/
~/.openclaw/cache/

# 日志文件
/tmp/gateway.log
/var/log/clawdbot_gateway.log
```

### 端口配置
- **默认网关端口**：18789
- **节点通信端口**：动态分配（通常 30000+）
- **修改端口**：在配置中设置或启动时指定 `--port <端口号>`

### 故障检查顺序
1. **`clawdbot session_status`** - 检查当前会话状态
2. **`ps aux | grep gateway`** - 检查网关进程是否存在
3. **`lsof -i :18789`** - 检查端口是否被占用
4. **`tail -f /tmp/gateway.log`** - 查看实时错误日志
5. **`clawdbot gateway config.get`** - 检查当前配置是否正确

### 安全注意事项
1. **API Key 保护**：使用环境变量，避免硬编码在配置文件中
2. **节点配对**：仅批准可信设备的配对请求
3. **端口暴露**：生产环境避免将网关端口暴露到公网
4. **日志清理**：定期清理包含敏感信息的日志文件

---

**文档版本**：v1.1  
**更新日期**：2026年2月1日  
**适用版本**：OpenClaw/Clawdbot ≥ v0.12  
**编写目的**：提供日常操作的快速命令参考，提高运维效率

> 💡 **提示**：建议将此文档与《插件系统与跨设备控制指南》、《模型配置与切换指南》结合使用，形成完整的技术文档体系。