# 列表查询
<subtitle>检索并筛选当前处于运行或暂停状态的沙箱实例。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

通过 `Sandbox.list()` 方法，您可以轻松获取名下所有活跃沙箱的清单，并支持按状态、元数据进行精细化过滤与分页处理。

## 基础查询

`Sandbox.list()` 返回一个分页器对象。

```python
from ucloud_sandbox import Sandbox

# 获取分页器
paginator = Sandbox.list()

# 获取第一页数据（默认包含运行中和已暂停的沙箱）
first_page = paginator.next_items()

for sbx in first_page:
    print(f"ID: {sbx.sandbox_id} | Template: {sbx.template_id} | Status: {sbx.state}")
```

## 按条件过滤

### 按任务状态过滤
您可以仅查询 `RUNNING` (运行中) 或 `PAUSED` (已暂停) 的沙箱。

```python
from ucloud_sandbox import Sandbox, SandboxQuery, SandboxState

# 仅查询处于暂停状态的沙箱
paginator = Sandbox.list(
    query=SandboxQuery(
        state=[SandboxState.PAUSED],
    ),
)
sandboxes = paginator.next_items()
```

### 按自定义元数据过滤
如果您在创建沙箱时附加了 `metadata`，则可以通过这些标签找回特定的沙箱。

```python
from ucloud_sandbox import Sandbox, SandboxQuery

# 查找所属 user_id 为 "123" 且环境为 "dev" 的沙箱
paginator = Sandbox.list(
    query=SandboxQuery(
        metadata={
            "user_id": "123",
            "env": "dev"
        }
    ),
)
sandboxes = paginator.next_items()
```

## 分页处理

!> **限制说明**：单次查询的最大限制（limit）为 **100**。

### 手动分页
利用 `next_token` 进行翻页操作。

```python
paginator = Sandbox.list(limit=50)

# 检查是否有更多数据
if paginator.has_next:
    print(f"Next Token: {paginator.next_token}")
    # 获取下一页
    next_items = paginator.next_items()
```

### 自动获取全部数据
通过循环处理，一次性加载所有活跃沙箱。

```python
paginator = Sandbox.list()
all_sandboxes = []

while paginator.has_next:
    items = paginator.next_items()
    all_sandboxes.extend(items)

print(f"Total active sandboxes: {len(all_sandboxes)}")
```

## 下一步操作

获取到沙箱 ID 后，您可以：
- 调用 `Sandbox.connect(id)` [重新连接沙箱](/agent-sandbox/docs/sdk/sandbox/09-connect-to-running-sanbox)。
- 调用 `Sandbox.kill(id)` 强制关停。
- 检索其运行指标。