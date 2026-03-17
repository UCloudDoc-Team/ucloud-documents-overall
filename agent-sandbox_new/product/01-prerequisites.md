# 前置条件与认证

<subtitle>开始使用 SDK/CLI 前需要完成的准备工作：获取 API Key 与配置环境变量。</subtitle>

本页统一说明 UCloud Sandbox 的认证配置。后续文档将不再重复此内容。

---

## 获取 API Key

前往控制台获取您的 API 密钥：

?> [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys)

---

## 原生 SDK 配置

使用 UCloud Sandbox 原生 Python SDK 时，请配置 `AGENTBOX_API_KEY` 环境变量：

```bash
export AGENTBOX_API_KEY=your_api_key
```

配置完成后即可使用 SDK：

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create(timeout=60)
print(sandbox.sandbox_id)
```

---

## E2B 兼容模式配置

如果您使用 E2B SDK 以兼容模式接入 UCloud Sandbox，请配置以下环境变量：

```bash
# 设置 UCloud Sandbox 域名
export E2B_DOMAIN=sandbox.ucloudai.com

# 设置您的 API Key
export E2B_API_KEY=your_api_key
```

!> **注意**：E2B 兼容模式与原生 SDK 使用**不同的环境变量**，请勿混用。

配置完成后，您可以直接使用 E2B SDK：

```python
from e2b_code_interpreter import Sandbox

sbx = Sandbox.create()
```

---

## CLI 配置

CLI 优先读取环境变量中的 API Key，也支持交互式登录：

```bash
# 方式一：环境变量（推荐）
export AGENTBOX_API_KEY=your_api_key

# 方式二：交互式登录
ucloud-sandbox-cli auth login
```

---

## 下一步

- [SDK 快速开始](/agent-sandbox/docs/sdk/00-quick-start) - 创建第一个沙箱
- [CLI 指南](/agent-sandbox/docs/cli/cli) - 命令行工具使用
- [E2B 兼容模式](/agent-sandbox/docs/sdk/e2b-compatibility) - 迁移现有 E2B 代码
