# 缓存机制
<subtitle>掌握分层缓存原理，优化模板构建效率，显著缩短环境部署时间。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

UCloud Sandbox 的模板构建借鉴了类似 Docker 的**分层缓存**机制。每一个指令（如 `.copy()`、`.run_cmd()`）都会生成或变更一个缓存层。如果指令及其输入参数未发生变化，系统将直接复用之前的构建结果。

## 缓存的分级失效

您可以灵活控制缓存的粒度，确保环境更新能够准确生效。

### 1. 部分失效 (Skip Cache)
如果您希望从某一条指令开始往后的所有层都重新构建，请使用 `.skip_cache()`。

```python
from ucloud_sandbox import Template

template = (
    Template()
    .from_base_image()
    # 之前层仍然复用缓存
    .skip_cache() 
    # 从此行往后，所有指令都将重新执行
    .run_cmd("apt-get update && apt-get install -y some-package")
)
```

### 2. 全局失效
在执行 `Template.build` 时，可以通过参数强制跳过所有层缓存。

```python
Template.build(
    template,
    alias="my-template",
    skip_cache=True,  # 强制完整构建
)
```

---

## 独特的文件级缓存

UCloud Sandbox 对文件传输进行了深度优化。不同于 Docker 的点对点缓存依赖，即使在 `.copy()` 之前的层发生了变化，只要文件内容本身未变，系统就会自动从云端缓存中读取，无需从您的本地机器重新上传。

!> **强制上传**：如果您确定文件内容未变但仍需重新覆盖（例如某些带有副作用的初始化操作），请在 `copy()` 中设置 `force_upload=True`。

---

## 构建性能优化建议

1.  **分层颗粒度**：将安装大型依赖包（耗时长、变动少）的命令放在定义的最前端。
2.  **代码后置**：将频繁改动的源代码 `copy` 操作放在定义的末尾。
3.  **多配置共用**：在为同一套环境构建不同规格（如不同 CPU/内存）的模板时，只需修改 `alias` 后重复构建，公共的软件安装层将自动复用。

?> **缓存范围**：缓存是基于**团队（Team）**共享的。同一个团队内的不同成员在构建相似模板时，可以互惠共享已有的缓存层。
