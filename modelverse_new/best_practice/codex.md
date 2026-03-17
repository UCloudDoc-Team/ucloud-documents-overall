## OpenAI Codex 接入指南

> 现在你可以通过 [UModelverse 平台](https://console.ucloud.cn/modelverse/model-center) 使用 `gpt-5.1-codex` 等模型。

## 🚀 快速入门

### 1. 安装

1. 请确保您已安装 npm，请参考 [Node.js 官方网站](https://nodejs.org/zh-cn/download)。

2. 安装 OpenAI Codex：

```shell
npm install -g @openai/codex@latest
```

### 2. 配置

#### 2.1 配置模型提供商

在 Mac 或 Linux 环境下创建并配置您的 `~/.codex/config.toml` 文件：

```toml
model_provider = "ucloud"
model_reasoning_effort = "high"
model = "gpt-5.1-codex"

[model_providers.ucloud]
name = "ucloud"
base_url = "https://api.modelverse.cn/v1"
wire_api = "responses"
requires_openai_auth = true
```

#### 2.2 配置 API Key

创建并配置您的 `~/.codex/auth.json` 文件：

```json
{
  "OPENAI_API_KEY": "your-umodelverse-api-key"
}
```

> **注意**: 请将 `your-umodelverse-api-key` 替换为您在 UModelverse 平台获取的实际 API Key。

### 3. 使用 Codex

配置完成后，您可以直接在终端中运行 Codex：

```shell
codex
```

您可以通过 `/model`来切换模型，如图所示：
![codex-model](https://static.ucloud.cn/docs/modelverse/images/codex/codex.png)
您也可以在配置后直接安装`codex` VS Code 插件，并切换模型和推理强度进行使用。
![codex-vscode](https://static.ucloud.cn/docs/modelverse/images/codex/codex-vscode.png)

