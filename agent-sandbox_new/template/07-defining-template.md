# 定义模板

<subtitle>掌握模板定义的完整 API，包括文件操作、包安装及命令执行。</subtitle>

?> **前置条件**：请先完成 [API Key 配置](/agent-sandbox/docs/product/01-prerequisites)

### 方法链

所有模板方法都返回模板实例，允许使用流畅的 API：

```python
from ucloud_sandbox import Template, wait_for_timeout

template = (
    Template()
    .from_ubuntu_image("22.04")
    .set_workdir("/app")
    .copy("package.json", "/app/package.json")
    .run_cmd("npm install")
    .set_start_cmd("npm start", wait_for_timeout(10_000))
)
```

### 用户和工作目录

设置模板的工作目录和用户：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

# 设置工作目录
template.set_workdir("/app")

# 设置用户（后续命令将以该用户身份运行）
template.set_user("node")
template.set_user("1000:1000")  # 用户 ID 和组 ID
```

### 复制文件

将文件从本地文件系统复制到模板：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

# 复制单个文件
template.copy("package.json", "/app/package.json")

# 复制多个文件到同一目标
template.copy(["file1", "file2"], "/app/file")

# 使用 copy_items 批量定义复制规则
template.copy_items([
    {"src": "src/", "dest": "/app/src/"},
    {"src": "package.json", "dest": "/app/package.json"},
])

# 指定用户与文件权限（mode）
template.copy("config.json", "/app/config.json", user="appuser", mode=0o644)
```

### 文件操作

在模板构建期间执行各种文件操作：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

# 删除文件或目录
template.remove("/tmp/old-file")
template.remove("/tmp/old-dir", recursive=True)
template.remove("/tmp/file", force=True)  # 强制删除

# 重命名文件或目录
template.rename("/old/path", "/new/path")
template.rename("/old/path", "/new/path", force=True)  # 强制重命名

# 创建目录
template.make_dir("/app/data")
template.make_dir("/app/data", mode=0o755)  # 设置权限

# 创建符号链接
template.make_symlink("/path/to/target", "/path/to/link")
```

### 安装包

使用包管理器安装包：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

# 安装 Python 包
template.pip_install(["requests", "pandas", "numpy"])

# 为当前用户安装（非全局）
template.pip_install(["requests", "pandas", "numpy"], g=False)

# 安装 Node.js 包
template.npm_install(["express", "lodash"])

# 安装 Node.js 包（全局）
template.npm_install(["express", "lodash"], g=True)

# 安装 Bun 包
template.bun_install(["express", "lodash"])

# 安装 Bun 包（全局）
template.bun_install(["express", "lodash"], g=True)

# 安装系统包 (Ubuntu/Debian)
template.apt_install(["curl", "wget", "git"])
```

### Git 操作

在模板构建期间克隆 Git 仓库（需要安装 `git`）：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

# 克隆仓库
template.git_clone("https://github.com/user/repo.git")

# 克隆仓库到特定路径
template.git_clone("https://github.com/user/repo.git", "/app/repo")

# 克隆特定分支
template.git_clone("https://github.com/user/repo.git", "/app/repo", branch="main")

# 带有深度限制的浅克隆
template.git_clone("https://github.com/user/repo.git", "/app/repo", depth=1)
```

### 环境变量

在模板中设置环境变量：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

template.set_envs({
    "NODE_ENV": "production",
    "API_KEY": "your-api-key",
    "DEBUG": "true",
})
```

### 运行命令

在模板构建期间执行 shell 命令：

```python
from ucloud_sandbox import Template

template = Template().from_base_image()

# 运行单个命令
template.run_cmd("apt-get update && apt-get install -y curl")

# 运行多个命令
template.run_cmd(["apt-get update", "apt-get install -y curl", "curl --version"])

# 以特定用户身份运行命令
template.run_cmd("npm install", user="node")
```
