# Desktop Sandbox

Desktop Sandbox 提供了一个带有图形用户界面 (GUI) 的 Linux 桌面环境。你可以通过 SDK 控制鼠标、键盘，甚至通过 VNC 流式传输桌面画面。这对于需要进行 GUI 自动化、浏览器操作或视觉任务的 Agent 非常有用。

## 引入

Desktop Sandbox 位于 `ucloud_sandbox.desktop` 模块中。

```python
from ucloud_sandbox.desktop import Sandbox
```

## 快速开始

```python
from ucloud_sandbox.desktop import Sandbox

# 创建一个 Desktop Sandbox 实例
# 默认分辨率为 1024x768
desktop = Sandbox.create()

# 截取屏幕截图
screenshot_bytes = desktop.screenshot()
with open("screenshot.png", "wb") as f:
    f.write(screenshot_bytes)

# 控制鼠标
desktop.left_click(100, 200)  # 在 (100, 200) 处左键点击
desktop.write("Hello Desktop!") # 输入文本

# 启动 VNC 流 (用于实时查看)
desktop.stream.start()
print(f"VNC URL: {desktop.stream.get_url()}")

desktop.kill()
```

## 主要功能

- **鼠标控制**: `move_mouse`, `left_click`, `right_click`, `double_click`, `drag`, `scroll`.
- **键盘控制**: `press`, `write`.
- **屏幕截图**: `screenshot` 支持返回字节或流。
- **VNC 流**: 内置 `stream` 对象 (`_VNCServer`) 可以启动 noVNC 代理方便在浏览器中查看。
- **窗口管理**: 获取当前窗口 ID、标题等（依赖 `xdotool`）。

## 注意事项

- Desktop Sandbox 启动可能比标准 Sandbox 稍慢，因为它需要启动 X Server 和桌面环境 (XFCE4)。
