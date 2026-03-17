# 基础镜像

<subtitle>为您的模板选择或自定义基础镜像。</subtitle>

!> 您的基础镜像必须是基于**Ubuntu**或**Debain**的，否则构建镜像将会失败。

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

## 创建模板

创建模板时，您可以指定选项：

```python
from ucloud_sandbox import Template

template = Template(
    file_context_path=".",  # 自定义文件上下文路径
    file_ignore_patterns=[".git", "node_modules"],  # 要忽略的文件模式
)
```

**文件忽略**：SDK 会自动读取 `.dockerignore` 文件，并将其与您的 `file_ignore_patterns` 合并。匹配这些模式的文件将从上传和哈希计算中排除。

## 定义基础镜像

从预定义的基础镜像中选择或使用自定义基础镜像：

```python
from ucloud_sandbox import Template

# 预定义基础镜像
template.from_ubuntu_image("lts")  # ubuntu:lts
template.from_ubuntu_image("22.04")  # ubuntu:22.04
template.from_debian_image("slim")  # debian:slim
template.from_debian_image("bullseye")  # debian:bullseye
template.from_python_image("3.13")  # python:3.13
template.from_python_image("3.11")  # python:3.11
template.from_node_image("lts")  # node:lts
template.from_node_image("20")  # node:20
template.from_bun_image("1.3")  # oven/bun:1.3

# 自定义基础镜像
template.from_image("custom-image:latest")

# 使用默认基础镜像
template.from_base_image()

# 从现有模板构建
template.from_template("existing-template-alias")

# 解析并从 Dockerfile 构建
template.from_dockerfile("Dockerfile")
template.from_dockerfile("FROM ubuntu:22.04\nRUN apt-get update")
```

> 您每个模板只能调用一次基础镜像方法。后续调用将抛出错误。

## 解析现有的 Dockerfile

使用 `from_dockerfile()` 将现有的 Dockerfile 转换为模板格式：

```python
from ucloud_sandbox import Template, wait_for_timeout

dockerfile_content = """
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl
WORKDIR /app
COPY . .
ENV NODE_ENV=production
ENV PORT=3000
USER appuser
"""

template = (
    Template()
    .from_dockerfile(dockerfile_content)
    .set_start_cmd("npm start", wait_for_timeout(5_000))
)
```

### Dockerfile 指令支持

| 指令                 | 支持情况 | 行为                                                              |
| :------------------- | :------: | :---------------------------------------------------------------- |
| `FROM`               |    ✅    | 设置基础镜像                                                      |
| `RUN`                |    ✅    | 转换为 `run_cmd()`                                                |
| `COPY` / `ADD`       |    ✅    | 转换为 `copy()`                                                   |
| `WORKDIR`            |    ✅    | 转换为 `set_workdir()`                                            |
| `USER`               |    ✅    | 转换为 `set_user()`                                               |
| `ENV`                |    ✅    | 转换为 `set_envs()`；支持 `ENV key=value` 和 `ENV key value` 格式 |
| `CMD` / `ENTRYPOINT` |    ✅    | 转换为 `set_start_cmd()`，并将 20 秒超时作为就绪命令              |
| `EXPOSE`             |    ❌    | 跳过（不支持）                                                    |
| `VOLUME`             |    ❌    | 跳过（不支持）                                                    |

> 不支持多阶段 Dockerfile。
