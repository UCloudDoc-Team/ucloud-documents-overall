# 指标监控
<subtitle>实时掌握沙箱的资源使用情况，包括 CPU、内存及磁盘占用。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

UCloud Sandbox 会实时采集沙箱的资源消耗数据。通过监控指标，您可以更好地优化 Agent 的任务分配或排查性能瓶颈。

## 指标概览

系统每 **5 秒** 采集一次数据点。获取的指标包含以下维度：
- **CPU**：核心数量及当前占用百分比。
- **内存**：总容量及当前已用空间（单位：字节）。
- **磁盘**：总容量及当前已用空间（单位：字节）。

## 获取监控指标

### 使用 SDK 获取

调用 `get_metrics()` 方法获取沙箱指标数据。

```python
from time import sleep
from ucloud_sandbox import Sandbox

# 1. 创建沙箱
sbx = Sandbox.create()

# 2. 等待一段时间以供系统收集初始数据
sleep(10)

# 3. 获取指标列表
metrics = sbx.get_metrics()

# 您也可以直接通过沙箱 ID 静态调用：
# metrics = Sandbox.get_metrics(sbx.sandbox_id)

for m in metrics:
    print(f"Time: {m.timestamp} | CPU: {m.cpu_used_pct}% | RAM: {m.mem_used / 1024**2:.1f} MB")
```

### 使用 CLI 查看

您也可以在终端直接通过 CLI 进行实时查看：

```bash
ucloud-sandbox-cli sandbox metrics <sandbox-id>
```

输出示例：
```text
[2025-07-25 14:05:55Z]  CPU:  8.27% /  2 Cores | Memory:    31 / 484 MiB | Disk:  1445 / 2453 MiB
[2025-07-25 14:06:00Z]  CPU:   0.5% /  2 Cores | Memory:    32 / 484 MiB | Disk:  1445 / 2453 MiB
```

## 注意事项

?> **延迟采集**：沙箱刚创建时，系统需要 1-5 秒的时间初始化监控组件。在此之前，`get_metrics()` 可能会返回空数组。

!> **数据精度**：监控指标主要用于反映运行趋势，而非精确计费。