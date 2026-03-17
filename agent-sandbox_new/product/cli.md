# UCloud Sandbox CLI
<subtitle>强大的命令行工具，用于本地管理沙箱生命周期、构建模板及执行运维任务。</subtitle>

UCloud Sandbox CLI 是开发者最常用的工具之一。它不仅可以帮助您快速初始化和构建沙箱模板，还可以实时查看沙箱日志、监控指标以及执行批量操作。

## 安装指南

### 使用 NPM 安装
确保您的系统中已安装 Node.js 环境。

```bash
npm i -g @ucloud-sdks/ucloud-sandbox-cli
```

安装完成后，可以通过 `ucloud-sandbox-cli --help` 验证是否成功。

---

## 身份认证与配置

### 环境注入
CLI 会优先读取环境变量中的 API Key。

```bash
export AGENTBOX_API_KEY=your_api_key
```

### 登录操作
您也可以通过交互式命令完成登录。

```bash
# 执行登录，CLI 会引导您打开浏览器获取 Key
ucloud-sandbox-cli auth login

# 查看当前登录身份
ucloud-sandbox-cli auth info

# 退出当前账号
ucloud-sandbox-cli auth logout
```

---

## 沙箱运行管理

### 创建与连接
快速创建沙箱并进入交互式终端。

```bash
# 使用内置模板创建沙箱
ucloud-sandbox-cli sandbox create [template]
# 简写：ucloud-sandbox-cli sbx cr [template]
```

**内置模板**：

```bash
# 代码解释器 - 预装 Python 和数据科学库
ucloud-sandbox-cli sandbox create code-interpreter-v1

# 桌面环境 - 支持图形化应用和浏览器
ucloud-sandbox-cli sandbox create desktop

# 基础环境 - 轻量级 Linux 环境
ucloud-sandbox-cli sandbox create base
```

> 创建成功后,CLI 会自动连接终端,您可以像操作本地 Shell 一样执行命令。按 `Ctrl+D` 或输入 `exit` 退出连接(沙箱继续运行)。

### 连接现有沙箱
重新连接到已运行的沙箱实例。

```bash
ucloud-sandbox-cli sandbox connect <sandbox-id>
# 简写：ucloud-sandbox-cli sbx cn <sandbox-id>
```

### 列表查询
查看名下所有活跃（运行或暂停）的沙箱实例。

```bash
ucloud-sandbox-cli sandbox list
# 简写：ucloud-sandbox-cli sandbox ls
```

*   **状态过滤**：`--state running,paused`
*   **元数据过滤**：`--metadata key=value`
*   **输出格式**：支持 `pretty` (默认) 和 `json`。

### 强制关停 (Kill)
立即释放沙箱资源。

```bash
# 关停特定 ID
ucloud-sandbox-cli sandbox kill <id1> <id2>

# 关停所有活跃沙箱
ucloud-sandbox-cli sandbox kill --all
```

### 监控与日志
实时洞察沙箱运行状态。

```bash
# 查看实时日志
ucloud-sandbox-cli sandbox logs <id>

# 查看资源占用指标 (CPU/RAM/Disk)
ucloud-sandbox-cli sandbox metrics <id>
```

---

## 模板构建管理

### 初始化模板项目
创建一个标准化的模板开发目录。

```bash
ucloud-sandbox-cli template init --name my-custom-env --language python-sync
```

### 构建与发布
在模板目录下执行构建，将其推送至 UCloud Sandbox 平台。

```bash
# 发布模板版本
ucloud-sandbox-cli template publish <template-id>
```

---

## 典型工作流示例

1.  **准备环境**：`ucloud-sandbox-cli auth login`
2.  **创建模板**：`ucloud-sandbox-cli template init` -> 编写 `Dockerfile`
4.  **业务接入**：在 SDK 中使用 `Sandbox.create(template='my-agent-env')`
5.  **资源回收**：`ucloud-sandbox-cli sandbox kill --all`