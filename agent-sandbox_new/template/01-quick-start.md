# 模板快速开始
<subtitle>学习如何定义、构建并部署自定义沙箱模板，快速定制 Agent 的运行环境。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

模板（Template）是沙箱的蓝图。它允许您预装软件、配置环境变量、预置文件，以及设置启动命令与就绪检查。通过模板，您可以确保 Agent 每次启动时都处于完全就绪的环境，无需额外等待安装过程。

---

## 方式一：使用 CLI (推荐)

CLI 是管理模板最便捷的方式。

1.  **安装 CLI**
    ```bash
    npm i -g @ucloud-sdks/ucloud-sandbox-cli
    ```

2.  **初始化项目**
    执行以下命令，按照交互提示配置您的新模板。
    ```bash
    ucloud-sandbox-cli template init
    ```

3.  **构建与使用**
    初始化完成后，CLI 会生成包含 `README.md` 的项目结构。您可以根据说明进行构建和部署。

---

## 方式二：使用 Python SDK

如果您希望将模板构建流程集成到现有的 Python 工作流中，可以使用 SDK 模式。

### 1. 编写模板定义 (`template.py`)

```python
from ucloud_sandbox import Template, wait_for_timeout

template = (
    Template()
    .from_base_image()  # 使用官方预置的基础镜像
    .set_envs({
        "APP_VERSION": "1.0.0",
        "DEBUG": "true"
    })
    .set_start_cmd("echo 'Environment is ready'", wait_for_timeout(5_000))
)
```

### 2. 构建模板 (`build.py`)

```python
from ucloud_sandbox import Template, default_build_logger

if __name__ == '__main__':
    # 调用构建接口，并指定别名 (Alias)
    Template.build(
        template,
        alias="my-agent-env",
        cpu_count=2,
        memory_mb=2048,
        on_build_logs=default_build_logger(),
    )
```

### 3. 执行构建

```bash
python build.py
```

---

## 使用自定义模板

一旦模板构建成功，您就可以通过其**别名 (Alias)** 来启动沙箱。

```python
from ucloud_sandbox import Sandbox

# 使用刚才构建的模板别名创建沙箱
sbx = Sandbox.create(template="my-agent-env")

# 检查环境变量
result = sbx.commands.run("echo $APP_VERSION")
print(f"Version: {result.stdout}")  # 输出: Version: 1.0.0
```

?> **提示**：模板别名是您全局唯一的标识符。在生产环境中，建议通过别名来管理版本迭代。
