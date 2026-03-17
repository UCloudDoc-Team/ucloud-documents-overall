# 典型示例库
<subtitle>涵盖从基础 Web 应用、多 runtime 环境到图形化桌面的沙箱构建方案。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

通过以下示例，您可以快速了解如何为各种复杂的 Agent 任务定制专属环境。

---

## Next.js 全栈应用 (Node.js)

此示例演示如何构建一个预装了 Next.js、Tailwind CSS 和 shadcn UI 的环境。

?> **沙箱预加载**：模板构建完成后，沙箱启动即会自动运行 `npm run dev`，开发服务器在端口 3000 就绪。

```python
# template.py
from ucloud_sandbox import Template, wait_for_url

template = (
    Template()
    .from_node_image("21-slim")
    .set_workdir("/home/user/nextjs-app")
    .run_cmd('npx create-next-app@14.2.30 . --ts --tailwind --no-eslint --import-alias "@/*" --use-npm --no-app --no-src-dir')
    .run_cmd("npx shadcn@2.1.7 init -d")
    .run_cmd("npx shadcn@2.1.7 add --all")
    # 整理目录结构并设置启动命令
    .run_cmd("mv /home/user/nextjs-app/* /home/user/ && rm -rf /home/user/nextjs-app")
    .set_workdir("/home/user")
    .set_start_cmd("npx next --turbo", wait_for_url('http://localhost:3000'))
)
```

---

## 高性能 Web 环境 (Bun)

使用 Bun 运行时可以显著提升依赖安装和热重载速度。

```python
# template.py
from ucloud_sandbox import Template, wait_for_url

template = (
    Template()
    .from_bun_image("1.3")
    .set_workdir("/home/user/nextjs-app")
    .run_cmd("bun create next-app --app --ts --tailwind --turbopack --yes --use-bun .")
    .run_cmd("bunx --bun shadcn@latest init -d")
    .set_workdir("/home/user")
    .set_start_cmd("bun --bun run dev", wait_for_url('http://localhost:3000'))
)
```

---

## 图形化桌面环境 (GUI & VNC)

UCloud Sandbox 支持运行 X11 桌面环境，并通过 NoVNC 提供浏览器端的实时交互界面。

```python
# template.py
from ucloud_sandbox import Template, wait_for_port

template = (
    Template()
    .from_image("ubuntu:22.04")
    # 安装图形化环境所需的所有系统依赖
    .run_cmd([
        "apt-get update",
        "apt-get install -y xfce4 xfce4-goodies xvfb x11vnc xdotool novnc websockify",
        "apt-get clean"
    ])
    # 拷贝并设置 VNC 启动脚本
    .copy("start_command.sh", "/start_command.sh")
    .run_cmd("chmod +x /start_command.sh")
    # 启动时开启桌面服务，等待 6080 端口就绪
    .set_start_cmd("/start_command.sh", wait_for_port(6080))
)
```

!> **资源建议**：运行桌面环境建议配置较高的资源限额（如 8 核 CPU，8GB 内存），以保证流畅的操控体验。

---

## 如何构建上述示例？

构建逻辑基本一致，只需调用 `Template.build` 接口：

```python
from ucloud_sandbox import Template, default_build_logger
from template import template

if __name__ == '__main__':
    Template.build(
        template,
        alias="my-example-env",
        cpu_count=4,
        memory_mb=4096,
        on_build_logs=default_build_logger(),
    )
```
