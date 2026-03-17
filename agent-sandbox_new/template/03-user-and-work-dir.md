# 用户与工作目录
<subtitle>了解沙箱环境中的默认权限体系及执行路径，确保您的脚本运行无误。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

## 默认规则

与标准的 Docker 容器不同，UCloud Sandbox 为了安全性及操作便利性，默认采用非 root 用户：

*   **默认用户**: `user` (具备 sudo 权限)
*   **默认工作目录**: `/home/user` (用户主目录)

这种设计可以帮助您更顺利地安装需要用户环境支持的工具（如 npm, pip 等），同时降低了误删系统关键文件的风险。

## 在模板中切换身份

模板构建过程中设置的最后一个用户和目录，将作为所有基于该模板生成的沙箱的**默认执行环境**。

```python
from ucloud_sandbox import Template, Sandbox

template = (
    Template()
    .from_base_image()
    .run_cmd("whoami")  # 输出: user
    .run_cmd("pwd")     # 输出: /home/user
    
    # 切换到 guest 用户
    .set_user("guest")
    .run_cmd("whoami")  # 输出: guest
    .run_cmd("pwd")     # 输出: /home/guest
)

# 生成沙箱后，其默认身份即为 guest
sbx = Sandbox.create(template="your-template-id")
sbx.commands.run("whoami")  # 输出: guest
```

## 注意事项

?> **sudo 权限**：默认用户 `user` 允许在无需输入密码的情况下调用 `sudo` 以执行系统级任务。

!> **路径隔离**：系统敏感目录（如 `/root` 或 `/etc/shadow`）默认是对 `user` 账户受限的，操作时请加上 `sudo`。
