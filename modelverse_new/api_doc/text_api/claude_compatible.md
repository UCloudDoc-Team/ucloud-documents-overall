# Claude (Anthropic) 兼容说明

> **重要提示**：我们提供兼容 Anthropic 标准的API服务，因此我们强烈推荐直接参考 [Anthropic 官方 API 文档](https://docs.anthropic.com/en/api/messages) 获取最全面、最新的参数细节和示例。以下是简化的接口概述，聚焦核心字段和使用说明。

## 概述

UModelverse 平台提供了与 Anthropic Claude API 兼容的 **Messages** 接口，开发者可以使用 Anthropic SDK 或其他支持的工具直接调用 Modelverse 上的模型。

- **请求方法**：POST
- **端点**：`https://api.modelverse.cn/v1/messages`
- **认证**：使用 API 密钥，通过 `x-api-key: {api_key}` 或 `Authorization: Bearer {api_key}` 传递

> **注意**：`/v1/messages` 端点仅支持 Claude 系列模型。其他模型（如 GPT、Gemini、DeepSeek 等）请使用 OpenAI 兼容的 `/v1/chat/completions` 端点。虽然 Claude 和 OpenAI 都使用 `/v1/models` 来获取模型列表，但调用接口不同。

## 主要核心字段

### 请求字段（Request Parameters）

| 字段           | 类型         | 是否必需 | 默认值 | 含义与说明                                                                     |
| -------------- | ------------ | -------- | ------ | ------------------------------------------------------------------------------ |
| model          | string       | 是       | 无     | 模型 ID，如 `claude-sonnet-4-5-20250929`。指定生成响应的模型。                 |
| messages       | array        | 是       | 无     | 对话消息列表。每个消息包含 `role`（user/assistant）和 `content`（文本/图像）。 |
| max_tokens     | integer      | 是       | 无     | 最大生成 token 数。控制响应长度，防止过长输出。                                |
| system         | string/array | 否       | 无     | 系统提示词。定义模型的行为和角色。                                             |
| temperature    | number       | 否       | 1.0    | 采样温度（0 到 1）。控制随机性，高值更创意，低值更确定。                       |
| top_p          | number       | 否       | 无     | 核采样（0 到 1）。控制多样性。                                                 |
| top_k          | integer      | 否       | 无     | Top-K 采样。仅从概率最高的 K 个 token 中采样。                                 |
| stop_sequences | array        | 否       | 无     | 停止序列列表。生成到此停止。                                                   |
| stream         | boolean      | 否       | false  | 是否流式响应。实时返回增量内容。                                               |
| metadata       | object       | 否       | 无     | 元数据对象，可包含 `user_id` 用于追踪。                                        |
| tools          | array        | 否       | 无     | 可用工具列表。启用函数调用功能。                                               |
| tool_choice    | object       | 否       | auto   | 工具选择策略。如 `{"type": "auto"}` 让模型决定调用工具。                       |

### 响应字段（Response）

| 字段          | 类型   | 含义与说明                                                        |
| ------------- | ------ | ----------------------------------------------------------------- |
| id            | string | 响应 ID。唯一标识此次完成。                                       |
| type          | string | 对象类型：`message`。                                             |
| role          | string | 角色：`assistant`。                                               |
| content       | array  | 内容块列表。每个块包含 `type` 和对应内容（如 `text`）。           |
| model         | string | 使用的模型 ID。                                                   |
| stop_reason   | string | 停止原因：`end_turn`、`max_tokens`、`stop_sequence`、`tool_use`。 |
| stop_sequence | string | 触发停止的序列（如适用）。                                        |
| usage         | object | 使用统计。包含 `input_tokens` 和 `output_tokens`。                |

## 快速开始

### 安装 Anthropic SDK

```bash
pip install anthropic
```

### 示例代码

<!-- tabs:start -->
#### ** Python **

```python
import anthropic

client = anthropic.Anthropic(
    api_key="<MODELVERSE_API_KEY>",
    base_url="https://api.modelverse.cn"
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(message.content[0].text)
```

#### ** Python 流式 **

```python
import anthropic

client = anthropic.Anthropic(
    api_key="<MODELVERSE_API_KEY>",
    base_url="https://api.modelverse.cn"
)

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short story about AI."}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

#### ** curl **

```bash
curl https://api.modelverse.cn/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MODELVERSE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

#### ** curl 流式 **

```bash
curl https://api.modelverse.cn/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MODELVERSE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```
<!-- tabs:end -->

## 多模态支持

Claude 兼容接口支持图像输入，可以通过 base64 编码或 URL 方式传递图像：

### 使用 URL 方式

```python
import anthropic

client = anthropic.Anthropic(
    api_key="<MODELVERSE_API_KEY>",
    base_url="https://api.modelverse.cn"
)

# 使用 URL 传递图像
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)

print(message.content[0].text)
```

### 使用 base64 编码

```python
import anthropic
import base64

client = anthropic.Anthropic(
    api_key="<MODELVERSE_API_KEY>",
    base_url="https://api.modelverse.cn"
)

# 使用 base64 编码图像
with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)

print(message.content[0].text)
```

## 工具调用（Function Calling）

```python
import anthropic

client = anthropic.Anthropic(
    api_key="<MODELVERSE_API_KEY>",
    base_url="https://api.modelverse.cn"
)

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather like in Beijing?"}
    ]
)

print(message.content)
```

## 模型列表

更多受支持的 Claude 兼容模型，请参考【获取模型列表】或访问 [UModelverse 模型中心](https://console.ucloud.cn/modelverse/model-center)。

> 更多字段详情，见 [Anthropic 官方文档](https://docs.anthropic.com/en/api/messages)
