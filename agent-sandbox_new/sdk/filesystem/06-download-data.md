# 从沙箱下载数据
<subtitle>从沙箱下载文件数据到本地或通过预签名 URL 分享。</subtitle>

您可以使用 `files.read()` 方法从沙箱下载数据。

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 从沙箱读取文件
content = sandbox.files.read('/path/in/sandbox')
# 将文件写入本地文件系统
with open('/local/path', 'w') as file:
    file.write(content)
```

## 使用预签名 URL 下载

有时，您可能希望允许未经授权环境（如浏览器）中的用户从沙箱下载文件。针对此用例，您可以使用预签名 URL 让用户安全地下载文件。

您所需要做的就是使用 `secure=True` 选项创建一个沙箱。随后将生成一个下载 URL，该 URL 带有签名，仅允许授权用户访问文件。您可以选择为 URL 设置过期时间，使其仅在有限时间内有效。

```python
from ucloud_sandbox import Sandbox

# 启动安全沙箱（默认情况下所有操作都必须经过授权）
sandbox = Sandbox.create(timeout=12_000, secure=True)

# 创建一个过期时间为10秒的预签名下载 URL
# 用户只需访问该 URL 即可下载文件，这在浏览器中也有效。
signed_url = sandbox.download_url(path="demo.txt", user="user", use_signature_expiration=10_000)
```
