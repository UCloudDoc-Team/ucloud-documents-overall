# 网络与互联网访问
<subtitle>灵活配置沙箱的出站连接权限，以及通过公共 URL 访问沙箱内服务。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

默认情况下，每个沙箱都具备完整的互联网访问能力，并可以通过唯一的公共 URL 暴露服务。

---

## 互联网出站控制

您可以在创建沙箱时通过 `allow_internet_access` 参数快速锁定或开放沙箱的外网访问权限。

```python
from ucloud_sandbox import Sandbox

# 默认启用互联网访问
sandbox = Sandbox.create(allow_internet_access=True)

# 禁用所有出站网络连接，确保敏感代码执行安全
isolated_sandbox = Sandbox.create(allow_internet_access=False)
```

### 细粒度黑白名单 (CIDR)

如果需要更精确的控制，可以使用 `network` 字典配置 `allow_out` 和 `deny_out` 规则。

```python
from ucloud_sandbox import Sandbox, ALL_TRAFFIC

# 拒绝所有流量，但允许访问特定的 API 服务器
sandbox = Sandbox.create(
    network={
        "deny_out": [ALL_TRAFFIC],
        "allow_out": ["1.2.3.4/32", "8.8.8.0/24"]
    }
)
```

!> **优先级规则**：`allow_out` (白名单) 的优先级始终高于 `deny_out` (黑名单)。如果一个 IP 同时出现在两个列表中，它将被**允许**访问。

---

## 访问沙箱内服务 (Inbound)

沙箱内启动的任何网络服务（如 Web API、Dashboard）都可以通过公共 URL 在外部访问。

### 获取公共 URL

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()

# 获取沙箱在 3000 端口暴露的主机名
host = sandbox.get_host(3000)
print(f"Server URL: https://{host}")

# 示例输出：https://3000-xxxx.sandbox.ucloudai.com
```

### 保护沙箱服务 (身份验证)

默认情况下这些 URL 是公开的。如果您希望只有授权客户端才能访问，请禁用 `allow_public_traffic`。

```python
from ucloud_sandbox import Sandbox
import requests

sandbox = Sandbox.create(
    network={"allow_public_traffic": False}
)

# 此时访问该沙箱需要令牌
token = sandbox.traffic_access_token

# 发起带有身份验证头的请求
response = requests.get(
    f"https://{sandbox.get_host(8080)}",
)
print(response) # 403
```

### 自定义请求 Host 头部

如果您的沙箱内服务对 `Host` 头部有特殊要求（例如反向代理需要匹配 `localhost`），可以使用 `mask_request_host` 进行重写。

```python
# 将进入沙箱的请求 Host 头部重写为 localhost:端口号
sandbox = Sandbox.create(
    network={
        "mask_request_host": "localhost:${PORT}"
    }
)
```

?> `${PORT}` 是一个动态占位符，执行时会被自动替换为请求的实际端口号。