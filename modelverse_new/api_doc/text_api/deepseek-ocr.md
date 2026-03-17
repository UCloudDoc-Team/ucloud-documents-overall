# DeepSeek-OCR 模型

DeepSeek-OCR 是一款先进的 OCR 模型，能够识别图片中的文字并将其转换为指定的文本格式。

## 请求示例

您可以通过向 `https://api.modelverse.cn/v1/chat/completions` 端点发送请求来使用 DeepSeek-OCR 模型。

> **说明：**
> DeepSeek-OCR 支持 `max_tokens` 参数最大设置为 **8192**。当前该模型免费开放使用，无需付费。
>
> **注意：** 该模型输入仅支持 base64 编码的图片（即 "data:image/..." 格式），不支持直接通过 image_url 远程图片地址。如果你的图片在远程地址，可以通过如下命令一键获取 base64 字符串：
>
> ```bash
> curl -s https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg | base64 | tr -d '\n'
> ```


### 非流式请求

<!-- tabs:start -->
#### **cURL**
```bash
curl https://api.modelverse.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $YOUR_API_KEY" \
  -d '{
    "model": "deepseek-ai/DeepSeek-OCR",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "convert to markdown"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,'$(curl -s https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg | base64 | tr -d '\n')'"
            }
          }
        ]
      }
    ]
  }'
```
#### **Python**
```python
import base64
import os
from openai import OpenAI

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = os.path.expanduser("ucloud.png")

# Getting the base64 string
base64_image = encode_image(image_path)

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY", "<YOUR_MODELVERSE_API_KEY>"),
    base_url="https://api.modelverse.cn/v1/",
)

response = client.chat.completions.create(
  model="deepseek-ai/DeepSeek-OCR",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "convert to markdown"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ]
)

print(response.choices[0].message.content)
```
<!-- tabs:end -->

### 流式请求

通过将 `stream` 参数设置为 `true`，您可以实现流式响应。

<!-- tabs:start -->
#### **cURL**
```bash
curl https://api.modelverse.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $YOUR_API_KEY" \
  -d '{
    "model": "deepseek-ai/DeepSeek-OCR",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "convert to markdown"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/jpeg;base64,'$(curl -s https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg | base64 | tr -d '\n')'"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```
#### **Python**
```python
import base64
import os
from openai import OpenAI

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = os.path.expanduser("ucloud.png")

# Getting the base64 string
base64_image = encode_image(image_path)

client = OpenAI(
    api_key=os.getenv("MODELVERSE_API_KEY", "<YOUR_MODELVERSE_API_KEY>"),
    base_url="https://api.modelverse.cn/v1/",
)

stream = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "convert to markdown"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```
<!-- tabs:end -->
