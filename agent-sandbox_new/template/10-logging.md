# 构建日志

<subtitle>实时获取模板构建日志并自定义日志处理逻辑。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

构建过程中会通过 `on_build_logs` 回调实时推送构建日志。您可以使用默认的日志处理器，也可以自定义处理逻辑。

?> 构建入口与状态轮询请参阅：[构建模板](/agent-sandbox/docs/sdk/template/09-build)

## 默认日志处理器

SDK 提供 `default_build_logger` 函数，可按级别过滤并输出日志：

```python
from ucloud_sandbox import Template, default_build_logger

Template.build(
    template,
    alias="my-template",
    on_build_logs=default_build_logger(
        min_level="info",  # 要显示的最低日志级别
    )
)
```

