# 常见问题与排障

<subtitle>按场景组织的排查清单：认证、构建卡住、命令超时、网络访问与限流。</subtitle>

---

## 快速自检清单

遇到问题时，请按以下顺序排查：

1. **环境变量是否正确**：原生 SDK 用 `AGENTBOX_API_KEY`，E2B 兼容模式用 `E2B_API_KEY` + `E2B_DOMAIN`
2. **模板是否存在**：检查模板别名是否正确，构建是否成功
3. **网络策略是否允许**：沙箱默认可访问外网，但可能被显式禁用
4. **是否触发限流**：检查请求频率和并发数
5. **就绪命令是否满足**：构建卡住最常见的原因

---

## 认证与权限问题

### 现象
- 请求返回 401 / 403 错误
- SDK 提示 API Key 无效或缺失

### 排查步骤

```bash
# 检查环境变量是否设置
echo $AGENTBOX_API_KEY

# 对于 E2B 兼容模式
echo $E2B_API_KEY
echo $E2B_DOMAIN
```

### 常见原因
- 环境变量名称错误（原生 vs E2B）
- 在 CI/容器/子进程中变量未正确传递
- API Key 已过期或被禁用

?> 详见：[前置条件与认证](/agent-sandbox/docs/product/01-prerequisites)

---

## 模板构建卡住

### 现象
- 构建长时间停留在 `building` 状态
- 日志持续输出相同的就绪检查结果

### 排查步骤

1. **检查就绪命令的退出码逻辑**

就绪命令只有返回退出码 `0` 时才会进入快照生成阶段：

```python
# 错误示例：服务未启动完成就返回 0
.set_start_cmd("npm start", wait_for_timeout(1000))  # 1秒太短

# 正确示例：等待端口就绪
.set_start_cmd("npm start", wait_for_port(3000))
```

2. **查看构建日志**

```python
from ucloud_sandbox import Template, default_build_logger

Template.build(
    template,
    alias="my-template",
    on_build_logs=default_build_logger(min_level="debug")  # 开启 debug 级别
)
```

3. **检查启动命令是否正常运行**

确保启动命令本身不会立即退出或报错。

?> 详见：[启动与就绪命令](/agent-sandbox/docs/sdk/template/08-start-and-ready-commands)

---

## 命令执行超时或无输出

### 现象
- `commands.run()` 运行时间过长
- 流式输出未返回或中断

### 排查步骤

1. **使用最小命令验证连通性**

```python
# 先用简单命令测试
result = sandbox.commands.run("echo hello")
print(result.stdout)  # 应输出 hello
```

2. **长任务改为后台执行**

```python
# 后台运行
process = sandbox.commands.run("long_running_task", background=True)

# 轮询输出
for stdout, stderr, _ in process:
    if stdout:
        print(stdout)
```

3. **检查命令本身是否卡住**

在沙箱内手动测试命令，确认不是命令本身的问题。

?> 详见：[命令执行概述](/agent-sandbox/docs/sdk/commands/01-overview)、[后台运行命令](/agent-sandbox/docs/sdk/commands/03-run-commands-in-background)

---

## 网络/外网访问失败

### 现象
- `curl`、`pip install`、`npm install` 无法访问外网
- DNS 解析失败或连接超时

### 排查步骤

1. **确认沙箱的网络策略**

```python
from ucloud_sandbox import Sandbox

# 默认允许外网
sandbox = Sandbox.create(allow_internet_access=True)

# 如果禁用了外网
sandbox = Sandbox.create(allow_internet_access=False)  # 无法访问外网
```

2. **检查是否配置了网络黑白名单**

```python
from ucloud_sandbox import Sandbox, ALL_TRAFFIC

# 检查是否误配了 deny_out（阻止所有出站流量）
sandbox = Sandbox.create(
    network={
        "deny_out": [ALL_TRAFFIC]
    }
)
```

3. **模板构建时的网络**

如果在模板构建阶段需要下载依赖，确保构建环境有网络访问权限。

?> 详见：[网络/互联网访问](/agent-sandbox/docs/sdk/sandbox/10-internet-access)

---

## 限流与资源限制

?> 详见：[配额说明](/agent-sandbox/docs/sdk/sandbox/rate-limit)

---

## 数据持久化问题

### 现象
- 数据未保存，重启后丢失
- 连接存储桶失败

### 排查步骤

1. **确认写入了正确的持久化路径**
2. **检查存储桶连接参数和权限**
3. **确认使用了支持持久化的沙箱配置**

?> 详见：[数据持久化](/agent-sandbox/docs/sdk/sandbox/04-persistence)、[连接存储桶](/agent-sandbox/docs/sdk/sandbox/11-connect-bucket)

---

## 仍有问题？

如果以上排查未能解决您的问题，请收集以下信息并联系技术支持：

- 沙箱 ID / 模板 ID / 构建 ID
- 完整的错误信息和堆栈
- 复现步骤
- SDK 版本和 Python 版本
