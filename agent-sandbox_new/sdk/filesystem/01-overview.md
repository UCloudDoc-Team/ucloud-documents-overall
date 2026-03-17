# 文件系统
<subtitle>在隔离的沙箱环境中管理文件与目录，支持各种读写及同步操作。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

每个沙箱都拥有独立的、隔离的文件系统，专为 Agent 的临时计算任务设计。通过文件系统 API，您可以高效地管理输入数据、输出结果以及任务中间文件。

## 核心功能

通过 SDK，您可以实现以下操作：

*   **[读写文件](/agent-sandbox/docs/sdk/filesystem/02-read-and-write)**：直接写入文本或字节数据，读取文件内容。
*   **[元数据查看](/agent-sandbox/docs/sdk/filesystem/03-file-and-directory-metadata)**：检索文件大小、权限及修改时间。
*   **[目录监控](/agent-sandbox/docs/sdk/filesystem/04-watch-directory-for-changes)**：实时监听目录下产生的任何文件变更（类似 `inotify`）。
*   **[数据上传](/agent-sandbox/docs/sdk/filesystem/05-upload-data)**：将本地文件或二进制流批量传输至沙箱。
*   **[数据下载](/agent-sandbox/docs/sdk/filesystem/06-download-data)**：从沙箱中回传生成的结果文件。

## 快速入口

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 快速写入并验证
sandbox.files.write("hello.txt", "UCloud Sandbox is awesome!")
content = sandbox.files.read("hello.txt")
print(content) # 输出: UCloud Sandbox is awesome!
```

---

?> **默认根目录**：绝大部分操作默认在 `/home/user` 下进行。对于自定义模板，请确保您的 Agent 对目标路径拥有足够的读写权限。
