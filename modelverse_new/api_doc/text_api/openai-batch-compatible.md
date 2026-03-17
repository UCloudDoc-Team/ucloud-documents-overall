# OpenAI兼容-Batch

## 前提条件

- 已开通 ModelVerse 服务，并已获取 API Key，参考 [认证鉴权](/api_doc/common/certificate)
- 建议您配置 API Key 到环境变量中以降低 API Key 的泄露风险

如果您使用 OpenAI Python SDK 调用 Batch 接口，请通过以下命令安装最新版 OpenAI SDK：

```bash
pip3 install -U openai
```

## 适用范围

**支持的模型：**

目前仅支持`qwen3-vl-flash`模型

## 快速开始

### 运行脚本

执行此 Python 脚本。如果需要调整文件路径或其他参数，请根据实际情况修改代码。

```python
import os
import io
import tempfile
from pathlib import Path
from urllib.parse import urlparse
import requests
from openai import OpenAI
import time

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，可将下行替换为：api_key="sk-xxx"
    # 但不建议在生产环境中直接将 API Key 硬编码到代码中，以减少 API Key 泄露风险
    # 获取 API Key：https://console.ucloud.cn/modelverse/experience/api-keys
    api_key=os.getenv(
        "MODELVERSE_API_KEY", "<MODELVERSE_API_KEY>"
    ),
    base_url="https://api.modelverse.cn/v1",
)


def upload_file(file_path):
    print(f"正在上传包含请求信息的JSONL文件...")

    # 判断是否为URL
    if file_path.startswith(("http://", "https://")):
        print(f"检测到公网链接，正在下载文件...")
        response = requests.get(file_path)
        response.raise_for_status()

        # 从URL中提取文件名
        parsed_url = urlparse(file_path)
        filename = os.path.basename(parsed_url.path) or "batch_input.jsonl"

        # 使用内存中的文件对象上传
        file_content = io.BytesIO(response.content)
        file_content.name = filename
        file_object = client.files.create(file=file_content, purpose="batch")
    else:
        # 本地文件路径
        file_object = client.files.create(file=Path(file_path), purpose="batch")

    print(f"文件上传成功。得到文件ID: {file_object.id}\n")
    return file_object.id


def create_batch_job(input_file_id):
    print(f"正在基于文件ID，创建Batch任务...")
    # 请注意：此处 endpoint 参数值需和输入文件中的 url 字段保持一致
    # qwen3-vl-flash 模型填写 /v1/chat/completions
    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/chat/ds-test",
        completion_window="24h",
    )
    print(f"Batch任务创建完成。得到Batch任务ID: {batch.id}\n")
    return batch.id


def check_job_status(batch_id):
    print(f"正在检查Batch任务状态...")
    batch = client.batches.retrieve(batch_id=batch_id)
    print(f"Batch任务状态: {batch.status}\n")
    return batch.status


def get_output_id(batch_id):
    print(f"正在获取Batch任务中执行成功请求的输出文件ID...")
    batch = client.batches.retrieve(batch_id=batch_id)
    print(f"输出文件ID: {batch.output_file_id}\n")
    return batch.output_file_id


def get_error_id(batch_id):
    print(f"正在获取Batch任务中执行错误请求的输出文件ID...")
    batch = client.batches.retrieve(batch_id=batch_id)
    print(f"错误文件ID: {batch.error_file_id}\n")
    return batch.error_file_id


def download_results(output_file_id, output_file_path):
    print(f"正在打印并下载Batch任务的请求成功结果...")
    content = client.files.content(output_file_id)
    print(f"打印请求成功结果的前1000个字符内容: {content.text[:1000]}...\n")
    content.write_to_file(output_file_path)
    print(f"完整的输出结果已保存至本地输出文件result.jsonl\n")


def download_errors(error_file_id, error_file_path):
    print(f"正在打印并下载Batch任务的请求失败信息...")
    content = client.files.content(error_file_id)
    print(f"打印请求失败信息的前1000个字符内容: {content.text[:1000]}...\n")
    content.write_to_file(error_file_path)
    print(f"完整的请求失败信息已保存至本地错误文件error.jsonl\n")


def main():
    input_file_path = (
        "https://umodelverse-inference.cn-wlcb.ufileos.com/test-batch.jsonl"
    )
    output_file_path = "result.jsonl"
    error_file_path = "error.jsonl"

    try:
        # Step 1: 上传包含请求信息的JSONL文件
        input_file_id = upload_file(input_file_path)

        # Step 2: 基于输入文件ID，创建Batch任务
        batch_id = create_batch_job(input_file_id)

        # Step 3: 检查Batch任务状态直到结束
        status = ""
        while status not in ["completed", "failed", "expired", "cancelled"]:
            status = check_job_status(batch_id)
            print(f"等待任务完成...")
            time.sleep(10)

        if status == "failed":
            batch = client.batches.retrieve(batch_id)
            print(f"Batch任务失败。错误信息为:{batch.errors}\n")
            return

        # Step 4: 下载结果
        output_file_id = get_output_id(batch_id)
        if output_file_id:
            download_results(output_file_id, output_file_path)

        error_file_id = get_error_id(batch_id)
        if error_file_id:
            download_errors(error_file_id, error_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

```

### 验证测试结果

任务状态显示 `completed`。

结果文件 `result.jsonl` 

```jsonl
{"id":"39dbd7fd-a261-96f1-85e9-c795ac379b8d","custom_id":"2","response":{"status_code":200,"request_id":"39dbd7fd-a261-96f1-85e9-c795ac379b8d","body":{"created":1766385214,"usage":{"completion_tokens":166,"prompt_tokens":23,"completion_tokens_details":{"text_tokens":166},"prompt_tokens_details":{"text_tokens":23},"total_tokens":189},"model":"qwen3-vl-flash","id":"chatcmpl-39dbd7fd-a261-96f1-85e9-c795ac379b8d","choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"Baaaah! *grazing peacefully in the sunlit field* \n\nOh, hello there! I'm just a little sheep enjoying my grassy life. I love nibbling on fresh green blades and watching the clouds drift by. Sometimes I get a bit sleepy and lie down with my woolly coat catching the breeze.\n\nYou wanna hear about my favorite things? I adore when the farmer brings out the hay bales in winter, and I always get extra treats on Sundays! Though I must say, I’m a bit of a chatterbox — I’ll happily chat about anything from the best grazing spots to how fluffy my wool is.\n\nWhat’s on your mind, friend? Maybe you’d like to hear about my latest adventure or just sit with me under the big oak tree? Baaaaah! 🐑✨"}}],"object":"chat.completion"}},"error":null}
{"id":"78ff9450-6a4f-917d-80d4-d9628c808d8d","custom_id":"3","response":{"status_code":200,"request_id":"78ff9450-6a4f-917d-80d4-d9628c808d8d","body":{"created":1766385214,"usage":{"completion_tokens":103,"prompt_tokens":23,"completion_tokens_details":{"text_tokens":103},"prompt_tokens_details":{"text_tokens":23},"total_tokens":126},"model":"qwen3-vl-flash","id":"chatcmpl-78ff9450-6a4f-917d-80d4-d9628c808d8d","choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"Moo! 🐄 I’m a cow — big, fluffy, and full of gentle vibes. I love munching on grass, lounging in the sun, and maybe getting a little muddy if it’s a good day. I might not be the smartest animal around, but I’ve got a heart as big as my udder (and I know that’s a lot!). What’s on your mind? Need advice? A cuddle? Or just someone to moo with? 😊🐄"}}],"object":"chat.completion"}},"error":null}
{"id":"6b9fecd9-4139-9190-b9d6-4f473c3f0e9b","custom_id":"1","response":{"status_code":200,"request_id":"6b9fecd9-4139-9190-b9d6-4f473c3f0e9b","body":{"created":1766385216,"usage":{"completion_tokens":72,"prompt_tokens":23,"completion_tokens_details":{"text_tokens":72},"prompt_tokens_details":{"text_tokens":23},"total_tokens":95},"model":"qwen3-vl-flash","id":"chatcmpl-6b9fecd9-4139-9190-b9d6-4f473c3f0e9b","choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"Oink! 🐷 I’m a pig — snorting, rooting around in the mud, and totally loving it. You want me to be your farmyard buddy? I’ll roll in the dirt, snuffle for treats, and maybe even do a little dance if you give me some apples. What’s up, friend? 🍏🐷"}}],"object":"chat.completion"}},"error":null}
```

---

### 执行正式Batch任务

通过测试验证后，您可以通过以下步骤来执行正式的 Batch 任务流程：

1. 参考输入文件要求准备输入文件，并将文件中的 `model` 参数设置为支持的模型，`url` 设置为：
   -  `/v1/chat/completions`

2. 替换上面 Python 脚本中的 `endpoint`

> **重要**：请确保脚本中的 `endpoint` 与输入文件中的 `url` 参数保持一致。

3. 运行脚本，等待任务完成：
   - 若任务成功，将在同一目录下生成输出结果文件 `result.jsonl`
   - 若任务失败，则程序退出并打印错误信息
   - 如果存在错误文件ID，将在同一目录下生成错误文件 `error.jsonl` 以供检查

---

## 数据文件格式说明

### 输入文件

创建批量推理任务前，需先准备一个符合以下规范的文件：

| 规范       | 说明                                                        |
| ---------- | ----------------------------------------------------------- |
| 格式       | UTF-8 编码的 JSONL（每行一个独立 JSON 对象）                |
| 规模限制   | 单文件 ≤ 50,000 个请求，且 ≤ 500 MB                         |
| 单行限制   | 每个 JSON 对象 ≤ 6 MB，且不超过模型上下文长度               |
| 一致性要求 | 同一文件内所有请求须使用相同模型及思考模式（如适用）        |
| 唯一标识   | 每个请求必须包含文件内唯一的 `custom_id` 字段，用于结果匹配 |

#### 请求示例

可下载示例文件 `test.jsonl`，内容为：

```jsonl
{"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen3-vl-flash","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你好！有什么可以帮助你的吗？"}]}}
{"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen3-vl-flash","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}]}}
```

#### 请求参数

| 字段                   | 类型    | 必选 | 描述                                                                                                                                                                                                             |
| ---------------------- | ------- | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `custom_id`            | String  | 是   | 用户自定义的请求ID，每一行表示一条请求，每一条请求有一个唯一的 custom_id。Batch 任务结束后，可以在结果文件中找到该 custom_id 对应的请求结果                                                                      |
| `method`               | String  | 是   | 请求方法，当前只支持 `POST`                                                                                                                                                                                      |
| `url`                  | String  | 是   | API 关联的 URL，需和创建 Batch 任务时的 endpoint 字段保持一致。<br>- Embedding 文本向量模型填写 `/v1/embeddings`<br>- 测试模型 batch-test-model 填写 `/v1/chat/ds-test`<br>- 其他模型填写 `/v1/chat/completions` |
| `body`                 | Object  | 是   | 模型调用的请求体，包含调用模型所需的全部参数，如 model、messages、enable_thinking、thinking_budget 等。请求体中的参数与实时推理接口所支持的参数保持一致                                                          |
| `body.model`           | String  | 是   | 本次 Batch 任务使用的模型。**重要**：同一任务的批量请求务必选择同一模型，其思考模式（若支持）也须保持一致                                                                                                        |
| `body.messages`        | Array   | 是   | 消息列表                                                                                                                                                                                                         |
| `body.enable_thinking` | Boolean | 否   | 表示是否开启深度思考，默认为 false。设置为 true 时，qwen3-vl-flash将开启推理模式                                                                                                                                 |
| `body.thinking_budget` | Integer | 否   | 思考过程最大 Token 数。如果模型思考过程生成的 Token 数超过 thinking_budget，推理内容会进行截断并立刻开始生成最终回复内容。                                                                                       |

扩展参数示例：

```jsonl
{"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-turbo-latest","stream":true,"enable_thinking":true,"thinking_budget":50,"messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你是谁？"}],"max_tokens": 1000,"temperature":0.7}}
{"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-turbo-latest","stream":true,"enable_thinking":true,"thinking_budget":50,"messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}],"max_tokens": 1000,"temperature":0.7}}
```

messages 示例：

```json
[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "What is 2+2?"}
]
```

### 输出文件

JSONL 文件，每行一个 JSON，对应一个请求结果。

#### 返回示例

单行内容示例：

```jsonl
{"id":"73291560-xxx","custom_id":"1","response":{"status_code":200,"request_id":"73291560-7616-97bf-87f2-7d747bbe84fd","body":{"created":1742303743,"usage":{"completion_tokens":7,"prompt_tokens":26,"total_tokens":33},"model":"qwen3-vl-flash","id":"chatcmpl-73291560-7616-97bf-87f2-7d747bbe84fd","choices":[{"finish_reason":"stop","index":0,"message":{"content":"2+2 equals 4."}}],"object":"chat.completion"}},"error":null}
```

多行内容示例：

```jsonl
{"id":"c308ef7f-xxx","custom_id":"1","response":{"status_code":200,"request_id":"c308ef7f-0824-9c46-96eb-73566f062426","body":{"created":1742303743,"usage":{"completion_tokens":35,"prompt_tokens":26,"total_tokens":61},"model":"qwen3-vl-flash","id":"chatcmpl-c308ef7f-0824-9c46-96eb-73566f062426","choices":[{"finish_reason":"stop","index":0,"message":{"content":"你好！当然可以。无论是需要信息查询、学习资料、解决问题的方法，还是其他任何帮助，我都在这里为你提供支持。请告诉我你需要什么方面的帮助？"}}],"object":"chat.completion"}},"error":null}
{"id":"73291560-xxx","custom_id":"2","response":{"status_code":200,"request_id":"73291560-7616-97bf-87f2-7d747bbe84fd","body":{"created":1742303743,"usage":{"completion_tokens":7,"prompt_tokens":26,"total_tokens":33},"model":"qwen3-vl-flash","id":"chatcmpl-73291560-7616-97bf-87f2-7d747bbe84fd","choices":[{"finish_reason":"stop","index":0,"message":{"content":"2+2 equals 4."}}],"object":"chat.completion"}},"error":null}
```

#### 返回参数

| 字段                | 类型    | 必选 | 描述                            |
| ------------------- | ------- | ---- | ------------------------------- |
| `id`                | String  | 是   | 请求ID                          |
| `custom_id`         | String  | 是   | 用户自定义的请求ID              |
| `response`          | Object  | 否   | 请求结果                        |
| `error`             | Object  | 否   | 异常响应结果                    |
| `error.code`        | String  | 否   | 错误码                          |
| `error.message`     | String  | 否   | 错误信息                        |
| `completion_tokens` | Integer | 否   | 完成生成所需的 token 数         |
| `prompt_tokens`     | Integer | 否   | prompt 的 token 数              |
| `reasoning_tokens`  | Integer | 否   | 深度思考模型的思考过程 token 数 |
| `model`             | String  | 否   | 本次任务进行推理的模型          |
| `reasoning_content` | String  | 否   | 深度思考模型的思考过程          |

---

## 具体流程

### 1. 准备与上传文件

创建 Batch 任务前，需要您将准备好的符合输入文件要求的 JSONL 文件，通过文件上传接口上传后，获取 `file_id`，通过 `purpose` 参数指定上传文件的用途为 `batch`。

**限制说明：**
- 单个文件最大为 500 MB
- 当前账号下的存储空间支持的最大文件数为 10000 个
- 文件总量不超过 100 GB
- 文件暂时没有有效期

当您的文件空间达到限制后，可以通过 OpenAI 兼容-File 接口删除不需要的文件以释放空间。

#### 请求示例

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，可将下行替换为：api_key="sk-xxx"
    # 获取 API Key：https://console.ucloud.cn/modelverse/experience/api-keys
    api_key=os.getenv("MODELVERSE_API_KEY"),
    base_url="https://api.modelverse.cn/v1",
)

# test.jsonl 是一个本地示例文件，purpose 必须是 batch
file_object = client.files.create(file=Path("test.jsonl"), purpose="batch")
print(file_object.model_dump_json())
```

测试文件 `test.jsonl` 内容：

```jsonl
{"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen3-vl-flash","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你好！有什么可以帮助你的吗？"}]}}
{"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen3-vl-flash","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}]}}
```

#### 返回示例

```json
{
    "id": "file-batch-xxx",
    "bytes": 437,
    "created_at": 1742304153,
    "filename": "test.jsonl",
    "object": "file",
    "purpose": "batch",
    "status": "processed",
    "status_details": null
}
```

### 2. 创建Batch任务

您可以通过 `input_file_id` 参数传入准备与上传文件接口返回的文件 ID 来创建 Batch 任务。

#### 请求示例

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY"),
    base_url="https://api.modelverse.cn/v1",
)

batch = client.batches.create(
    input_file_id="file-batch-xxx",  # 上传文件返回的 id
    endpoint="/v1/chat/completions",  
    completion_window="24h",
    metadata={'ds_name': "任务名称", 'ds_description': '任务描述'}
)
print(batch)
```

#### 输入参数

| 字段                      | 类型   | 传参方式 | 必选 | 描述                                                                      |
| ------------------------- | ------ | -------- | ---- | ------------------------------------------------------------------------- |
| `input_file_id`           | String | Body     | 是   | 用于指定文件 ID，作为 Batch 任务的输入文件                                |
| `endpoint`                | String | Body     | 是   | 访问路径，需和输入文件中的 url 字段保持一致。<br>- `/v1/chat/completions` |
| `completion_window`       | String | Body     | 是   | 等待时间，支持最短 24h，最长 336h，仅支持整数。支持 "h" 和 "d" 两个单位   |
| `metadata`                | Map    | Body     | 否   | 任务扩展元数据，以键值对形式附加信息                                      |
| `metadata.ds_name`        | String | Body     | 否   | 任务名称，长度不超过 100 个字符                                           |
| `metadata.ds_description` | String | Body     | 否   | 任务描述，长度不超过 200 个字符                                           |

#### 返回示例

```json
{
    "id": "batch_xxx",
    "object": "batch",
    "endpoint": "/v1/chat/completions",
    "errors": null,
    "input_file_id": "file-batch-xxx",
    "completion_window": "24h",
    "status": "validating",
    "output_file_id": null,
    "error_file_id": null,
    "created_at": 1742367779,
    "in_progress_at": null,
    "expires_at": null,
    "finalizing_at": null,
    "completed_at": null,
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": null,
    "cancelled_at": null,
    "request_counts": {
        "total": 0,
        "completed": 0,
        "failed": 0
    },
    "metadata": {
        "ds_name": "任务名称",
        "ds_description": "任务描述"
    }
}
```

#### 返回参数

| 字段                      | 类型    | 描述                                                                                             |
| ------------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| `id`                      | String  | Batch 任务 ID                                                                                    |
| `object`                  | String  | 对象类型，固定值 `batch`                                                                         |
| `endpoint`                | String  | 访问路径                                                                                         |
| `errors`                  | Map     | 错误信息                                                                                         |
| `input_file_id`           | String  | 文件 ID                                                                                          |
| `completion_window`       | String  | 等待时间                                                                                         |
| `status`                  | String  | 任务状态：validating、failed、in_progress、finalizing、completed、expired、cancelling、cancelled |
| `output_file_id`          | String  | 执行成功请求的输出文件 id                                                                        |
| `error_file_id`           | String  | 执行错误请求的输出文件 id                                                                        |
| `created_at`              | Integer | 任务创建的 Unix 时间戳（秒）                                                                     |
| `in_progress_at`          | Integer | 任务开始运行的 Unix 时间戳（秒）                                                                 |
| `expires_at`              | Integer | 任务开始超时的时间戳（秒）                                                                       |
| `finalizing_at`           | Integer | 任务最后开始时间戳（秒）                                                                         |
| `completed_at`            | Integer | 任务完成的时间戳（秒）                                                                           |
| `failed_at`               | Integer | 任务失败的时间戳（秒）                                                                           |
| `expired_at`              | Integer | 任务超时的时间戳（秒）                                                                           |
| `cancelling_at`           | Integer | 任务设置为取消中的时间戳（秒）                                                                   |
| `cancelled_at`            | Integer | 任务取消的时间戳（秒）                                                                           |
| `request_counts`          | Map     | 不同状态的请求数量                                                                               |
| `metadata`                | Map     | 附加信息，键值对                                                                                 |
| `metadata.ds_name`        | String  | 当前任务的任务名称                                                                               |
| `metadata.ds_description` | String  | 当前任务的任务描述                                                                               |

### 3. 查询与管理Batch任务

#### 查询Batch任务详情

通过传入创建 Batch 任务返回的 Batch 任务 ID，来查询指定 Batch 任务的信息。当前仅支持查询 30 天之内创建的 Batch 任务。

**接口限流**：每个账号每分钟 1000 次（建议创建 Batch 任务之后，每分钟调用 1 次该查询接口获取任务信息）。

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY"),
    base_url="https://api.modelverse.cn/v1",
)

batch = client.batches.retrieve("batch_id")  # 将 batch_id 替换为 Batch 任务的 id
print(batch)
```

**输入参数**

| 字段       | 类型   | 传参方式 | 必选 | 描述                                                        |
| ---------- | ------ | -------- | ---- | ----------------------------------------------------------- |
| `batch_id` | String | Path     | 是   | 需要查询的 Batch 任务的 ID，以 batch 开头，例如 "batch_xxx" |

返回参数中 `output_file_id` 和 `error_file_id` 可以通过下载 Batch 结果文件获取内容。

#### 查询Batch任务列表

您可以使用 `batches.list()` 方法查询 Batch 任务列表，并通过分页机制逐步获取完整的任务列表。

**接口限流**：每个账号每分钟 100 次。

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY"),
    base_url="https://api.modelverse.cn/v1",
)

batches = client.batches.list(
    limit=2,
    extra_query={
        'status': 'completed,expired'
    }
)
print(batches)
```

**输入参数**

| 字段             | 类型    | 传参方式 | 必选 | 描述                                                           |
| ---------------- | ------- | -------- | ---- | -------------------------------------------------------------- |
| `after`          | String  | Query    | 否   | 用于分页的游标，取值为 Batch 任务 ID，表示查询该 ID 之后的数据 |
| `limit`          | Integer | Query    | 否   | 每次查询返回的 Batch 任务数量，范围 [1,100]，默认 20           |
| `ds_name`        | String  | Query    | 否   | 根据任务名称进行模糊筛选                                       |
| `input_file_ids` | String  | Query    | 否   | 筛选多个文件 ID，以英文逗号分隔，最多可填写 20 个              |
| `status`         | String  | Query    | 否   | 筛选多个状态，以英文逗号分隔                                   |
| `create_after`   | String  | Query    | 否   | 筛选在此时间点之后创建的任务，格式：yyyyMMddHHmmss             |
| `create_before`  | String  | Query    | 否   | 筛选在此时间点之前创建的任务，格式：yyyyMMddHHmmss             |

**返回示例**

```json
{
  "object": "list",
  "data": [
    {
      "id": "batch_xxx",
      "object": "batch",
      "endpoint": "/v1/chat/completions",
      "errors": null,
      "input_file_id": "file-batch-xxx",
      "completion_window": "24h",
      "status": "completed",
      "output_file_id": "file-batch_output-xxx",
      "error_file_id": null,
      "created_at": 1722234109,
      "in_progress_at": 1722234109,
      "expires_at": null,
      "finalizing_at": 1722234165,
      "completed_at": 1722234165,
      "failed_at": null,
      "expired_at": null,
      "cancelling_at": null,
      "cancelled_at": null,
      "request_counts": {
        "total": 100,
        "completed": 95,
        "failed": 5
      },
      "metadata": {}
    }
  ],
  "first_id": "batch_xxx",
  "last_id": "batch_xxx",
  "has_more": true
}
```

**返回参数**

| 字段       | 类型    | 描述                         |
| ---------- | ------- | ---------------------------- |
| `object`   | String  | 类型，固定值 `list`          |
| `data`     | Array   | Batch 任务对象数组           |
| `first_id` | String  | 当前页第一个 Batch 任务 ID   |
| `last_id`  | String  | 当前页最后一个 Batch 任务 ID |
| `has_more` | Boolean | 是否有下一页                 |

#### 取消Batch任务

通过传入创建 Batch 任务返回的 Batch 任务 ID，来取消指定的 Batch 任务。

**接口限流**：每个账号每分钟 1000 次。

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY"),
    base_url="https://api.modelverse.cn/v1",
)

batch = client.batches.cancel("batch_id")  # 将 batch_id 替换为 Batch 任务的 id
print(batch)
```

**输入参数**

| 字段       | 类型   | 传参方式 | 必选 | 描述                                                        |
| ---------- | ------ | -------- | ---- | ----------------------------------------------------------- |
| `batch_id` | String | Path     | 是   | 需要取消的 Batch 任务的 id，以 batch 开头，例如 "batch_xxx" |

### 4. 下载Batch结果文件

在 Batch 推理任务结束后，您可以通过接口下载结果文件。

您可以通过查询 Batch 任务详情或通过查询 Batch 任务列表返回参数中的 `output_file_id` 获取下载文件的 `file_id`。仅支持下载以 `file-batch_output` 开头的 `file_id` 对应的文件。

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY"),
    base_url="https://api.modelverse.cn/v1",
)

content = client.files.content(file_id="file-batch_output-xxx")
# 打印结果文件内容
print(content.text)
# 保存结果文件至本地
content.write_to_file("result.jsonl")
```

**输入参数**

| 字段      | 类型   | 传参方式 | 必选 | 描述                                                                                            |
| --------- | ------ | -------- | ---- | ----------------------------------------------------------------------------------------------- |
| `file_id` | String | Path     | 是   | 需要下载的文件的 ID，查询 Batch 任务详情或通过查询 Batch 任务列表返回参数中的 output_file_id 值 |

**返回示例**

```jsonl
{"id":"c308ef7f-xxx","custom_id":"1","response":{"status_code":200,"request_id":"c308ef7f-0824-9c46-96eb-73566f062426","body":{"created":1742303743,"usage":{"completion_tokens":35,"prompt_tokens":26,"total_tokens":61},"model":"qwen3-vl-flash","id":"chatcmpl-c308ef7f-0824-9c46-96eb-73566f062426","choices":[{"finish_reason":"stop","index":0,"message":{"content":"你好！当然可以。无论是需要信息查询、学习资料、解决问题的方法，还是其他任何帮助，我都在这里为你提供支持。请告诉我你需要什么方面的帮助？"}}],"object":"chat.completion"}},"error":null}
{"id":"73291560-xxx","custom_id":"2","response":{"status_code":200,"request_id":"73291560-7616-97bf-87f2-7d747bbe84fd","body":{"created":1742303743,"usage":{"completion_tokens":7,"prompt_tokens":26,"total_tokens":33},"model":"qwen3-vl-flash","id":"chatcmpl-73291560-7616-97bf-87f2-7d747bbe84fd","choices":[{"finish_reason":"stop","index":0,"message":{"content":"2+2 equals 4."}}],"object":"chat.completion"}},"error":null}
```

---

## 计费说明

**计费单价**：所有成功请求的输入和输出 Token，单价均为对应模型实时推理价格的 **50%**。

**计费范围**：
- 仅对任务中成功执行的请求进行计费
- 文件解析失败、任务执行失败、或行级错误请求均不产生费用
- 对于被取消的任务，在取消操作前已成功完成的请求仍会正常计费
