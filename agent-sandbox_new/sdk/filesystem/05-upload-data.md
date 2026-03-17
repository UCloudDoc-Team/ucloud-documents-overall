# 上传数据到沙箱
<subtitle>将本地文件或数据流上传到沙箱文件系统。</subtitle>

您可以使用 `files.write()` 方法将数据上传到沙箱。

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

## 上传单个文件

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 读取本地文件系统的文件
with open("path/to/local/file", "rb") as file:
    # 上传文件到沙箱
    sandbox.files.write("/path/in/sandbox", file)
```

## 使用预签名 URL 上传

有时，您可能希望允许未经授权环境（如浏览器）中的用户将文件上传到沙箱。针对此用例，您可以使用预签名 URL 让用户安全地上传文件。

您所需要做的就是使用 `secure=True` 选项创建一个沙箱。随后将生成一个上传 URL，该 URL 带有签名，仅允许授权用户上传文件。您可以选择为 URL 设置过期时间，使其仅在有限时间内有效。

```python
import requests
from ucloud_sandbox import Sandbox

# 启动安全沙箱（默认情况下所有操作都必须经过授权）
sandbox = Sandbox.create(timeout=12_000, secure=True)

# 创建一个过期时间为10秒的预签名上传 URL
signed_url = sandbox.upload_url(path="demo.txt", user="user", use_signature_expiration=10_000)

form_data = {"file": "file content"}
requests.post(signed_url, data=form_data)
```

## 上传目录/多个文件

```python
import os
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

def read_directory_files(directory_path):
    files = []
    
    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # 如果是目录则跳过
        if os.path.isfile(file_path):
            # 以二进制模式读取文件内容
            with open(file_path, "rb") as file:
                files.append({
                    'path': file_path,
                    'data': file.read()
                })
    
    return files

files = read_directory_files("/local/dir")
print(files)
# [
#   {"path": "/local/dir/file1.txt", "data": "File 1 contents..."},
#   {"path": "/local/dir/file2.txt", "data": "File 2 contents..."},
#   ...
# ]

sandbox.files.write_files(files)
```
