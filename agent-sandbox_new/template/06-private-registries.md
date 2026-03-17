# 私有仓库

<subtitle>从私有仓库拉取基础镜像以构建您的自定义模板。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

如果您的基础镜像托管在私有仓库中，您可以使用以下辅助函数提供凭据：

*   通用仓库
*   UHub 仓库

## 通用仓库

```python
from ucloud_sandbox import Template

Template().from_image(
    image="ubuntu:22.04",
    username="user",
    password="pass",
)
```

## UHub 仓库

UHub 是 UCloud 提供的容器镜像仓库服务。

| 参数 | 说明 |
|------|------|
| `image` | UHub 镜像地址，如 `uhub.service.ucloud.cn/xxx/myimage:latest` |
| `username` | UHub 用户名，如 `user@ucloud.cn` |
| `password` | UHub 独立密码 |

```python
from ucloud_sandbox import Template

Template().from_uhub_registry(
    image="uhub.service.ucloud.cn/your-org/your-image:tag",
    username="user@ucloud.cn",
    password="your-uhub-password",
)
```

