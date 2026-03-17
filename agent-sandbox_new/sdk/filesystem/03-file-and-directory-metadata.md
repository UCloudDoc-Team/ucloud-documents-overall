# 获取文件或目录信息
<subtitle>获取文件或目录的详细属性信息，包括权限、大小和修改时间。</subtitle>

您可以使用 `files.get_info()` 方法获取有关文件或目录的信息。返回的信息包括文件名、类型和路径等。

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

### 获取文件信息

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 创建新文件
sandbox.files.write('test_file.txt', 'Hello, world!')

# 获取文件相关信息
info = sandbox.files.get_info('test_file.txt')

print(info)
# EntryInfo(
#   name='test_file.txt',
#   type=<FileType.FILE: 'file'>,
#   path='/home/user/test_file.txt',
#   size=13,
#   mode=0o644,
#   permissions='-rw-r--r--',
#   owner='user',
#   group='user',
#   modified_time='2025-05-26T12:00:00.000Z',
#   symlink_target=None
# )
```

### 获取目录信息

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 创建新目录
sandbox.files.make_dir('test_dir')

# 获取目录相关信息
info = sandbox.files.get_info('test_dir')

print(info)
# EntryInfo(
#   name='test_dir',
#   type=<FileType.DIR: 'dir'>,
#   path='/home/user/test_dir',
#   size=0,
#   mode=0o755,
#   permissions='drwxr-xr-x',
#   owner='user',
#   group='user',
#   modified_time='2025-05-26T12:00:00.000Z',
#   symlink_target=None
# )
```
