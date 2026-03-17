# Kimi K2 × Claude Code 接入指南

由于 Claude Code 在使用时不兼容 OpenAI 格式的请求，所以需要一个代理应用做转发，这里以 [claude-code-proxy](https://github.com/fuergaosi233/claude-code-proxy) 举例。

---

## 环境准备

- Ubuntu 24.04 操作系统

---

## 安装 ClaudeCode

```bash
# 确保已经安装了 npm
npm install -g @anthropic-ai/claude-code
```

## 安装 ClaudeCodeProxy
### 克隆项目到本地：
```bash
git clone https://github.com/fuergaosi233/claude-code-proxy
cd claude-code-proxy
```
### 安装依赖：
```bash
# 安装 uv（已经安装可以忽略）：
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync
```
## 修改配置
```bash
cp .env.example .env

# 编辑配置文件
vim .env
```
![](https://www-s.ucloud.cn/2025/07/682ae34721e558e2efc06c524918a37d_1752663308311.PNG)
需要修改的配置，以 moonshotai/Kimi-K2-Instruct 模型为例：

| 设置项 | 描述 |
|---|---|
| OPENAL_API_KEY | [API Key管理](https://console.ucloud.cn/modelverse/experience/api-keys)|
| ANTHROPIC_API_KEY | 需要注释掉这一行 |
| OPENAL_BASE_URL | https://api.modelverse.cn |
| BIG_MODEL | moonshotai/Kimi-K2-Instruct |
| MIDDLE_MODEL | moonshotai/Kimi-K2-Instruct |
| SMALL_MODEL | moonshotai/Kimi-K2-Instruct |

## 启动代理
1. 临时启动
```bash
uv run start_proxy.py
```
![](https://www-s.ucloud.cn/2025/07/8ea6f9445e9e7e17680d9436e1d0de1f_1752663621261.PNG)
2. Docker 后台运行
ClaudeCodeProxy 提供了 Dockerfile，能够以容器的方式后台运行代理服务：
```bash
# 编译镜像（确保安装了docker）
docker build -t claude-code-proxy:latest .

# 启动
docker run -d --name claude-code-proxy -p 8082:8082 claude-code-proxy
```
## 运行 Claude
启动代理成功后，执行下面的命令：
```bash
# ANTHROPIC_BASE_URL 转发到本地代理，ANTHROPIC_AUTH_TOKEN 绕过登录认证
ANTHROPIC_BASE_URL=http://localhost:8082 ANTHROPIC_AUTH_TOKEN="any-value" claude
```
![](https://www-s.ucloud.cn/2025/07/d83ee6721ce78781b3f520746134ea52_1752663621267.png)
![](https://www-s.ucloud.cn/2025/07/1aa0ed407af02576155d6e68a8c05347_1752663621269.png)
