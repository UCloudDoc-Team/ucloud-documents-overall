# 启动与就绪命令

<subtitle>定义模板构建时启动的后台服务及就绪检查逻辑。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

## 启动命令

启动命令（Start Command）用于在**构建模板**时启动需要常驻运行的后台服务，并将其运行状态写入快照。

典型用途包括：
- Web 服务器（如 Node.js、Python Flask）
- 数据库服务（如 SQLite、Redis）
- 后台守护进程

当您基于该模板创建沙箱时，这些服务会处于已启动且就绪的状态，用户连接后即可使用，无需等待服务初始化。

?> 工作原理请参阅：[模板工作原理](/agent-sandbox/docs/sdk/template/02-how-it-works)

## 就绪命令

就绪命令（Ready Command）用于在创建[快照](/agent-sandbox/docs/sdk/template/02-how-it-works)之前，判断**模板沙箱**是否已达到可用状态。

系统会循环执行该命令，直到其返回退出码 **0**。借此您可以精确控制：在快照生成前，需要等待[启动命令](/#启动命令)完成到什么程度（或等待哪些系统条件满足）。

## 用法

设置沙箱启动时运行的命令以及确定沙箱何时就绪的命令：

```python
from ucloud_sandbox import Template, wait_for_port, wait_for_timeout

template = Template().from_base_image()

# 同时设置启动命令和就绪命令
template.set_start_cmd("npm start", wait_for_port(3000))

# 仅设置就绪命令
template.set_ready_cmd(wait_for_timeout(10_000))
```

就绪命令用于确定沙箱何时准备好接受连接。

> 您每个模板只能调用这些命令一次。后续调用将抛出错误。

## 就绪命令辅助函数

SDK 为常见的就绪命令模式提供了辅助函数：

```python
from ucloud_sandbox import wait_for_port, wait_for_process, wait_for_file, wait_for_timeout

# 等待端口可用
wait_for_port(3000)

# 等待进程运行
wait_for_process("node")

# 等待文件存在
wait_for_file("/tmp/ready")

# 等待指定时间
wait_for_timeout(10_000)  # 10 秒
```
