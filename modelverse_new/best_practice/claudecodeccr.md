## Claude Code x Claude Code Router 接入指南


> 现在你可以通过[UModelverse平台](https://console.ucloud.cn/modelverse/model-center)使用`GLM-4.5`、`Kimi-K2`、`Qwen3-Coder-480B-A35B`、`DeepSeek v3.1`等模型。          


## 🚀 快速入门
### 1. 安装

1. 请确保您已安装 npm, 请参考 [Node.js官方网站](https://nodejs.org/zh-cn/download)。

2. 安装[Claude Code](https://docs.anthropic.com/en/docs/claude-code/quickstart)：

```shell
npm install -g @anthropic-ai/claude-code
```

3. 安装 Claude Code Router：

```shell
npm install -g @musistudio/claude-code-router
```

### 2. 配置

在 Mac 或 Linux 环境下创建并配置您的 `~/.claude-code-router/config.json` 文件。

这是一个综合示例：

```json
{
  "APIKEY": "sk-your-umodelverse-api-key", // 填写您的UModelverse的api-key
  "PROXY_URL": "",
  "LOG": false,
  "API_TIMEOUT_MS": 600000,
  "NON_INTERACTIVE_MODE": false,
  "Providers": [
    {
      "name": "ucloud",
      "api_base_url": "https://api.modelverse.cn/v1/chat/completions",
      "api_key": "sk-your-umodelverse-api-key", // 填写您的UModelverse的api-key
      "models": [
        "openai/gpt-4.1",
        "deepseek-ai/DeepSeek-V3.1",
        "Qwen/Qwen3-32B",
        "openai/gpt-5",
        "zai-org/glm-4.5v",
        "openai/gpt-5-mini",
        "Qwen/Qwen3-30B-A3B",
        "ByteDance/doubao-seed-1.6",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "grok-4",
        "gpt-4.1-mini",
        "claude-4-opus",
        "gemini-2.5-pro",
        "claude-4-sonnet",
        "gemini-2.5-flash",
        "ByteDance/doubao-seed-1.6-thinking",
        "ByteDance/doubao-1.5-thinking-vision-pro",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "zai-org/glm-4.5",
        "Qwen/Qwen3-Coder",
        "moonshotai/Kimi-K2-Instruct",
        "deepseek-ai/DeepSeek-R1-0528",
        "deepseek-ai/DeepSeek-V3-0324",
        "Qwen/Qwen3-235B-A22B",
        "Qwen/QwQ-32B",
        "deepseek-ai/DeepSeek-Prover-V2-671B",
        "qwen/qwen2.5-vl-72b-instruct",
        "deepseek-ai/DeepSeek-R1"
      ]
    }
  ],
  "Router": {
    "default": "ucloud,claude-4-sonnet",
    "background": "ucloud,claude-4-sonnet",
    "think": "ucloud,claude-4-sonnet",
    "longContext": "ucloud,claude-4-sonnet",
    "longContextThreshold": 60000,
    "webSearch": "ucloud,claude-4-sonnet"
  }
}
```

### 3. 使用 Router 运行 Claude Code

使用 router 启动 Claude Code：

```shell
ccr code
```

> **注意**: 
> ⚠️ 如果您在`ccr ui`修改或直接修改了ccr的配置，请务必执行`ccr restart`进行重启，否则模型选择可能不生效！
> 如果您是首次安装 Claude Code 时遇到反复弹出官方登录页面的问题，您可以通过以下方式临时解决：
> 在终端中执行 ANTHROPIC_AUTH_TOKEN=token ccr code 命令，其中 token 参数可使用任意值填充，此操作旨在绕过官方账号登录验证流程。
> 
> 如果您想在 VS Code 中使用 Claude Code 插件并完成ccr相关配置，请按照以下步骤操作：
> 1. 退出当前的 Claude Code, 可以按两下 Ctrl + C
> 2. 在命令行中输入：ccr code 并执行


### 4. UI 模式

为了获得更直观的体验，您可以使用 UI 模式来管理您的配置：

```shell
ccr ui
```

这将打开一个基于 Web 的界面，您可以在其中轻松查看和编辑您的 `config.json` 文件。

#### Router

`Router` 对象定义了在不同场景下使用哪个模型：

-   `default`: 用于常规任务的默认模型。
-   `background`: 用于后台任务的模型。这可以是一个较小的本地模型以节省成本。
-   `think`: 用于推理密集型任务（如计划模式）的模型。
-   `longContext`: 用于处理长上下文（例如，> 60000 token）的模型。
-   `longContextThreshold` (可选): 触发长上下文模型的令牌数阈值。如果未指定，默认为 60000。
-   `webSearch`: 用于处理网络搜索任务，需要模型本身支持。

