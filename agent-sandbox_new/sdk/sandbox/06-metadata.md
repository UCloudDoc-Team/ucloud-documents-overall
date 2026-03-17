# 元数据管理
<subtitle>为沙箱附加自定义标签，便于进行多维度筛选与会话关联。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

元数据允许您为沙箱关联自定义的键值对（Key-Value Pairs）。这在管理大规模并发沙箱时非常有价值。

## 典型应用场景

*   **会话关联**：将沙箱与特定终端用户的 Session ID 绑定。
*   **权限透传**：为沙箱存储自定义的用户标识（如 `userId`），方便回溯查询。
*   **业务分类**：标注沙箱所属的项目或任务类型。

## 设置与访问元数据

您需要在创建沙箱时指定 `metadata` 参数。之后可以通过沙箱信息的 `metadata` 字段进行访问。

```python
from ucloud_sandbox import Sandbox

# 1. 创建带有元数据的沙箱
sandbox = Sandbox.create(
    metadata={
        'userId': 'user_1a2b3c',
        'taskType': 'data-analysis'
    },
)

# 2. 访问当前沙箱的元数据
print(sandbox.get_info())


# 3. 通过列表接口访问元数据
running_sandboxes = Sandbox.list().next_items()
for sbx in running_sandboxes:
    if sbx.metadata.get('taskType') == 'data-analysis':
        print(f"Found analysis sandbox: {sbx.sandbox_id}")
```

## 按元数据过滤

配合 `Sandbox.list()` 方法，您可以高效地按标签找回所需的沙箱实例。详情请参考 [列表查询](/agent-sandbox/docs/sdk/sandbox/08-list)。