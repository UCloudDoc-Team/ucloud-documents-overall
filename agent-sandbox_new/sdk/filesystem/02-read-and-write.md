# 读写文件
<subtitle>在沙箱内高效执行文件的持久化存储与读取操作。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

文件系统是沙箱存储状态的核心方式。SDK 提供了一系列便捷的方法来处理文本、二进制等不同类型的数据。

## 读取文件内容

使用 `files.read()` 方法从指定路径获取文件内容。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 读取文本文件
content = sandbox.files.read('/home/user/output.txt')
print(f"File content: {content}")
```

## 写入单个文件

使用 `files.write()` 方法将数据保存到沙箱中。如果目标路径的父目录不存在，SDK 会自动为您创建。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 写入简单文本
sandbox.files.write('/home/user/script.py', 'print("Hello from Sandbox")')

# 写入二进制数据
sandbox.files.write('/home/user/data.bin', b'\x00\x01\x02\x03')
```

## 批量写入多文件

为了减少网络往返（RTT），对于多个小文件，建议使用 `write_files` 进行批量操作。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

files_to_sync = [
    {"path": "config/app.conf", "data": "port=8080"},
    {"path": "data/sample.json", "data": '{"id": 1}'}
]

sandbox.files.write_files(files_to_sync)
```

---

!> **权限说明**：如果您尝试向受保护的系统目录（如 `/etc`）写入文件，请确保您的沙箱进程具备 sudo 权限，或通过 `commands.run` 配合 `sudo tee` 等命令完成。
