# gemini-2.5-flash-image( nano banana )

本文介绍 `gemini-2.5-flash-image` 模型调用 API 的输入输出参数，供您使用接口时查阅字段含义。

---

以下只展示部分使用到的字段说明，Gemini API 详细字段见[Gemini 官网文档](https://ai.google.dev/gemini-api/docs/image-generation?hl=zh-cn)

## 请求参数

### 请求体

| 字段名                              | 类型   | 是否必须 | 默认值            | 描述                               |
| ----------------------------------- | ------ | -------- | ----------------- | ---------------------------------- |
| contents                            | array  | 必须     | -                 | 请求的内容，包含一个或多个部分。   |
| contents.role                       | string | 必须     | "user"            | 内容的角色，此处固定为 "user"。    |
| contents.parts                      | array  | 必须     | -                 | 内容的具体部分。                   |
| contents.parts.text                 | string | 可选     | -                 | 提示词文本。                       |
| contents.parts.inlineData           | object | 可选     | -                 | 内联数据（如图像）。 |
| contents.parts.inlineData.mimeType  | string | 可选     | -                 | 数据的 MIME 类型。 |
| contents.parts.inlineData.data      | string | 可选     | -                 | Base64 编码的数据。                |
| contents.parts.fileData             | object | 可选     | -                 | 文件数据，支持 snake_case: file_data。 |
| contents.parts.fileData.mimeType    | string | 可选     | -                 | 文件的 MIME 类型。 |
| contents.parts.fileData.fileUri     | string | 可选     | -                 | 文件的 URI。 |
| generationConfig                    | object | 可选     | -                 | 生成配置。                         |
| generationConfig.responseModalities | array  | 可选     | ["TEXT", "IMAGE"] | 期望的响应形式，可以是文本或图像。 |

## 响应参数

| 字段名                                       | 类型      | 描述                                     |
| -------------------------------------------- | --------- | ---------------------------------------- |
| candidates                                   | `array`   | 返回的候选内容列表。                     |
| candidates.content                           | `object`  | 候选内容。                               |
| candidates.content.parts                     | `array`   | 内容的具体部分，可能包含文本和图像数据。 |
| candidates.content.parts.text                | `string`  | 模型返回的文本描述。                     |
| candidates.content.parts.inlineData          | `object`  | 内联的图像数据。                         |
| candidates.content.parts.inlineData.data     | `string`  | Base64 编码的图像数据。                  |
| candidates.content.parts.inlineData.mimeType | `string`  | 数据的 MIME 类型，例如 "image/png"。     |
| candidates.content.role                      | `string`  | 内容的角色，此处为 "model"。             |
| candidates.finishReason                      | `string`  | 生成结束的原因，例如 "STOP"。            |
| usageMetadata                                | `object`  | token 使用情况的元数据。                 |
| usageMetadata.candidatesTokenCount           | `integer` | 候选内容消耗的 token 数。                |
| usageMetadata.promptTokenCount               | `integer` | 提示词消耗的 token 数。                  |
| usageMetadata.totalTokenCount                | `integer` | 总共消耗的 token 数。                    |
| error                                        | `Object`  | 错误信息对象                             |
| error.code                                   | `string`  | 错误码                                   |
| error.message                                | `string`  | 错误提示信息                             |
| error.param                                  | `string`  | 请求 id                                  |

## 示例

### Gemini 兼容接口
我们兼容gemini的 `{xxx}/v1beat/models`接口，您可以直接使用官方SDK调用，例如 [python-genai](https://github.com/googleapis/python-genai)

`POST https://api.modelverse.cn/v1beta/models/gemini-2.5-flash-image:generateContent`

#### 图片生成（文本转图片）

> ⚠️ 注意：您必须在配置中添加 responseModalities: ["TEXT", "IMAGE"]。这些模型不支持仅图片输出。

<!-- tabs:start -->

##### ** curl **

```bash
curl --location 'https://api.modelverse.cn/v1beta/models/gemini-2.5-flash-image:generateContent' \
--header "x-goog-api-key: $MODELVERSE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
                }
            ]
        }
    ],
    "generationConfig": {
        "responseModalities": [
            "TEXT",
            "IMAGE"
        ]
    }
}' | jq -r '.candidates[0].content.parts[1].inlineData.data' \
| base64 -d > modelverse_generated_image.png
```

##### ** python **

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os


client = genai.Client(
    api_key=os.getenv("Modelverse_API_KEY", "<UModelverse_API_KEY>"),  # 您的API_KEY
    http_options=types.HttpOptions(
        base_url="https://api.modelverse.cn"
    ),
)

contents = [
    {
        "text": "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme.",
    },
]

generation_config = types.GenerationConfig(
    response_modalities=["text", "image"],
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=contents,
    config={
        "response_modalities": ["text", "image"],
    },
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("modelverse_generated_image.png")
)

```

<!-- tabs:end -->

#### 图片编辑（文本和图片转图片）

<!-- tabs:start -->

##### ** curl **

```bash
cat <<EOF | curl -X POST \
  --header "Authorization: Bearer ${MODELVERSE_API_KEY}" \
  --header "Content-Type: application/json" \
  --data @- \
  https://api.modelverse.cn/v1beta/models/gemini-2.5-flash-image:generateContent | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > modelverse_generated_image.png
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {"text": "Convert this photo to black and white, in a cartoonish style."},
        {
          "inlineData": {
            "mimeType": "image/jpeg",
            "data": "$(curl -s https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg | base64 | tr -d '\n')"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
EOF
```

##### ** python **

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

client = genai.Client(
    api_key=os.getenv("Modelverse_API_KEY", "<UModelverse_API_KEY>"),  # 您的API_KEY
    http_options=types.HttpOptions(
        base_url="https://api.modelverse.cn"
    ),
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text="Convert this photo to black and white, in a cartoonish style."
                ),
                types.Part(
                    file_data=types.FileData(
                        mime_type="image/jpeg",
                        file_uri="https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg",
                    )
                ),
            ],
        )
    ],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("modelverse_generated_image.png")

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
            "text": "That sounds incredibly unique! Here's a picture of a nano banana dish in a fancy restaurant with a Gemini theme:\n\n"
          },
          {
            "inlineData": {
              "data": "xxx",
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
    "candidatesTokensDetails": [
      {
        "modality": "IMAGE",
        "tokenCount": 1290
      },
      {
        "modality": "TEXT",
        "tokenCount": 25
      }
    ],
    "promptTokenCount": 16,
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 16
      }
    ],
    "totalTokenCount": 1331,
    "trafficType": "ON_DEMAND"
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
