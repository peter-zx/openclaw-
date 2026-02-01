# Clawdbot 插件系统总结文档

## 概述

Clawdbot（也称为moltbot或openclaw）是一个支持多模型、多频道的AI助手平台，可以通过插件系统扩展功能。本文档总结了Clawdbot插件系统的核心知识经验。

## 目录

- [插件安装机制](#插件安装机制)
- [插件配置格式](#插件配置格式)
- [插件管理命令](#插件管理命令)
- [插件安装工作流](#插件安装工作流)
- [插件加载与执行](#插件加载与执行)
- [安装速度优化](#安装速度优化)
- [示例插件](#示例插件)
- [注意事项](#注意事项)

---

## 插件安装机制

Clawdbot的插件系统基于npm包管理，插件以npm包的形式发布和安装。

### 插件命名规范

插件包使用`@m1heng-clawd/`命名空间前缀：
```
@m1heng-clawd/feishu
@m1heng-clawd/其他插件名
```

### 安装方式

#### 方式一：使用clawdbot命令（推荐）
```bash
clawdbot plugins install @m1heng-clawd/feishu
```

#### 方式二：使用openclaw命令（部分环境）
```bash
openclaw plugins install @m1heng-clawd/feishu
```

#### 方式三：直接使用npm安装
```bash
npm install @m1heng-clawd/feishu
```

---

## 插件配置格式

插件配置存储在主配置文件`~/.clawdbot/clawdbot.json`中。

### 配置结构

```json
{
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      },
      "qwen-portal-auth": {
        "enabled": false
      }
    }
  }
}
```

### 配置说明

- `plugins.entries`: 插件条目字典
- `enabled`: 插件启用状态（`true`/`false`）
- 插件名称：使用短名称（如`feishu`），而非完整的npm包名

---

## 插件管理命令

### 插件相关命令

```bash
# 安装插件
clawdbot plugins install <plugin-name>

# 添加/配置频道（可能使用插件）
clawdbot channels add

# 列出已配置的频道
clawdbot channels list

# 移除频道
clawdbot channels remove <channel-name>

# 查看频道配置
clawdbot channels show <channel-name>
```

### 网关管理命令

```bash
# 启动网关（前台运行，查看日志）
clawdbot gateway --local --port 18789 --verbose

# 启动网关（后台运行）
nohup clawdbot gateway --local --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 停止网关
clawdbot gateway stop

# 手动终止网关进程
pkill -f clawdbot-gateway
```

### 配置管理命令

```bash
# 运行交互式配置向导
clawdbot configure

# 查看版本
clawdbot --version

# 查看帮助
clawdbot --help
clawdbot gateway --help
```

---

## 插件安装工作流

以飞书插件为例，完整的插件安装流程如下：

### 标准安装流程

```bash
# 步骤1：安装插件
clawdbot plugins install @m1heng-clawd/feishu

# 步骤2：停止现有网关（如果正在运行）
clawdbot gateway stop

# 步骤3：启动网关（临时测试）
clawdbot gateway --local --port 18789 --verbose

# 步骤4：重新进入通道配置菜单
clawdbot channels add
```

### 配置文件编辑

在`clawdbot.json`中添加飞书配置：

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

### 飞书应用配置

在飞书开放平台完成以下配置：

1. **权限管理**：添加`im:message`、`im:message.group_at_msg`等权限
2. **事件订阅**：添加`im.message.receive_v1`事件
3. **回调URL**：`http://你的服务器IP:18789/feishu/events`
4. **安全设置**：添加加密密钥（如需）

### 重启并验证

```bash
# 停止现有网关
clawdbot gateway stop

# 持久化启动网关（后台运行）
nohup clawdbot gateway --local --port 18789 --verbose > /tmp/gateway.log 2>&1 &

# 查看日志，确认飞书插件加载
tail -f /tmp/gateway.log
```

---

## 插件加载与执行

### 加载机制

- 插件安装后自动被Clawdbot检测
- 插件系统自动处理依赖下载
- 插件需要在配置文件中启用才能生效

### 执行要求

- 插件安装后必须重启网关才能生效
- 网关启动时会加载所有已启用的插件
- 插件功能通过频道系统暴露给用户

### 生命周期

```
安装 → 配置 → 重启网关 → 使用
```

---

## 安装速度优化

如果`npm install`命令执行缓慢，可以使用以下方法提速。

### 方案一：使用国内镜像（推荐）

```bash
# 临时使用淘宝镜像
npm install @m1heng-clawd/feishu --registry=https://registry.npmmirror.com

# 永久设置镜像源
npm config set registry https://registry.npmmirror.com
npm config set maxsockets 10
npm set progress=false

# 或使用cnpm（淘宝官方客户端）
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install @m1heng-clawd/feishu
```

### 方案二：使用更快的包管理器

```bash
# 使用yarn
npm install -g yarn
yarn add @m1heng-clawd/feishu

# 或使用pnpm
npm install -g pnpm
pnpm add @m1heng-clawd/feishu
```

### 方案三：优化npm配置

```bash
# 使用离线模式（如果已有缓存）
npm install @m1heng-clawd/feishu --prefer-offline

# 清理并重建缓存
npm cache clean --force
npm install @m1heng-clawd/feishu
```

---

## 示例插件

### 飞书插件（Feishu）

**插件名称**：`@m1heng-clawd/feishu`

**功能**：集成飞书（Lark）消息平台，支持群聊@机器人交互

**配置示例**：
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "your_app_id",
      "appSecret": "your_app_secret"
    }
  },
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  }
}
```

### Qwen Portal认证插件

**插件名称**：`qwen-portal-auth`

**功能**：提供Qwen Portal的OAuth认证

**禁用示例**：
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

## 注意事项

### 1. 配置文件位置

- 主配置文件：`~/.clawdbot/clawdbot.json`
- 环境变量文件：`~/.clawdbot/.env`

### 2. 网关重启

- 插件安装后必须重启网关
- 配置修改后必须重启网关
- 使用`clawdbot gateway stop`或`pkill -f clawdbot-gateway`停止

### 3. 端口管理

- 默认端口：`18789`
- 检查端口占用：`lsof -i :18789`
- 更换端口：`clawdbot gateway --local --port 18790`

### 4. 日志查看

```bash
# 查看网关日志
tail -f /tmp/gateway.log

# 查看系统日志（systemd）
sudo journalctl -u clawdbot -f

# 查看PM2日志
pm2 logs clawdbot
```

### 5. 故障排除

#### 问题：插件安装后菜单中看不到选项

**解决**：按照标准安装流程执行4个步骤
```bash
clawdbot plugins install @m1heng-clawd/feishu
clawdbot gateway stop
clawdbot gateway --local --port 18789 --verbose
clawdbot channels add
```

#### 问题：网关启动失败

**解决**：
```bash
# 检查端口占用
lsof -i :18789

# 停止冲突进程
kill -9 <PID>

# 使用verbose模式查看详细错误
clawdbot gateway --local --port 18789 --verbose
```

#### 问题：飞书消息不回复

**解决**：
```bash
# 检查飞书插件状态
grep -i feishu /tmp/gateway.log

# 验证回调URL可达性
curl -X POST http://localhost:18789/feishu/events \
  -H "Content-Type: application/json" \
  -d '{"test":"event"}'
```

---

## 配置检查清单

在部署插件系统前，确保以下项已完成：

- [ ] Node.js 24+ 已安装
- [ ] Clawdbot 已全局安装
- [ ] 配置文件`~/.clawdbot/clawdbot.json`存在
- [ ] 插件通过npm成功安装
- [ ] 插件在配置文件中已启用
- [ ] 网关进程正在运行
- [ ] 端口18789（或自定义端口）监听正常
- [ ] 环境变量文件`.env`配置正确（如需要）
- [ ] 防火墙已开放相应端口

---

## 总结

Clawdbot插件系统是一个基于npm的模块化扩展机制，具有以下特点：

1. **简单易用**：通过单一命令即可安装插件
2. **配置驱动**：所有插件配置集中在JSON文件中
3. **自动管理**：插件系统自动处理依赖和加载
4. **灵活扩展**：支持多种频道和功能扩展

### 核心命令速查

```bash
# 安装插件
clawdbot plugins install @m1heng-clawd/feishu

# 配置频道
clawdbot channels add

# 启动网关
clawdbot gateway --local --port 18789 --verbose

# 停止网关
clawdbot gateway stop
```

### 相关文档

- 部署指南：`clawdbot_deployment_guide.md`
- 自定义模型配置：`clawdbot_custom_models_guide.md`

---

**文档版本**：1.0
**最后更新**：2026-02-01
**适用版本**：Clawdbot 2026.1.24-3+
