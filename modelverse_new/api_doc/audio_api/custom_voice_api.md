# 自定义音色管理 API 文档

> 本文仅描述自定义音色相关管理接口（上传 / 列表 / 删除）的 **请求与响应格式**，适合已有开发基础的用户参考。如何在 `/v1/audio/speech` 中实际使用自定义音色，请查看《[OpenAI TTS API 调用文档](/api_doc/audio_api/ttts)》中的「使用自定义音色（可选）」一节。

## 概述

- 域名示例：`https://api.modelverse.cn`
- 认证方式：所有接口都需要在 Header 中携带 `Authorization: Bearer <MODELVERSE_API_KEY>`。
- 组织隔离：
  - 自定义音色按组织维度隔离；同一组织下所有子账号可以共享该组织内的自定义音色；
  - 不同组织之间无法共享。
- 生命周期：自定义音色默认保存 **7 天**，超期会被后台任务清理；如有长期保存需求，可联系商务团队评估方案。

---

## 1. 上传自定义音色

- **HTTP 方法**：`POST`
- **路径**：`/v1/audio/voice/upload`
- **Content-Type**：
  - 推荐：`multipart/form-data`（直接上传文件）
  - 也支持：表单字段传 Base64 字符串或远程 URL

### 1.1 请求参数

#### 公共字段

| 字段 | 类型   | 必填 | 说明 |
| ---- | ------ | ---- | ---- |
| name | string | 是   | 音色名称，用于列表展示，例如「温柔女声」「客服音色A」。 |
| model | string | 是   | 使用该音色时对应的 TTS 模型名称，例如 `IndexTeam/IndexTTS-2`。与后续 `/v1/audio/speech` 请求中的 `model` 保持一致。 |

#### Speaker（音色语料音频，三选一，必填其一）

| 字段                 | 类型  | 必填              | 说明 |
| -------------------- | ----- | ----------------- | ---- |
| speaker_file         | file  | 是（三选一必填） | 本地音频文件（推荐方式），通过 `multipart/form-data` 上传。 |
| speaker_file_base64  | string| 是（三选一必填） | `speaker_file` 的 Base64 字符串，通过普通表单字段传递。 |
| speaker_url          | string| 是（三选一必填） | 可访问的公网 URL，指向音色音频文件。 |

> 说明：
> - `speaker_*` 三个字段 **三选一，至少提供其一**；
> - 若同时提供多个，优先级为：`speaker_file` → `speaker_file_base64` → `speaker_url`；
> - 若三者均未提供，请求会被拒绝（错误码：`missing_speaker`）。

#### Emotion（情绪样例音频，三选一，可选）

| 字段                  | 类型  | 必填              | 说明 |
| --------------------- | ----- | ----------------- | ---- |
| emotion_file          | file  | 否（三选一可选） | 情绪样例音频文件，通过 `multipart/form-data` 上传。 |
| emotion_file_base64   | string| 否（三选一可选） | `emotion_file` 的 Base64 字符串，通过普通表单字段传递。 |
| emotion_url           | string| 否（三选一可选） | 可访问的公网 URL，指向情绪样例音频文件。 |

> 说明：
> - `emotion_*` 字段整体可选，可不提供；
> - 若同时提供多个，优先级为：`emotion_file` → `emotion_file_base64` → `emotion_url`；
> - 若完全不传 `emotion_*`，则只基于 Speaker 构建音色特征。

### 1.2 音频文件约束

对 `speaker_*` 与 `emotion_*` 上传的音频均适用以下约束：

- **格式**：仅支持 `MP3`、`WAV`
- **大小**：单个音频 ≤ `20MB`
- **时长**：`5–30` 秒
- **采样率**：`16kHz` 及以上

若不满足上述任一条件，接口会返回 4xx 错误，并在 `error.code` 中标明具体原因（如 `file_too_large`、`duration_out_of_range`、`sample_rate_too_low` 等）。

### 1.3 请求示例（推荐：multipart 文件上传）

```bash
curl -X POST "https://api.modelverse.cn/v1/audio/voice/upload" \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "name=温柔女声" \
  -F "model=IndexTeam/IndexTTS-2" \
  -F "speaker_file=@/path/to/speaker.wav" \
  -F "emotion_file=@/path/to/emotion.wav"
```

### 1.4 成功响应示例

```json
{
  "id": "uspeech:xxxx-xxxx-xxxx-xxxx"
}
```

- `id`：自定义音色 ID，后续在 `/v1/audio/speech` 请求中通过 `voice` 字段引用（例如：`"voice": "uspeech:xxxx-xxxx-xxxx-xxxx"`）。

### 1.5 失败响应示例

所有错误响应都会采用统一格式：

```json
{
  "error": {
    "message": "错误描述信息",
    "type": "invalid_request_error",
    "code": "missing_speaker",
    "param": "<请求 ID 或参数名>"
  }
}
```

常见错误码示例：

- `missing_name`：未提供 `name` 字段；
- `missing_speaker`：未提供任意一个 `speaker_*` 字段；
- `invalid_speaker_base64`：`speaker_file_base64` 解码失败；
- `unsupported_audio_format`：音频格式不是 MP3/WAV；
- `file_too_large` / `duration_out_of_range` / `sample_rate_too_low`：音频不符合大小、时长或采样率限制。

---

## 2. 查询自定义音色列表

- **HTTP 方法**：`GET`
- **路径**：`/v1/audio/voice/list`

### 2.1 请求说明

- 无请求体，仅需在 Header 中携带鉴权信息。
- 系统会根据当前 API Key 所属组织（`top_org_id`）返回该组织下的自定义音色列表。
- 为保证接口性能，单次调用最多返回 `1000` 条记录。

### 2.2 响应示例

```json
{
  "list": [
    { "id": "uspeech:xxxx", "name": "温柔女声" },
    { "id": "uspeech:yyyy", "name": "沉稳男声" }
  ]
}
```

字段说明：

| 字段 | 类型   | 说明 |
| ---- | ------ | ---- |
| list | array  | 自定义音色列表。 |
| list[].id   | string | 自定义音色 ID，可在 `/v1/audio/speech` 的 `voice` 字段中引用。 |
| list[].name | string | 创建时填写的音色名称，仅用于展示。 |

---

## 3. 删除自定义音色

- **HTTP 方法**：`POST`
- **路径**：`/v1/audio/voice/delete`
- **Content-Type**：`application/json`

### 3.1 请求参数

| 字段 | 类型   | 必填 | 说明 |
| ---- | ------ | ---- | ---- |
| id   | string | 是   | 要删除的自定义音色 ID，即上传接口返回的 `id`。 |

### 3.2 请求示例

```bash
curl -X POST "https://api.modelverse.cn/v1/audio/voice/delete" \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "uspeech:xxxx"
  }'
```

### 3.3 成功响应示例

```json
{
  "success": true
}
```

> 说明：删除成功后，该 `voice_id` 将无法继续在 `/v1/audio/speech` 请求中使用，请在确认业务不再引用后再删除。

### 3.4 可能的错误码

- `missing_id`：请求体中未提供 `id` 字段；
- `invalid_voice_id`：指定的 `id` 在当前组织下不存在或已被删除；
- 其他 `server_error`：内部错误或对象存储异常，可结合返回的 `message` 与请求 ID 排查。

---

通过以上三个接口，可以完成自定义音色的完整生命周期管理：

1. 通过上传接口创建音色并获取 `voice_id`；
2. 在 TTS 调用中通过 `voice` 字段引用该 `voice_id`；
3. 通过列表/删除接口管理已有音色资源，并结合 7 天有效期策略控制存储成本。
