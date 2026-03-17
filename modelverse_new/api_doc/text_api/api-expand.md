# ModelVerse OpenAPI

当前文档为 ModelVerse 支持的 API 列表，以及自定义扩展字段说明。

## 支持的协议入口

| 协议/接口 | 说明 | 示例路径 |
| --- | --- | --- |
| OpenAI Chat Completions | 文本对话/流式输出 | `POST /v1/chat/completions` |
| OpenAI Responses | 多段输出与工具调用 | `POST /v1/responses` |
| OpenAI Images | 图片生成、编辑 | `POST /v1/images/generations`, `/v1/images/edits` |
| OpenAI Audio | 文本转语音 | `POST /v1/audio/speech` |
| 模型列举 (OpenAI/Gemini) | 返回可用模型列表 | `GET /v1/models`, `GET /v1beta/models` |
| Anthropic Messages | Claude 协议对话 | `POST /v1/messages` |
| Google Gemini | `/v1beta/models/{model}:{action}` 样式的内容生成 | `POST /v1beta/models/*` |
| 异步任务 | 视频/长时任务提交与查询 | `POST /v1/tasks/submit`, `GET /v1/tasks/status` |

## 自定义扩展字段

在兼容官方 OpenAI/Gemini 协议的基础上，我们额外提供了少量可选字段，只有走 ModelVerse OpenAPI 时才会被识别；第三方直接调用 OpenAI 官方服务时无需填写。

| 字段 | 适用接口 | 说明 | 使用方式 |
| --- | --- | --- | --- |
| `web_search` | `POST /v1/chat/completions` | 控制是否启用联网搜索能力，并选择搜索供应商。默认关闭。支持的 `vendor`：`tencent_sougo`（腾讯搜狗，默认）、`bocha`（博查 API）、`bing`。 | 在请求 JSON 根节点加入<br/>```json<br/>"web_search": {<br/>  "enable": true,<br/>  "vendor": "tencent_sougo"<br/>}``` |
| `thinking_enabled` | `POST /v1/chat/completions` | 内部的「思考模式」开关，影响模型侧推理策略。默认关闭。 | 与 OpenAI 请求一同提交：<br/>`"thinking_enabled": true` |