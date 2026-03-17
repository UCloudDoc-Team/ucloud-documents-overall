# Claude Code

<subtitle>在沙箱中快速启动并使用 Claude Code 智能助手。</subtitle>

`claude-code` 模板预置了 Anthropic 的 Claude Code 环境，基于UModelverse 模型服务平台，您可以通过 CLI 快速启动并直接进行交互。

## 快速开始

使用 CLI 命令 `ucloud-sandbox-cli sbx cr claude-code` 即可通过终端连接：

```bash
ucloud-sandbox-cli sbx cr claude-code
```

## 交互流程

连接成功后，您将看到如下启动画面。首次使用需要输入 API Token 进行认证。

```text
~ $ claude

╔════════════════════════════════════════════╗
║     🚀 Claude Code Launcher              ║
╚════════════════════════════════════════════╝

ℹ Please enter your Anthropic API token
(The token will be stored in ~/.claude/settings.json)

Enter API Token: 
```

**配置步骤：**

1.  当提示 `Enter API Token:` 时，请输入您的 ModelVerse API Key。
    *   [获取 ModelVerse API Key](/https://console.ucloud.cn/modelverse/experience/api-keys)
2.  输入完成后回车，即可进入 Claude Code 的交互界面开始编程。

## 模板特性

*   **预装环境**: 内置 Node.js 与 `claude-code` CLI 工具。
*   **持久化设置**: 支持在沙箱生命周期内保存配置。
*   **安全隔离**: 所有代码执行均在沙箱隔离环境中运行，保障宿主机安全。
