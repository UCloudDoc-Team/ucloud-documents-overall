# 监视沙箱目录的更改
<subtitle>实时监听沙箱内目录的文件变更事件。</subtitle>

您可以使用 `files.watch_dir()` 方法来监视目录的更改。

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

> **提示**
>
> 由于事件是异步追踪的，投递可能会有延迟。
> 建议不要在进行更改后立即收集或关闭监视器。

```python
from ucloud_sandbox import Sandbox, FilesystemEventType

sandbox = Sandbox.create()
dirname = '/home/user'

# 监视目录更改
handle = sandbox.files.watch_dir(dirname)
# 触发文件写入事件
sandbox.files.write(f"{dirname}/my-file", "hello")

# 获取自上次 `get_new_events()` 调用以来的最新事件
events = handle.get_new_events()
for event in events:
    print(event)
    if event.type == FilesystemEventType.WRITE:
        print(f"wrote to file {event.name}")
```

## 递归监视

您可以通过 `recursive` 参数启用递归监视。

> **提示**
>
> 当快速创建新文件夹（例如，深度嵌套的文件夹路径）时，除 `CREATE` 之外的事件可能不会被触发。为避免这种情况，请提前创建所需的文件夹结构。

```python
from ucloud_sandbox import Sandbox, FilesystemEventType

sandbox = Sandbox.create()
dirname = '/home/user'

# 监视目录更改（递归）
handle = sandbox.files.watch_dir(dirname, recursive=True)
# 触发文件写入事件
sandbox.files.write(f"{dirname}/my-folder/my-file", "hello")

# 获取自上次 `get_new_events()` 调用以来的最新事件
events = handle.get_new_events()
for event in events:
    print(event)
    if event.type == FilesystemEventType.WRITE:
        print(f"wrote to file {event.name}")
```
