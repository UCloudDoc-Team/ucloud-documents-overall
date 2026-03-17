# 概览

模型服务平台 UModelVerse 旨在为客户提供快速搭建 AGI 应用的能力。我们强大的 API 让您无需关注底层算力调度、模型部署等复杂工作。仅需一个 API Key，即可轻松接入 OpenAI、Gemini 兼容的 API 接口，快速构建您的专属 AGI 应用。

## 产品简介

- [什么是模型服务平台](/introduction/introduction)
- [产品优势](/introduction/advantages)

## 计费说明

- [计费说明](/price)

## API 调用

- [快速开始](/api_doc/quick-start)
- 通用说明
  - [认证鉴权](/api_doc/common/certificate)
  - [错误码](/api_doc/common/error-code)
- 文本生成
  - [如何获取模型列表](/api_doc/text_api/models)
  - [API支持与UCloud扩展字段说明](/api_doc/text_api/api-expand)
  - [OpenAI Chat Completions 说明](/api_doc/text_api/openai_compatible)
  - [OpenAI Response API 说明](/api_doc/text_api/response_api)
  - [Embeddings 向量嵌入](/api_doc/text_api/embeddings)
  - [DeepSeek-OCR 模型调用示例](/api_doc/text_api/deepseek-ocr)
  - [Doubao 豆包模型思考开关](/api_doc/text_api/thinking/doubao)
  - [Gemini 快速开始](/api_doc/text_api/gemini_compatible)
  - [Claude (Anthropic) 兼容说明](/api_doc/text_api/claude_compatible)
- 图片生成
  - [gemini-2.5-flash-image ( Nano Banana )](/api_doc/image_api/gemini-2.5-flash-image)
  - [gemini-3-pro-image ( Nano Banana 2 )](/api_doc/image_api/gemini-3-pro-image)
  - [flux-2-pro](/api_doc/image_api/flux-2-pro)
  - [flux-kontext-pro](/api_doc/image_api/flux-kontext-pro)
  - [flux-pro-1.1](/api_doc/image_api/flux-pro-1.1)
  - [black-forest-labs/flux.1-dev](/api_doc/image_api/black-forest-labs-flux.1-dev)
  - [black-forest-labs/flux-kontext-pro](/api_doc/image_api/black-forest-labs-flux-kontext-pro)
  - [black-forest-labs/flux-kontext-pro/multi](/api_doc/image_api/black-forest-labs-flux-kontext-pro-multi)
  - [black-forest-labs/flux-kontext-pro/text-to-image](/api_doc/image_api/black-forest-labs-flux-kontext-pro-text-to-image)
  - [stepfun-ai/step1x-edit](/api_doc/image_api/stepfun-ai-step1x-edit)
  - [black-forest-labs/flux-kontext-max](/api_doc/image_api/black-forest-labs-flux-kontext-max)
  - [black-forest-labs/flux-kontext-max/multi](/api_doc/image_api/black-forest-labs-flux-kontext-max-multi)
  - [black-forest-labs/flux-kontext-max/text-to-image](/api_doc/image_api/black-forest-labs-flux-kontext-max-text-to-image)
  - [Qwen/Qwen-Image-Edit](/api_doc/image_api/Qwen-Qwen-Image-Edit)
  - [Qwen/Qwen-Image](/api_doc/image_api/Qwen-Qwen-Image)
  - [gpt-image-1](/api_doc/image_api/gpt-image-1)
  - [gpt-image-1.5](/api_doc/image_api/gpt-image-1.5)
  - [doubao-seedream-4.5](/api_doc/image_api/doubao-seedream-4.5)
- 视频生成
  - [OpenAI/Sora2-T2V](/api_doc/video_api/OpenAI-Sora2-T2V)
  - [OpenAI/Sora2-T2V-Pro](/api_doc/video_api/OpenAI-Sora2-T2V-Pro)
  - [OpenAI/Sora2-I2V](/api_doc/video_api/OpenAI-Sora2-I2V)
  - [OpenAI/Sora2-I2V-Pro](/api_doc/video_api/OpenAI-Sora2-I2V-Pro)
  - [Wan-AI/Wan2.2-I2V](/api_doc/video_api/Wan-AI-Wan2.2-I2V)
  - [Wan-AI/Wan2.2-T2V](/api_doc/video_api/Wan-AI-Wan2.2-T2V)
  - [Wan-AI/Wan2.5-I2V](/api_doc/video_api/Wan-AI-Wan2.5-I2V)
  - [Wan-AI/Wan2.5-T2V](/api_doc/video_api/Wan-AI-Wan2.5-T2V)
  - [Wan-AI/Wan2.6-I2V](/api_doc/video_api/Wan-AI-Wan2.6-I2V)
  - [Wan-AI/Wan2.6-T2V](/api_doc/video_api/Wan-AI-Wan2.6-T2V)
  - [MiniMax/Hailuo-2.3-I2V](/api_doc/video_api/MiniMax-Hailuo-2.3-I2V)
  - [MiniMax/Hailuo-2.3-T2V](/api_doc/video_api/MiniMax-Hailuo-2.3-T2V)
  - [Vidu/文生视频](/api_doc/video_api/vidu/Vidu-Text2Video)
  - [Vidu/图生视频](/api_doc/video_api/vidu/Vidu-Img2Video)
  - [Vidu/参考图生视频](/api_doc/video_api/vidu/Vidu-Reference2Video)
  - [Vidu/首尾帧生视频](/api_doc/video_api/vidu/Vidu-StartEnd2Video)
  - [Vidu/视频延长](/api_doc/video_api/vidu/Vidu-Extend)
  - [Vidu/对口型](/api_doc/video_api/vidu/Vidu-LipSync)
  - [doubao-seedance-1-5-pro](/api_doc/video_api/doubao-seedance-1-5-pro-251215)
  - [kling-video-o1](/api_doc/video_api/Kling-O1)
  - [kling-v2-6/图生视频](/api_doc/video_api/Kling-v2.6-I2V)
  - [kling-v2-6/文生视频](/api_doc/video_api/Kling-v2.6-T2V)
  - [Veo-3.1/文图生视频](/api_doc/video_api/Veo-3.1)
- 音频生成
  - [OpenAI TTS 兼容](/api_doc/audio_api/ttts)
  - [自定义音色](/api_doc/audio_api/custom_voice_api)
  - [IndexTeam/IndexTTS 扩展参数](/api_doc/audio_api/IndexTeam-IndexTTS-extend)

## 最佳实践

- [Claude Code 接入指南](/best_practice/claudecode)
- [OpenAI Codex 接入指南](/best_practice/codex)
- [ComfyUI插件接入](/best_practice/comfyui)
- 常见客户端接入 API
  - [Chatbox](/best_practice/scenario/chatbox)
  - [Open WebUI](/best_practice/scenario/open-webui)
  - [Dify](/best_practice/scenario/dify)
  - [Cherry-Studio](/best_practice/scenario/cherry-studio)
- MCP 说明
  - [MCP 简介](/best_practice/mcp/mcpgeneral)
  - [通过 CLINE 接入 MCP 服务](/best_practice/mcp/MCPServer)
  - [通过 UCloud API 实现 MCP Client](/best_practice/mcp/MCPClient)

## UModelVerse 协议

- [UModelVerse 隐私政策](/private)
