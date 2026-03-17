# /v1/responses 接口文档

> **重要提示**：我们的服务完全兼容OpenAI Responses API标准，因此我们强烈推荐直接参考[OpenAI官方API文档](https://platform.openai.com/docs/api-reference/responses/create)获取最全面、最新的参数细节和示例。这能让你利用OpenAI的丰富资源（如教程、SDK）。以下是精简版接口概述，聚焦核心字段和使用说明，以减少参数过多带来的复杂性（完整参数约30个，仅列出必需/常用）。如果需要高级功能或完整列表，请优先查阅官方文档。

## 概述

`/v1/responses` 是OpenAI最先进的响应生成接口，支持文本/图像输入、文本/JSON输出、多轮对话、工具调用（如web search、file search）和背景处理。适用于状态化交互和外部数据集成。请求方法：POST。端点：https://api.modelverse.cn/v1/responses（兼容OpenAI格式）。

**认证**：使用API密钥，通过`Authorization: Bearer {api_key}`传递。
**注意**：参数过多（约30个），建议从核心开始使用。支持流式响应和工具扩展。某些参数（如reasoning）仅适用于o-series模型。

## 主要核心字段

### 请求字段（Request Parameters）

精选必需和常用字段（约10个），完整列表请查官方文档。

| 字段                  | 类型          | 是否必需 | 默认值       | 含义与说明 |
|-----------------------|---------------|----------|--------------|------------|
| input          | string | 否      | 无          | 输入内容（文本/图像/文件）。 |
| model                | string       | 是      | 无          | 模型ID，如`gpt-4o`或`o3`。含义：指定响应生成模型。 |
| instructions         | string       | 否      | 无          | 系统消息。含义：指导模型行为，可覆盖先前指令。 |
| max_tokens           | integer      | 否      | 无          | 最大输出token数（包括推理）。含义：控制响应长度。 |
| tools                | array        | 否      | 无          | 工具列表（如函数/web search）。含义：扩展模型能力。 |
| tool_choice          | string/object| 否      | auto        | 工具选择（如`auto`）。含义：决定是否调用工具。 |
| stream               | boolean      | 否      | false       | 是否流式。含义：实时返回事件流。 |
| temperature          | number       | 否      | 1           | 采样温度（0-2）。含义：控制随机性。 |
| top_p                | number       | 否      | 1           | 核采样（0-1）。含义：控制多样性，与temperature互斥。 |
| background           | boolean      | 否      | false       | 是否后台运行。含义：异步处理，长任务适用。 |

* **精简提示**：其他常用如`previous_response_id`（多轮对话）、`reasoning`（推理配置）。避免非必需参数以简化调用。

### 响应字段（Response）

核心响应对象，流式时返回事件序列。

| 字段              | 类型     | 含义与说明 |
|-------------------|----------|------------|
| output           | array   | 生成内容（如文本/工具调用）。含义：模型输出结果。 |
| status           | string  | 状态（如`completed`、`failed`）。含义：响应处理结果。 |
| created          | number  | 创建时间戳。含义：Unix秒。 |
| id               | string  | 响应ID。含义：唯一标识。 |
| model            | string  | 使用模型。含义：确认模型。 |
| usage            | object  | token使用统计。含义：计费依据。 |

* **流式事件**：如`response.created`、`response.output_item.added`等。以`response.done`结束。完整事件列表见官方文档。

## 使用文档

### 基本流程
1. **构建请求**：指定model和input_items。
2. **发送请求**：POST携带密钥。
3. **解析响应**：提取output内容。
4. **流式**：处理事件流。

### 示例（Curl，非流式）
```
curl https://api.modelverse.cn/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "model": "{model_name}",
    "input": "Hello! Who are you?"
  }'
```

预期响应（简化）：
```json
{
  "id": "resp-123",
  "object": "response",
  "created": 1677652288,
  "model": "gpt-4o",
  "output": [{"type": "text", "text": "Hi!"}],
  "status": "completed",
  "usage": {"total_tokens": 20}
}
```

### 示例（Python，流式）
```python
import openai

client = openai.OpenAI(api_key="{api_key}", base_url="https://api.modelverse.cn/v1/")
stream = client.responses.create(
    model="{model_name}",
    input_items=[{"type": "text", "text": "Hello!"}],
    stream=True
)
for event in stream:
    print(event)  # 如 response.delta
```

更多细节，请直接参考[OpenAI官方文档](https://platform.openai.com/docs/api-reference/responses/create)。