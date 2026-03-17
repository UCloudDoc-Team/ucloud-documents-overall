# 沙箱持久化
<subtitle>支持沙箱状态的暂停与恢复，保留内存运行数据与文件系统状态。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

> 沙箱持久化目前处于公测阶段。

沙箱持久化允许您暂停（Pause）正在运行的沙箱，并在需要时恢复（Resume）到完全相同的状态。

与简单的磁盘快照不同，UCloud Sandbox 的持久化包含**内存状态**。这意味着所有正在运行的进程、加载的变量、打开的文件句柄等都会被原封不动地保留。

## 状态流转

了解沙箱在不同生命周期阶段的状态变化，有助于更精确地管理资源。

*   **Running (运行中)**：沙箱正常运行，可执行代码。这是创建后的默认状态。
*   **Paused (已暂停)**：沙箱执行被挂起，物理资源释放，但内存和磁盘状态被加密保存。
*   **Killed (已销毁)**：沙箱被彻底删除，所有相关资源和数据被清理。此状态不可逆。

### 状态操作示例

```python
from ucloud_sandbox import Sandbox

# 1. 以 Running 状态启动
sandbox = Sandbox.create()

# 2. 暂停沙箱 (Running → Paused)
sandbox.beta_pause()

# 3. 恢复沙箱 (Paused → Running)
# 使用 connect 方法连接到特定 ID 的沙箱会自动触发恢复
same_sbx = Sandbox.connect(sandbox.sandbox_id)

# 4. 彻底销毁 (Running/Paused → Killed)
same_sbx.kill()
```

## 暂停与恢复详解

### 暂停沙箱 (Pause)
当您调用 `beta_pause()` 时，沙箱会即刻冻结所有进程并将状态持久化。

```python
from ucloud_sandbox import Sandbox

sbx = Sandbox.create()
print(f"Sandbox {sbx.sandbox_id} is running.")

# 执行一些操作，例如定义变量或运行服务
# ...

# 暂停并保存状态
sbx.beta_pause()
print("Sandbox state saved and paused.")
```

### 恢复沙箱 (Resume/Connect)
通过 `Sandbox.connect(id)` 恢复沙箱。恢复后的环境与暂停瞬间完全一致。

```python
from ucloud_sandbox import Sandbox

# 连接并恢复已暂停的沙箱
# 如果沙箱正在运行，则直接建立连接
sbx = Sandbox.connect("your-sandbox-id")
print("Connected and resumed.")
```

## 管理已暂停的沙箱

### 列表查询
您可以筛选出当前处于暂停状态的所有沙箱，防止资源僵死。

```python
from ucloud_sandbox import Sandbox, SandboxQuery, SandboxState

# 查询所有已暂停的沙箱
paginator = Sandbox.list(query=SandboxQuery(state=[SandboxState.PAUSED]))
sandboxes = paginator.next_items()

for sbx in sandboxes:
    print(f"Paused Sandbox ID: {sbx.sandbox_id}")
```

### 手动清理
如果您不再需要某个暂停的沙箱，请务必将其销毁。

```python
# 通过实例销毁
sbx.kill()

# 或直接通过 ID 销毁
Sandbox.kill("your-sandbox-id")
```

## 自动暂停 (Beta)

!> **注意**：自动暂停功能目前仅可通过 `Sandbox.beta_create()` 启用。

您可以配置沙箱在非活跃状态下（超时后）不直接销毁，而是自动转入暂停状态，以平衡响应速度与成本。

```python
from ucloud_sandbox import Sandbox

# 创建启用自动暂停的沙箱
sandbox = Sandbox.beta_create(
    auto_pause=True,       # 超时后自动进入暂停状态
    timeout=10 * 60        # 设置 10 分钟非活跃超时
)
```

## Beta 阶段限制与注意事项

*   **耗时**：暂停操作大约每 GB 内存需要 4 秒；恢复操作通常在 1 秒内完成。
*   **网络**：沙箱暂停期间，其暴露的公共 URL 将不可访问，已连接的客户端会断开。恢复后需重新建立连接。
*   **有效期**：暂停状态最长保留 **30 天**。超过此期限，系统将自动清理数据，尝试恢复会抛出 `NotFoundException`。