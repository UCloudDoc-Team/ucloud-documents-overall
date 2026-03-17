# 沙箱生命周期
<subtitle>管理沙箱从创建到关闭的全过程，包括超时设置与运行监控。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

## 创建与超时设置

启动沙箱时，默认存活时间（timeout）为 5 分钟（300 秒）。您可以根据需求自定义此参数。

!> 注意：超时的沙箱将由系统自动回收并清理。

```python
from ucloud_sandbox import Sandbox

# 创建沙箱并设置存活时间为 60 秒
# 🚨 参数单位为秒
sandbox = Sandbox.create(timeout=60)
```

## 动态调整存活时间

您可以在沙箱运行时通过调用 `set_timeout` 方法实时更新存活时间。

每次调用该方法时，剩余寿命将**从当前时间点开始重新计算**。这对于需要根据用户交互动态延长会话的场景非常有用。

```python
from ucloud_sandbox import Sandbox

# 创建沙箱，初始 60 秒
sandbox = Sandbox.create(timeout=60)

# 在后续业务逻辑中重新调整为 30 秒
# 沙箱将从此刻起再运行 30 秒后自动关闭
sandbox.set_timeout(30)
```

## 获取运行详情

通过 `get_info` 方法，您可以检索沙箱的实时状态，包括 ID、所用模板、元数据以及精确的开始与结束时间。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create(timeout=60)

# 获取沙箱详细信息
info = sandbox.get_info()

print(info)

# 输出示例：
# SandboxInfo(
#   sandbox_id='ig6f1yt6idvxkxl562scj-419ff533',
#   template_id='u7nqkmpn3jjf1tvftlsu',
#   name='base',
#   metadata={},
#   started_at=datetime.datetime(2025, 3, 24, 15, 42, 59, 255612),
#   end_at=datetime.datetime(2025, 3, 24, 15, 47, 59, 255612)
# )
```

## 彻底关闭沙箱

当业务流程结束时，建议立即调用 `kill` 方法手动关闭沙箱，以释放资源。任务超时后系统也会自动执行此操作。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create(timeout=60)

# 立即销毁并回收沙箱
sandbox.kill()
```