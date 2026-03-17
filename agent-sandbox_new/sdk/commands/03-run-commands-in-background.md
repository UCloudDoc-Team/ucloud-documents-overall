# 后台运行命令
<subtitle>在沙箱内异步执行长任务，并实时获取其运行状态与输出流。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

对于耗时较长、无需阻塞主线程的任务，您可以通过设置 `background=True` 将命令置于后台运行。

## 启动异步任务

调用 `run` 方法并指定 `background` 参数，它将立即返回一个 `Command` 进程句柄。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 在后台启动一个长耗时命令
process = sandbox.commands.run('sleep 5; echo "Task Complete"', background=True)

# 主线程可以继续执行其他逻辑
print(f"Command started with PID: {process.pid}")
```

## 交互与监控

### 迭代实时输出
您可以像迭代生成器一样获取后台命令的实时输出。

```python
for stdout, stderr, _ in process:
    if stdout:
        print(f"[STDOUT]: {stdout}")
    if stderr:
        print(f"[STDERR]: {stderr}")
```

### 强制关停后台任务
如果任务超时或逻辑不再需要，请及时释放资源。

```python
# 立即终止后台运行的命令
process.kill()
```

---

?> **等待完成**：如果您在程序末尾需要确保某个后台任务执行完毕，可以调用 `process.wait()`。
