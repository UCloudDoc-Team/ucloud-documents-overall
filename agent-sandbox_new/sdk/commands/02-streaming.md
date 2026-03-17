# 流式输出
<subtitle>在命令执行过程中实时捕获并处理标准输出与错误流，提升用户交互体验。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

对于长时间运行或需要向用户展示进度的命令，您可以通过回调函数实时接收数据流，而无需等待整个命令执行结束。

## 使用回调函数 (Callback)

在调用 `commands.run()` 时，传入 `on_stdout` 和 `on_stderr` 参数。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 定义处理函数
def handle_output(data):
    print(f"[LIVE]: {data.strip()}")

# 执行命令并实时流式处理结果
result = sandbox.commands.run(
    'for i in {1..5}; do echo "Step $i"; sleep 1; done',
    on_stdout=handle_output,
    on_stderr=handle_output
)
```

## 应用场景

*   **进度展示**：在执行安装脚本或复杂计算时显示实时进度条。
*   **交互式日志**：将沙箱内的实时运行日志转发至前端 UI。
*   **异常监控**：实时扫描 `on_stderr` 中的关键错误字符并即刻触发告警。

---

?> **性能提示**：回调函数是在单独的监听线程中执行的，请避免在回调中执行大量耗时或阻塞操作，以免影响流数据的接收。
