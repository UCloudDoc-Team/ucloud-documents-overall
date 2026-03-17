# 手动连接沙箱
<subtitle>通过沙箱 ID 重新建立与正在运行或已暂停沙箱的连接。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

在有些场景下，您可能需要跨进程、跨会话重用已存在的沙箱实例。通过 `Sandbox.connect()` 方法，您可以利用沙箱 ID 重新控制目标环境。

## 连接流程

### 1. 获取目标沙箱 ID

您通常可以从数据库中读取之前保存的 ID，或者通过 `Sandbox.list()` 动态检索。

```python
from ucloud_sandbox import Sandbox

# 检索正在运行的第一个沙箱
paginator = Sandbox.list()
running_sandboxes = paginator.next_items()

if not running_sandboxes:
    print("未发现活动的沙箱。")
else:
    target_id = running_sandboxes[0].sandbox_id
    print(f"准备连接到: {target_id}")
```

### 2. 建立连接

使用 `connect` 方法。如果目标沙箱处于 `PAUSED` 状态，该操作将自动唤醒沙箱进入 `RUNNING` 状态。

```python
from ucloud_sandbox import Sandbox

# 建立连接
# 提示：connect 也会重置沙箱的非活跃超时时间
sandbox = Sandbox.connect("your-sandbox-id")

# 连接后可直接执行命令
result = sandbox.commands.run("whoami")
print(result.stdout)
```

## 注意事项

?> **超时重置**：连接沙箱会自动将该实例的非活跃超时时间重置为默认值（5 分钟）或您显式指定的 `timeout` 参数值。

!> **无效 ID**：如果目标沙箱已被销毁（Killed）或 ID 错误，该方法将抛出 `NotFoundException` 异常。建议在生产环境中使用 `try-except` 进行包裹。