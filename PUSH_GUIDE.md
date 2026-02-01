# 推送到 GitHub 操作指南

## 当前状态

✅ Git 仓库已初始化
✅ 10 个 Markdown 文件已提交到本地
✅ 远程仓库已配置：`https://github.com/peter-zx/openclaw-.git`
❌ 文件尚未推送到远程仓库

---

## 推送方法（按推荐顺序）

### 方法 1：使用 VSCode 图形界面（最简单）

1. **打开 VSCode**
2. **打开文件夹**: `Cmd+O` → 选择 `/Users/admin/Desktop/moltbot`
3. **点击左侧源代码管理图标**（或按 `Cmd+Shift+G`）
4. **点击"..."菜单** → 选择"推送"（Push）
5. **VSCode 会弹出 GitHub 登录窗口**
6. **完成登录后，推送会自动完成**

---

### 方法 2：使用 VSCode 命令面板

1. **打开 VSCode**
2. **打开文件夹**: `/Users/admin/Desktop/moltbot`
3. **按 `Cmd+Shift+P` 打开命令面板**
4. **输入**: `Git: Push`
5. **按回车执行**
6. **在弹出的认证窗口中完成登录**

---

### 方法 3：使用终端 + GitHub Personal Access Token

#### 步骤 1：生成 Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 勾选权限：
   - `repo` (完整仓库访问权限)
   - `workflow` (GitHub Actions)
4. 点击 **Generate token**
5. **复制生成的 token**（只显示一次，请妥善保存）

#### 步骤 2：使用 Token 推送

```bash
cd /Users/admin/Desktop/moltbot
git push -u origin main
```

当提示输入用户名和密码时：
- **Username**: `peter-zx`
- **Password**: 粘贴刚才生成的 Personal Access Token

---

### 方法 4：使用 Git Credential Manager

#### 步骤 1：安装 Git Credential Manager

```bash
# 下载并安装
curl -L https://aka.ms/gcm/osx/install.sh | sh
```

#### 步骤 2：配置 Git

```bash
git config --global credential.helper manager-core
```

#### 步骤 3：推送

```bash
cd /Users/admin/Desktop/moltbot
git push -u origin main
```

会弹出浏览器窗口，完成 GitHub 登录即可。

---

### 方法 5：使用 GitHub CLI (gh)

#### 步骤 1：安装 Homebrew（如果未安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 步骤 2：安装 GitHub CLI

```bash
brew install gh
```

#### 步骤 3：登录 GitHub

```bash
gh auth login
```

按照提示选择：
- What account do you want to log into? → `GitHub.com`
- What is your preferred protocol for Git operations? → `HTTPS`
- Authenticate Git with your GitHub credentials? → `Yes`
- How would you like to authenticate GitHub CLI? → `Login with a web browser`

#### 步骤 4：推送代码

```bash
cd /Users/admin/Desktop/moltbot
git push -u origin main
```

---

## 验证推送成功

推送成功后，访问：https://github.com/peter-zx/openclaw-

您应该能看到 10 个 Markdown 文件：

1. `Clawdbot插件系统总结.md`
2. `OpenClaw_常用命令速查指南.md`
3. `OpenClaw_模型配置与切换指南.md`
4. `clawdbot_custom_models_guide.md`
5. `clawdbot_deployment_guide.md`
6. `clawdbot_plugins_and_cross_device_guide.md`
7. `修复配置脚本.md`
8. `如何切换自定义大模型使用API.md`
9. `服务器状态分析报告.md`
10. `配置阿里云百炼模型指南.md`

---

## 故障排除

### 问题：推送失败，提示认证错误

**解决方案**：
- 确保在 VSCode 中已登录 GitHub
- 或使用 Personal Access Token
- 或安装 Git Credential Manager

### 问题：提示仓库不存在

**解决方案**：
- 确认仓库 URL 正确：`https://github.com/peter-zx/openclaw-.git`
- 确认仓库已在 GitHub 上创建

### 问题：推送后远程仓库仍为空

**解决方案**：
```bash
cd /Users/admin/Desktop/moltbot
git status
git log --oneline
git remote -v
```

检查是否有提交，远程地址是否正确。

---

## 快速命令参考

```bash
# 查看当前状态
cd /Users/admin/Desktop/moltbot
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 推送到远程
git push -u origin main

# 查看推送状态
git push --dry-run origin main
```

---

## 推荐方案

**最简单**：方法 1（VSCode 图形界面）
**最可靠**：方法 4（Git Credential Manager）
**最灵活**：方法 3（Personal Access Token）

选择适合您的方法即可！
