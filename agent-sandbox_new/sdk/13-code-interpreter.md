# Code Interpreter

Code Interpreter 提供了一个有状态的 Jupyter 笔记本环境，支持运行 Python 代码、生成图表、处理文件等。它非常适合用于 AI 代码执行、数据分析和可视化任务。

## 引入

Code Interpreter 位于 `ucloud_sandbox.code_interpreter` 模块中。

```python
from ucloud_sandbox.code_interpreter import Sandbox
```

## 快速开始

```python
from ucloud_sandbox.code_interpreter import Sandbox

# 创建一个 Code Interpreter 实例
sandbox = Sandbox.create()

# 运行代码
execution = sandbox.run_code("print('Hello, World!')")
print(execution.logs.stdout)  # 输出: Hello, World!

# 运行带有图表的代码
code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
"""
execution = sandbox.run_code(code)

# 获取结果中的图表（如果有）
for result in execution.results:
    if result.png:
        print(f"Generated PNG image of {len(result.png)} bytes")

sandbox.kill()
```

## 主要功能

- **有状态执行**: 变量和状态在多次 `run_code` 调用之间保持。
- **富媒体输出**: 支持文本、PNG/JPEG 图片、甚至 matplotlib 图表。
- **文件操作**: 可以上传/下载文件到沙箱环境中。

