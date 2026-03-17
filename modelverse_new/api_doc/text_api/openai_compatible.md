# OpenAI Chat Completions 说明

> **重要提示**：我们的服务完全兼容OpenAI API标准，因此我们强烈推荐直接参考[OpenAI官方API文档](https://platform.openai.com/docs/api-reference/chat/create)获取最全面、最新的参数细节和示例。这能让你利用OpenAI的丰富资源（如教程、SDK）。以下是简化的接口概述，聚焦核心字段和使用说明。如果需要高级功能或更新，请优先查阅官方文档。我们已补充字段的具体含义，以补足快速开始文档的简单实用性。

## 概述

`/v1/chat/completions` 接口用于基于对话消息生成模型响应，支持文本、图像和音频输入。适用于聊天、内容生成等场景。支持流式响应（streaming）。请求方法：POST。端点：https://api.modelverse.cn/v1/chat/completions（兼容OpenAI格式）。

**认证**：使用API密钥，通过`Authorization: Bearer {api_key}`传递。
**注意**：某些参数仅适用于特定模型（如推理模型的`reasoning_effort`）。弃用参数（如`functions`）请避免使用，改用`tools`。

## 主要核心字段

### 请求字段（Request Parameters）

| 字段                  | 类型          | 是否必需 | 默认值       | 含义与说明 |
|-----------------------|---------------|----------|--------------|------------|
| messages             | array        | 是      | 无          | 对话消息列表。每个消息包含`role`（system/user/assistant）和`content`（文本/图像/音频）。含义：定义对话上下文，模型据此生成响应。示例：`[{"role": "user", "content": "Hello!"}]`。支持多模态输入。 |
| model                | string       | 是      | 无          | 模型ID，如`gpt-4o`。含义：指定生成响应的模型。参考`/v1/models`获取可用模型列表。 |
| frequency_penalty    | number       | 否      | 0           | 频率惩罚（-2.0到2.0）。含义：减少重复token生成，提高输出多样性。 |
| logit_bias           | map          | 否      | 无          | token偏置映射。含义：调整特定token的生成概率（如禁止某些词）。 |
| logprobs             | boolean      | 否      | false       | 是否返回token对数概率。含义：用于分析模型置信度。 |
| max_completion_tokens| integer      | 否      | 无          | 最大完成token数（包括推理token）。含义：控制响应长度，防止过长输出。 |
| max_tokens           | integer      | 否      | 无          | 最大token数（已弃用）。含义：类似max_completion_tokens，用于旧模型。 |
| n                    | integer      | 否      | 1           | 生成选项数量。含义：返回多个备选响应，注意会增加token消耗。 |
| presence_penalty     | number       | 否      | 0           | 存在惩罚（-2.0到2.0）。含义：鼓励新主题，避免重复。 |
| response_format      | object       | 否      | 无          | 输出格式。含义：如`{"type": "json_schema"}`确保结构化JSON输出。 |
| seed                 | integer      | 否      | 无          | 随机种子。含义：确保响应确定性（重复请求返回相同结果）。 |
| stop                 | string/array | 否      | 无          | 停止序列。含义：生成到此停止（如"END"）。 |
| stream               | boolean      | 否      | false       | 是否流式响应。含义：实时返回chunk，便于交互式应用。 |
| temperature          | number       | 否      | 1           | 采样温度（0到2）。含义：控制随机性，高值更创意，低值更确定。 |
| tool_choice          | string/object| 否      | auto（若有工具）| 工具选择策略。含义：如`auto`让模型决定调用工具。 |
| tools                | array        | 否      | 无          | 可用工具列表。含义：启用函数调用或内置工具（如web search）。 |
| top_p                | number       | 否      | 1           | 核采样（0到1）。含义：控制多样性，与temperature互斥。 |
| user                 | string       | 否      | 无          | 用户标识。含义：用于监控和滥用检测。 |

* **其他字段**：如`metadata`（存储额外信息）、`modalities`（输出类型，如["text", "audio"]）等。参考官方文档获取完整列表。

### 响应字段（Response）

| 字段              | 类型     | 含义与说明 |
|-------------------|----------|------------|
| choices          | array   | 完成选项列表。含义：每个选项包含index、message（响应内容）和finish_reason（停止原因）。 |
| created          | integer | 创建时间戳。含义：Unix秒，表示响应生成时间。 |
| id               | string  | 响应ID。含义：唯一标识此次完成。 |
| model            | string  | 使用模型。含义：确认实际模型。 |
| object           | string  | 对象类型：`chat.completion`。含义：响应类型标识。 |
| service_tier     | string  | 服务层级。含义：如果指定，返回实际使用层级。 |
| system_fingerprint| string  | 系统指纹。含义：监控后端变化影响确定性。 |
| usage            | object  | 使用统计。含义：包含prompt_tokens、completion_tokens、total_tokens，用于计费。 |

* **流式响应**：返回chunk序列，每个chunk的object为`chat.completion.chunk`，包含delta（增量内容）。以`[DONE]`结束。

## 使用文档

### 基本流程
1. **构建请求**：准备messages数组，确保角色正确。
2. **发送请求**：使用HTTP POST，携带密钥。
3. **解析响应**：从choices中提取message.content。
4. **流式处理**：若stream=true，逐chunk读取delta.content。

### 示例（Curl，非流式）
```
curl https://api.modelverse.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "model": "{model_name}",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 示例（Python，流式）
```python
import openai

client = openai.OpenAI(api_key="{api_key}", base_url="https://api.modelverse.cn/v1/")
stream = client.chat.completions.create(
    model="{model_name}",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

更多示例和高级用法，请直接参考[OpenAI官方文档](https://platform.openai.com/docs/api-reference/chat/create)。