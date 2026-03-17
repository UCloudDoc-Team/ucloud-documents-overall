# Claude Code 接入指南

> 现在你可以通过 [UModelverse 平台](https://console.ucloud.cn/modelverse/model-center) 使用 Claude 系列模型。

## 系统要求

| 平台    | 要求                                |
| ------- | ----------------------------------- |
| Windows | Windows 10 或 Windows 11            |
| macOS   | macOS 10.15 (Catalina) 或更高版本   |
| Linux   | Ubuntu 18.04+, CentOS 7+, Debian 9+ |

所有平台均需要：
- Node.js 18+
- 网络连接

## 1. 安装 Node.js

请确保您已安装 Node.js 18+，请参考 [Node.js 官方网站](https://nodejs.org/zh-cn/download)。

验证安装：
```bash
node --version
npm --version
```

> **提示：** 建议使用 LTS（长期支持）版本以获得最佳稳定性。

## 2. 安装 Claude Code CLI

打开终端/命令提示符，执行以下命令：

```bash
npm install -g @anthropic-ai/claude-code
```

验证安装：
```bash
claude --version
```

> **注意：** Windows 用户如遇到权限问题，请确保以管理员身份运行命令提示符。

## 3. 配置 UModelverse API

### 3.1 获取 API Key

访问 [UModelverse 控制台](https://console.ucloud.cn/modelverse/api) 获取您的 API 密钥。

### 3.2 配置环境变量

> **重要提示：** 请将下方的 `ANTHROPIC_AUTH_TOKEN` 替换为您在 UModelverse 平台获取的实际 API Key！

> **⚠️ 注意：** 由于部分实验性功能存在 API 兼容性问题，建议通过 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 参数禁用这些功能以确保稳定运行。

<!-- tabs:start -->
#### **Windows**

配置位置：`%USERPROFILE%\.claude\settings.json`

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-umodelverse-api-key",
    "ANTHROPIC_BASE_URL": "https://api.modelverse.cn",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
  }
}
```

#### **macOS**

配置位置：`~/.claude/settings.json`

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-umodelverse-api-key",
    "ANTHROPIC_BASE_URL": "https://api.modelverse.cn",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
  }
}
```

#### **Linux**

配置位置：`~/.claude/settings.json`

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-umodelverse-api-key",
    "ANTHROPIC_BASE_URL": "https://api.modelverse.cn",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
  }
}
```
<!-- tabs:end -->

**配置参数说明：**

| 参数                                     | 说明                                          |
| ---------------------------------------- | --------------------------------------------- |
| `ANTHROPIC_MODEL`                        | 指定默认使用的模型                            |
| `ANTHROPIC_DEFAULT_*_MODEL`              | 将 Haiku、Sonnet 等模型统一指向平台支持的模型 |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | 禁用实验性功能，避免 API 兼容性问题           |

> **注意：** 配置文件更加安全且便于管理，需要重启 Claude Code 才生效。

## 4. 启动 Claude Code

配置完成后，先进入到工程目录：

```bash
cd your-project-folder
```

然后，运行以下命令启动：

```bash
claude
```

首次启动后需要先进行主题的选择等操作：

1. 选择喜欢的主题（回车）
2. 确认安全须知（回车）
3. 使用默认 Terminal 配置（回车）
4. 信任工作目录（回车）
5. 开始编程！🚀
