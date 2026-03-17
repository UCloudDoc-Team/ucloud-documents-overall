# 环境变量
<subtitle>配置沙箱运行时的上下文变量，支持内置系统变量与自定义注入。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

环境变量是控制 Agent 运行逻辑的重要手段。UCloud Sandbox 提供了一系列内置变量，同时也允许用户在不同阶段注入自定义变量。

## 内置系统变量

当沙箱启动后，系统会自动注入以下变量，供程序识别当前的运行环境：

*   `UCLOUD_SANDBOX`: 始终为 `true`，用于代码自检当前是否运行于沙箱内。
*   `UCLOUD_SANDBOX_ID`: 当前沙箱的唯一标识符。
*   `UCLOUD_TEAM_ID`: 所属团队 ID。
*   `UCLOUD_TEMPLATE_ID`: 启动该沙箱所使用的模板 ID。

**通过 SDK 验证：**

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create()
result = sandbox.commands.run("echo $UCLOUD_SANDBOX_ID")
print(f"Current Sandbox ID: {result.stdout}")
```

?> **CLI 访问路径**：如果您通过 CLI 手动进入沙箱，可以通过检查 `/run/ucloud/` 目录下的点文件来读取这些变量。

---

## 注入自定义变量

注入环境变量通常有三种粒度，按需选择：

### 1. 全局环境变量 (生命周期内有效)

在创建沙箱时指定，对该沙箱内后续执行的所有进程均可见。

```python
from ucloud_sandbox import Sandbox

sandbox = Sandbox.create(
    envs={
        'BASE_URL': 'https://api.example.com',
        'APP_MODE': 'production'
    },
)

res = sandbox.commands.run("echo $BASE_URL")
print(res.stdout)

res = sandbox.commands.run("echo $APP_MODE")
print(res.stdout)
```

### 2. 执行代码时临时注入

仅在某一次 `run_code` 调用中生效。

```python
# 仅对本次 Python 代码执行生效
from ucloud_sandbox.code_interpreter import Sandbox

sandbox = Sandbox.create()

res = sandbox.run_code(
    'import os; print(os.environ.get("TEMP_KEY"))',
    envs={'TEMP_KEY': 'temporary_value'}
)
print(res.logs.stdout)
```

### 3. 执行命令时临时注入

仅在某一次 `commands.run` 调用中生效。

```python
# 仅对本次 Shell 命令执行生效
from ucloud_sandbox.code_interpreter import Sandbox

sandbox = Sandbox.create()

res = sandbox.commands.run(
    'echo $DEBUG_LEVEL',
    envs={'DEBUG_LEVEL': 'verbose'}
)
print(res)
```

## 覆盖优先规则

!> **覆盖说明**：如果某个变量名同时存在于全局设置和单次执行设置中，**单次执行设置将具有更高的优先级**并覆盖全局设置。