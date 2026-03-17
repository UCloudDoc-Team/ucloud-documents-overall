# OpenAI TTS API 调用文档

UModelverse 平台提供了与 OpenAI TTS（Text-to-Speech）API 完全兼容的语音合成接口。开发者可以使用熟悉的 OpenAI SDK 或标准 HTTP 客户端，无缝调用 Modelverse 上部署的高质量 TTS 模型。

> **🎉 限时免费**：TTS 语音合成服务现正限时免费开放，欢迎体验！

## 快速开始

您可以使用 `curl` 命令或任何支持 OpenAI API 的客户端库来调用 Modelverse TTS API。平台支持多种高质量语音合成模型，如 `IndexTeam/IndexTTS-2` 等。

## 请求参数

| 参数  | 类型   | 必填 | 说明                                                                                                                                |
| ----- | ------ | ---- | ----------------------------------------------------------------------------------------------------------------------------------- |
| model | string | 是   | 要使用的 TTS 模型名称，例如：`IndexTeam/IndexTTS-2`                                                                                 |
| input | string | 是   | 要转换为语音的文本内容（最大支持 600 字符）                                                                                         |
| voice | string | 是   | 使用的音色，可选值包括：内置音色（`jack_cheng`, `sales_voice`, `crystla_liu`, `stephen_chow`, `xiaoyueyue`, `mkas`, `entertain`, `novel`, `movie`），也可以填写自定义音色 ID（形如 `uspeech:xxxx`，详见下文「使用自定义音色」） |

## 调用示例

以下示例展示如何使用 `IndexTeam/IndexTTS-2` 模型进行语音合成。请确保将 `$MODELVERSE_API_KEY` 替换为您自己的 API Key。

 <!-- tabs:start -->

#### ** curl **
```bash
curl https://api.modelverse.cn/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -d '{
    "model": "IndexTeam/IndexTTS-2",
    "input": "你好！欢迎使用 Modelverse 语音合成服务。",
    "voice": "jack_cheng"
  }' \
  --output speech.wav
```
    
#### ** python **
```python
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY", "<YOUR_MODELVERSE_API_KEY>"),
    base_url="https://api.modelverse.cn/v1/",
)

speech_file_path = Path(__file__).parent / "generated-speech.wav"

with client.audio.speech.with_streaming_response.create(
    model="IndexTeam/IndexTTS-2",
    voice="jack_cheng",
    input="你好！欢迎使用 Modelverse 语音合成服务。",
) as response:
    response.stream_to_file(speech_file_path)

print(f"Audio saved to {speech_file_path}")
```

<!-- tabs:end -->

## 使用自定义音色（可选）

除了使用内置的 `voice` 名称外，您还可以上传自己的音色（甚至带有特定情绪的样例语音），生成一个专属的 `voice_id`，在 TTS 请求中通过 `voice` 字段进行引用。

> 注意：当前自定义音色资源会在上传 **7 天** 后自动清理，如需长期使用请注意提前备份或重新上传。（可联系商务团队咨询长期保存需求）

使用方式可以简单理解为 **三步**：

1. **上传音色，获取 `voice_id`**  
   调用 `POST /v1/audio/voice/upload` 上传一段符合要求的示例语音，接口会返回一个 `id` 作为自定义音色 ID。  
   详细的请求参数与返回结构请参考《[自定义音色管理 API 文档](/api_doc/audio_api/custom_voice_api)》。
2. **在 TTS 请求中使用 `voice_id`**  
   在 `/v1/audio/speech` 请求中，把 `voice` 字段设置为步骤一返回的 `id`，下文会给出完整示例。
3. **管理已有的自定义音色（可选）**  
   如需查看或删除已有音色，可调用 `GET /v1/audio/voice/list` 和 `POST /v1/audio/voice/delete`。  
   具体请求/返回格式同样见《[自定义音色管理 API 文档](/api_doc/audio_api/custom_voice_api)》。

> 提示：自定义音色完全兼容 OpenAI 协议，只是复用了 `voice` 这个字段，不需要学习新的参数名。

### 在 TTS 请求中使用自定义 voice_id

当您已经拿到一个自定义音色 `id`（例如 `uspeech:xxxx`）后，只需要在 `/v1/audio/speech` 请求中把 `voice` 字段改成该 `id` 即可。

```bash
VOICE_ID="uspeech:xxxx-xxxx-xxxx-xxxx"

curl https://api.modelverse.cn/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -d "{
    \"model\": \"IndexTeam/IndexTTS-2\",\
    \"input\": \"你好，我是自定义的温柔女声。\",\
    \"voice\": \"$VOICE_ID\"\
  }" \
  --output speech-custom.wav
```

行为说明：

- `voice` 为空：使用默认音色或模型自带的默认配置。
- `voice` 为内置名称（如 `jack_cheng` 等）：使用平台内置的预置音色。
- `voice` 为形如 `uspeech:xxxx` 的值：表示使用你上传的自定义音色，平台会根据该 ID 查找并应用对应的音色/情绪素材，无需额外配置。

  ## 响应格式

API 返回二进制音频文件流。

- **音频格式**：目前仅支持 **WAV** 格式输出
- **Content-Type**：`audio/wav`

## 注意事项

1. **限时免费**：当前 TTS 服务限时免费开放，正式计费标准后续将另行通知
2. **音频格式**：响应的二进制流格式目前仅支持 WAV，暂不支持其他音频格式
3. **文本长度限制**：单次请求的文本长度限制因具体模型而异，`IndexTeam/IndexTTS-2` 模型通常支持 600 字符以内的文本
4. **语音类型**：不同的 `voice` 参数会产生不同音色和风格的语音效果，建议根据实际场景选择合适的语音类型

## 错误处理

当请求失败时，API 会返回标准的 JSON 格式错误响应：

```json
{
  "error": {
    "message": "错误描述信息",
    "type": "invalid_request_error",
    "code": "error_code",
    "param": "<请求 ID，用于反馈或排查错误原因>"
  }
}
```

### 常见问题（FAQ）

- **Q：我上传的音频有什么要求？**  
  A：必须是 MP3/WAV，单个文件 ≤ 20MB，时长 5–30 秒，采样率至少 16kHz，不符合要求会返回 4xx 错误，并在 `error.code` 中标明原因。

- **Q：`voice` 字段应该填什么？**  
  A：
  - 想直接用平台提供的固定音色：填写内置名称（如 `jack_cheng`）；
  - 想用自己录制的音色：先调用上传接口拿到 `id`，然后在 TTS 请求中把 `voice` 设置为这个 `id`（例如 `uspeech:xxxx`）。

- **Q：出现 `invalid_voice_id` / `voice_not_found` 等错误怎么办？**  
  A：说明当前账号下找不到这个 `voice_id`，或者已被删除。可以先调用 `/v1/audio/voice/list` 确认当前可用的 ID，再在请求里使用正确的值。

- **Q：不同账号之间能共享自定义音色吗？**  
  A：同一组织下所有子账号，自定义音色可以共享。非同一账号下，无法共享。