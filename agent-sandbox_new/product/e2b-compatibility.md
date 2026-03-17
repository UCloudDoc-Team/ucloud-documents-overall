# E2B 兼容模式
<subtitle>使用现有的 E2B SDK 无缝接入 UCloud Sandbox 服务。</subtitle>

UCloud Sandbox 完全兼容 E2B SDK，您只需简单配置环境变量即可使用现有的 E2B 代码库直接接入 UCloud Sandbox 服务。

---

## 环境配置

### 设置域名和 API Key

在使用 E2B SDK 之前，您需要配置以下环境变量：

```bash
# 设置 UCloud Sandbox 域名
export E2B_DOMAIN=sandbox.ucloudai.com

# 设置您的 Modelverse API Key
export E2B_API_KEY="<Your Modelverse API Key>"
```

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的 API Key。

---

## 支持的 SDK 包

UCloud Sandbox 兼容以下 E2B SDK 包：

| SDK 包 | 用途 | 安装命令 |
|--------|------|----------|
| `e2b_code_interpreter` | 代码解释执行 | `pip install e2b-code-interpreter` |
| `e2b` | 基础沙箱功能 | `pip install e2b` |
| `e2b_desktop` | 桌面环境沙箱 | `pip install e2b-desktop` |

---

## 快速开始

### 基础示例

```python
from e2b_code_interpreter import Sandbox
# 或者 from e2b import Sandbox
# 或者 from e2b_desktop import Sandbox

# 创建沙箱
sbx = Sandbox.create()

# 执行命令
execution = sbx.commands.run('ls -l')
print(execution)

# 销毁沙箱
sbx.kill()
```

---

## 完整示例

### 代码执行

```python
from e2b_code_interpreter import Sandbox

# 创建沙箱
sbx = Sandbox.create()

# 执行 shell 命令
result = sbx.commands.run('echo "Hello from UCloud Sandbox!"')
print(f"stdout: {result.stdout}")
print(f"exit_code: {result.exit_code}")

# 写入文件
sbx.files.write("test.py", """
print("Hello, World!")
for i in range(5):
    print(f"Count: {i}")
""")

# 执行 Python 脚本
result = sbx.commands.run('python test.py')
print(result.stdout)

# 读取文件
content = sbx.files.read("test.py")
print(f"File content: {content}")

# 销毁沙箱
sbx.kill()
```

### 超时控制

```python
from e2b_code_interpreter import Sandbox

# 创建沙箱，设置 5 分钟超时
sbx = Sandbox.create(timeout=300)

# 执行长时间任务
result = sbx.commands.run('sleep 10 && echo "Done!"')
print(result.stdout)

# 手动销毁
sbx.kill()
```

### 自定义模板

```python
from e2b_code_interpreter import Sandbox

# 使用自定义模板创建沙箱
sbx = Sandbox.create(template="my-custom-template")

# 验证环境
result = sbx.commands.run('echo $MY_ENV_VAR')
print(result.stdout)

sbx.kill()
```

---

## API 对照表

E2B SDK 的主要方法在 UCloud Sandbox 中均有对应支持：

| E2B 方法 | 说明 | 支持状态 |
|----------|------|----------|
| `Sandbox.create()` | 创建沙箱 | ✅ |
| `sbx.commands.run()` | 执行命令 | ✅ |
| `sbx.files.write()` | 写入文件 | ✅ |
| `sbx.files.read()` | 读取文件 | ✅ |
| `sbx.files.list()` | 列出目录 | ✅ |
| `sbx.kill()` | 销毁沙箱 | ✅ |
| `sbx.set_timeout()` | 设置超时 | ✅ |

---

## 迁移指南

如果您已有使用 E2B SDK 的代码，迁移到 UCloud Sandbox 非常简单：

1. **无需修改代码**：保持现有的 E2B SDK 导入和使用方式不变
2. **配置环境变量**：设置 `E2B_DOMAIN` 和 `E2B_API_KEY`
3. **运行代码**：您的代码将自动使用 UCloud Sandbox 服务

```bash
# 设置环境变量后，直接运行现有代码
export E2B_DOMAIN=sandbox.ucloudai.com
export E2B_API_KEY="your-api-key"

python your_e2b_script.py
```

---

## 注意事项

!> **API Key 区别**：E2B 兼容模式使用 `E2B_API_KEY` 环境变量，而原生 UCloud SDK 使用 `AGENTBOX_API_KEY`。请确保使用正确的环境变量。

?> **推荐**：如果您是新用户，建议直接使用 [UCloud Sandbox 原生 SDK](/00-quick-start)，以获得更好的功能支持和技术支持体验。

---

## 下一步

- [SDK 快速开始](/agent-sandbox/docs/sdk/00-quick-start) - 使用原生 UCloud Sandbox SDK
- [沙箱生命周期](/agent-sandbox/docs/sdk/sandbox/01-lifecycle) - 了解沙箱管理
- [命令执行](/agent-sandbox/docs/sdk/commands/01-overview) - 详细的命令执行指南
