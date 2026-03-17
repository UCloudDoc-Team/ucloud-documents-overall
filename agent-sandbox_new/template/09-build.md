# 构建模板

<subtitle>执行模板构建并监控构建进度与状态。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

?> 在调用 `Template.build(...)` 之前，请先定义 `template` 变量，见：[定义模板](/agent-sandbox/docs/sdk/template/07-defining-template)

## 构建并等待完成

`build` 方法会构建模板并等待完成，返回构建信息（包含模板 ID 与构建 ID）。

```python
from ucloud_sandbox import Template, default_build_logger

build_info = Template.build(
    template,
    alias="my-template",  # 模板别名（必填）
    cpu_count=2,  # CPU 核心数
    memory_mb=2048,  # 内存（MB）
    skip_cache=False,  # 是否跳过缓存（复制文件步骤除外）
    on_build_logs=default_build_logger(),  # 日志回调：接收 LogEntry 对象
    api_key="your-api-key",  # 覆盖 API 密钥
    domain="your-domain",  # 覆盖域名
)

# build_info 包含: BuildInfo(alias, template_id, build_id)
```

## 后台构建

`build_in_background` 方法会启动构建并立即返回（不等待完成），适用于「触发构建 → 稍后轮询状态/拉取日志」的场景。

```python
from ucloud_sandbox import Template

build_info = Template.build_in_background(
    template,
    alias="my-template",
    cpu_count=2,
    memory_mb=2048,
)

# 立即返回: BuildInfo(alias, template_id, build_id)
```

## 检查构建状态

使用 `get_build_status` 检查由 `build_in_background` 启动的构建状态。

```python
from ucloud_sandbox import Template

status = Template.get_build_status(
    build_info,
    logs_offset=0,  # 可选：获取日志的偏移量
)

# status 包含构建状态和日志
```

## 示例：带有状态轮询的后台构建

```python
import time
from ucloud_sandbox import Template

# 在后台启动构建
build_info = Template.build_in_background(
    template,
    alias="my-template",
    cpu_count=2,
    memory_mb=2048,
)

# 轮询构建状态
logs_offset = 0
status = "building"

while status == "building":
    build_status = Template.get_build_status(
        build_info,
        logs_offset=logs_offset,
    )

    logs_offset += len(build_status.log_entries)
    status = build_status.status.value

    for log_entry in build_status.log_entries:
        print(log_entry)

    # 等待一小段时间后再次检查状态
    time.sleep(2)

if status == "ready":
    print("Build completed successfully")
else:
    print("Build failed")
```
