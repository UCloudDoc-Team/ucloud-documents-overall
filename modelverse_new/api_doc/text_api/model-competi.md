# 各模型支持的协议

本页用于说明不同模型在各协议下的兼容情况。  
约定：

- ✅：当前推荐、经过验证的主要调用方式。
- 空白：可以尝试，但未充分验证或可能不稳定或完全无法使用，使用前建议在测试环境验证，不保证其兼容性。

> 说明：实际兼容性可能会随官方协议演进而调整，请以官方最新文档和测试结果为准。

## 如何查看支持的模型列表

您可以通过 `/v1/models` 接口获取所有支持的模型：

```shell
curl https://api.modelverse.cn/v1/models \
  -H "Content-Type: application/json"
```

推荐使用 `Cherry Studio` 客户端，配置 API 地址后点击管理按钮即可直观查看所有支持的模型。详细配置教程请参考：[Cherry Studio 配置教程](https://docs.ucloud.cn/modelverse/best_practice/scenario/cherry-studio)。

## OpenAI / GPT 系列

| 模型 ID                   | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注                                                                 |
| ------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | -------------------------------------------------------------------- |
| gpt-5.1-chat              | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| gpt-5.1                   | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| gpt-5.1-codex-mini        |                                         | ✅                                   |                             |                              | 仅支持 /v1/responses 接口                                            |
| gpt-5.1-codex             |                                         | ✅                                   |                             |                              | 仅支持 /v1/responses 接口                                            |
| gpt-5                     | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| gpt-5-chat                | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| gpt-5-codex               |                                         | ✅                                   |                             |                              | 仅支持 /v1/responses 接口                                            |
| gpt-4o-mini               | ✅                                       |                                     |                             |                              |                                                                      |
| gpt-4.1-nano              | ✅                                       |                                     |                             |                              |                                                                      |
| gpt-4.1-mini              | ✅                                       |                                     |                             |                              |                                                                      |
| o1                        | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| openai/gpt-5.1-chat       | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| openai/gpt-5.1-codex      |                                         | ✅                                   |                             |                              | 仅支持 /v1/responses 接口                                            |
| openai/gpt-5.1-codex-mini |                                         | ✅                                   |                             |                              | 仅支持 /v1/responses 接口                                            |
| openai/gpt-5.1            | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| openai/gpt-4o             | ✅                                       | ✅                                   |                             |                              |                                                                      |
| openai/gpt-5-nano         | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| openai/gpt-4.1            | ✅                                       | ✅                                   |                             |                              |                                                                      |
| openai/gpt-5              | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| openai/gpt-5-mini         | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |
| openai/gpt-oss-20b        | ✅                                       |                                     |                             |                              |                                                                      |
| openai/gpt-oss-120b       | ✅                                       |                                     |                             |                              |                                                                      |
| o4-mini-deep-research     |                                         | ✅                                   |                             |                              | 仅支持 /v1/responses 接口                                            |
| o4-mini                   | ✅                                       | ✅                                   |                             |                              | 不支持 max_tokens 参数，请使用max_completion_tokens，图像需用 base64 |

## Claude 系列

| 模型 ID                             | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注                                                           |
| ----------------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | -------------------------------------------------------------- |
| claude-opus-4-1-20250805            | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-sonnet-4-5-20250929-thinking | ✅                                       |                                     |                             | ✅                            | temperature 和 top_p 只能指定一个，temperature 取值范围为[0,1) |
| claude-sonnet-4-5-20250929          | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-sonnet-3.7                   | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-opus-4.1-thinking            | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-opus-4.0-thinking            | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-sonnet-4.0-thinking          | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-sonnet-3.5                   | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-4-opus                       | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-4-sonnet                     | ✅                                       |                                     |                             | ✅                            |                                                                |
| claude-sonnet-4.5-thinking          | ✅                                       |                                     |                             | ✅                            | temperature 和 top_p 只能指定一个，temperature 取值范围为[0,1) |
| claude-sonnet-4.5                   | ✅                                       |                                     |                             | ✅                            | temperature 和 top_p 只能指定一个，temperature 取值范围为[0,1) |

> **参数限制说明**：Claude Sonnet 4.5 仅支持指定 `temperature` 或 `top_p` 参数中的一个，不能同时使用这两个参数。详见 [官方文档说明](https://docs.aws.amazon.com/zh_cn/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-request-response.html)。

## Grok 系列

| 模型 ID                     | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注 |
| --------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---- |
| grok-4-1-fast-reasoning     | ✅                                       |                                     |                             |                              |      |
| grok-4-1-fast-non-reasoning | ✅                                       |                                     |                             |                              |      |
| grok-4-fast-reasoning       | ✅                                       |                                     |                             |                              |      |
| grok-4-fast                 | ✅                                       |                                     |                             |                              |      |
| grok-4                      | ✅                                       |                                     |                             |                              |      |

## Qwen 系列

| 模型 ID                            | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注 |
| ---------------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---- |
| Qwen/Qwen3-vl-Plus                 | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-235B-A22B-Thinking-2507 | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen-Plus-Thinking            | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen-Plus                     | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-Max                     | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-VL-235B-A22B-Instruct   | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-VL-235B-A22B-Thinking   | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-32B                     | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-30B-A3B                 | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-Coder                   | ✅                                       |                                     |                             |                              |      |
| Qwen/Qwen3-235B-A22B               | ✅                                       |                                     |                             |                              |      |
| Qwen/QwQ-32B                       | ✅                                       |                                     |                             |                              |      |
| qwen/qwen2.5-vl-72b-instruct       | ✅                                       |                                     |                             |                              |      |

## Gemini 系列（支持 `/v1beta/models`）

| 模型 ID              | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注                         |
| -------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---------------------------- |
| gemini-3-pro-preview |                                         |                                     | ✅                           |                              | 推荐使用 /v1beta/models 接口 |
| gemini-2.5-pro       |                                         |                                     | ✅                           |                              | 推荐使用 /v1beta/models 接口 |
| gemini-2.5-flash     |                                         |                                     | ✅                           |                              | 推荐使用 /v1beta/models 接口 |

> **思考过程配置**：使用 Gemini 协议的 `v1beta/models` 接口，可通过 `thinkingConfig` 参数开启/关闭思考过程。详见 [Gemini 协议兼容](https://docs.ucloud.cn/modelverse/api_doc/text_api/gemini_compatible)
> 
> **安全等级配置**：Gemini 支持通过 `safetySettings` 配置内容过滤策略，包括仇恨言论、色情内容、危险内容、骚扰内容和公民诚信五个类别。详见 [Google 官方安全设置文档](https://ai.google.dev/gemini-api/docs/safety-settings?hl=zh-cn)

## DeepSeek 系列

| 模型 ID                                   | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注 |
| ----------------------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---- |
| deepseek-ai/DeepSeek-OCR                  | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-V3.1-Think           | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-V3.2-Exp-Think       | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-V3.2-Exp             | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-V3.1-Terminus        | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-V3.1                 | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-R1-Distill-Llama-70B | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-R1-0528              | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-V3-0324              | ✅                                       |                                     |                             |                              |      |
| deepseek-ai/DeepSeek-R1                   | ✅                                       |                                     |                             |                              |      |

## Doubao（豆包）系列

| 模型 ID                                  | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注 |
| ---------------------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---- |
| ByteDance/doubao-1-5-pro-32k-250115      | ✅                                       |                                     |                             |                              |      |
| ByteDance/doubao-1-5-pro-256k-250115     | ✅                                       |                                     |                             |                              |      |
| ByteDance/doubao-seed-1.6                | ✅                                       |                                     |                             |                              |      |
| ByteDance/doubao-seed-1.6-thinking       | ✅                                       |                                     |                             |                              |      |
| ByteDance/doubao-1.5-thinking-vision-pro | ✅                                       |                                     |                             |                              |      |

## Baidu 系列

| 模型 ID                      | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注 |
| ---------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---- |
| baidu/ernie-x1-turbo-32k     | ✅                                       |                                     |                             |                              |      |
| baidu/ernie-4.5-turbo-128k   | ✅                                       |                                     |                             |                              |      |
| baidu/ernie-4.5-turbo-vl-32k | ✅                                       |                                     |                             |                              |      |

## 其他模型

| 模型 ID                          | `OpenAI Chat 协议 /v1/chat/completions` | `OpenAI Response 协议/v1/responses` | `Gemini协议 /v1beta/models` | `Anthropic协议 /v1/messages` | 备注 |
| -------------------------------- | --------------------------------------- | ----------------------------------- | --------------------------- | ---------------------------- | ---- |
| moonshotai/Kimi-K2-Thinking      | ✅                                       |                                     |                             |                              |      |
| moonshotai/Kimi-K2-Instruct-0905 | ✅                                       |                                     |                             |                              |      |
| moonshotai/Kimi-K2-Instruct      | ✅                                       |                                     |                             |                              |      |
| zai-org/glm-4.6                  | ✅                                       |                                     |                             |                              |      |
| zai-org/glm-4.5v                 | ✅                                       |                                     |                             |                              |      |
| zai-org/glm-4.5                  | ✅                                       |                                     |                             |                              |      |
| kat-coder-256k                   | ✅                                       |                                     |                             |                              |      |

