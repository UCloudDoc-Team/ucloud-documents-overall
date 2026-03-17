# gemini-3-pro-image ( nano banana 2 )

本文介绍 `gemini-3-pro-image-preview` (模型ID: `gemini-3-pro-image-preview`) 模型调用 API 的输入输出参数，供您使用接口时查阅字段含义。

---

以下只展示部分使用到的字段说明，详细说明请参考官方文档 [Gemini 3 Pro 图片功能的新变化](https://ai.google.dev/gemini-api/docs/image-generation?hl=zh-cn#gemini-3-capabilities)

## 请求参数

### 请求体

| 字段名                                   | 类型   | 是否必须 | 默认值            | 描述                                                                                       |
| ---------------------------------------- | ------ | -------- | ----------------- | ------------------------------------------------------------------------------------------ |
| contents                                 | array  | 必须     | -                 | 请求的内容，包含一个或多个部分。                                                           |
| contents.role                            | string | 必须     | "user"            | 内容的角色，此处固定为 "user"。                                                            |
| contents.parts                           | array  | 必须     | -                 | 内容的具体部分。                                                                           |
| contents.parts.text                      | string | 可选     | -                 | 提示词文本。                                                                               |
| generationConfig                         | object | 可选     | -                 | 生成配置。                                                                                 |
| generationConfig.responseModalities      | array  | 可选     | ["TEXT", "IMAGE"] | 期望的响应形式，可以是文本或图像。                                                         |
| generationConfig.imageConfig             | object | 可选     | -                 | 图片生成配置。                                                                             |
| generationConfig.imageConfig.aspectRatio | string | 可选     | "1:1"             | 图片宽高比。支持 "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"。 |
| generationConfig.imageConfig.imageSize   | string | 可选     | "1K"              | 图片分辨率。支持 "1K", "2K", "4K"。                                                        |

## 响应参数

| 字段名                                       | 类型     | 描述                                     |
| -------------------------------------------- | -------- | ---------------------------------------- |
| candidates                                   | `array`  | 返回的候选内容列表。                     |
| candidates.content                           | `object` | 候选内容。                               |
| candidates.content.parts                     | `array`  | 内容的具体部分，可能包含文本和图像数据。 |
| candidates.content.parts.text                | `string` | 模型返回的文本描述。                     |
| candidates.content.parts.inlineData          | `object` | 内联的图像数据。                         |
| candidates.content.parts.inlineData.data     | `string` | Base64 编码的图像数据。                  |
| candidates.content.parts.inlineData.mimeType | `string` | 数据的 MIME 类型，例如 "image/png"。     |
| candidates.finishReason                      | `string` | 生成结束的原因，例如 "STOP"。            |
| usageMetadata                                | `object` | token 使用情况的元数据。                 |
| error                                        | `Object` | 错误信息对象                             |

## 示例

### Gemini 兼容接口

`POST https://api.modelverse.cn/v1beta/models/gemini-3-pro-image-preview:generateContent`

#### 图片生成（文本转图片）

> ⚠️ 注意：您必须在配置中添加 responseModalities: ["TEXT", "IMAGE"]。

<!-- tabs:start -->

##### ** curl **

```bash
curl -s -X POST \
  "https://api.modelverse.cn/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $MODELVERSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English."}]}],
    "tools": [{"google_search": {}}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {"aspectRatio": "1:1", "imageSize": "1K"}
    }
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | head -1 | base64 --decode > butterfly.png
```

##### ** python **

```python
from google import genai
from google.genai import types
import os

client = genai.Client(
    api_key=os.getenv("MODELVERSE_API_KEY", "<MODELVERSE_API_KEY>"),  # 您的API_KEY
    http_options=types.HttpOptions(
        base_url="https://api.modelverse.cn"
    ),
)

prompt = "Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English."
aspect_ratio = "1:1"  # "1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"
resolution = "1K"  # "1K", "2K", "4K"

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio, image_size=resolution
        ),
    ),
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image := part.as_image():
        image.save("butterfly.png")

```

<!-- tabs:end -->

### 响应示例

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Here is the anatomical sketch of a dissected Monarch butterfly in Da Vinci style..."
          },
          {
            "inlineData": {
              "data": "iVBORw0KGgoAAAANSUhEUgAA...",
              "mimeType": "image/png"
            }
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "candidatesTokenCount": 1315,
    "totalTokenCount": 1331
  }
}
```


```json
{
  "error": {
    "message": "error_message",
    "type": "error_type",
    "param": "request_id",
    "code": "error_code"
  }
}
```