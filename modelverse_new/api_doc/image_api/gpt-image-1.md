# gpt-image-1 API

本文介绍 `gpt-image-1` 模型调用 API 的输入输出参数，供您使用接口时查阅字段含义。

---

## 请求参数

### 请求体

| 字段名              | 类型   | 是否必须 | 默认值        | 描述                                                                                                                       |
| ------------------- | ------ | -------- | ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| prompt              | string | 必须     | -             | 提示词                                                                                                                     |
| model               | string | 必须     | -             | 本次请求使用的模型名称，此处为 `gpt-image-1`。                                                                             |
| n                   | int    | 可选     | 1             | 生成图片数量，取值范围为 1~4                                                                                               |
| size                | string | 可选     | "1024x1024"   | 分辨率。GPT‑image‑1 支持 `1024x1024`、`1024x1536`、`1536x1024`。                                                             |
| quality             | string | 可选     | -             | 图片质量，支持 `low`、`medium`、`high`；质量越高耗时越长。                                                                  |
| output_format       | string | 可选     | "png"         | 输出图片格式，支持 `png`、`jpeg`。                                                                                          |
| output_compression  | int    | 可选     | 100           | 图片压缩强度，取值 0~100；`0` 为不压缩，`100` 为最大压缩。                                                                  |

## 响应参数

| 字段名        | 类型      | 描述                                                                                                                                                                                                                                                    |
| ------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| created       | `integer` | 本次请求创建时间的 Unix 时间戳（秒）。                                                                                                                                                                                                                  |
| data          | `array`   | 输出图像的信息，包括图像下载的 URL 或 Base64，gpt-image-1模型返回的是base64数据。<br>• 当指定返回生成图像的格式为 url 时，则相应参数的子字段为 url；<br>• 当指定返回生成图像的格式为 b64_json 时，则相应参数的子字段为 b64_json。<br>注意：链接将在生成后 7 天内失效，请务必及时保存图像。 |
| error         | `Object`  | 错误信息对象                                                                                                                                                                                                                                            |
| error.code    | `string`  | 错误码                                                                                                                                                                                                                                                  |
| error.message | `string`  | 错误提示信息                                                                                                                                                                                                                                            |
| error.param   | `string`  | 请求 id                                                                                                                                                                                                                                                 |

## 示例

### OPENAI 兼容接口

`POST https://api.modelverse.cn/v1/images/generations`

#### 同步请求

<!-- tabs:start -->
#### ** curl **
```bash
curl --location 'https://api.modelverse.cn/v1/images/generations' \
  --header "Authorization: Bearer $MODELVERSE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "gpt-image-1",
    "prompt": "a beautiful flower",
    "size": "1024x1024",
    "quality": "high",
    "output_format": "png",
    "output_compression": 100
  }'
```

#### ** python **
```python
import os, base64
from openai import OpenAI

client = OpenAI(
    base_url="https://api.modelverse.cn/v1",
    api_key=os.getenv("MODELVERSE_API_KEY", "YOUR_API_KEY")
)

res = client.images.generate(
    model="gpt-image-1",
    prompt="a beautiful flower",
    size="1024x1024",
    quality="high",
)

# gpt-image-1 返回 base64 数据
image_b64 = res.data[0].b64_json
raw = image_b64.split(",")[-1] if image_b64.startswith("data:") else image_b64
with open("image.png", "wb") as f:
    f.write(base64.b64decode(raw))
print("Saved to image.png")
```
<!-- tabs:end -->

### 图片编辑

`POST https://api.modelverse.cn/v1/images/edits`

使用 multipart/form-data 传参，至少包含待编辑图片 `image`（可选 `mask`）、以及 `model`、`prompt` 等字段；其余参数如 `size`、`quality`、`output_format`、`output_compression` 与生成接口一致。

<!-- tabs:start -->
#### ** curl **
```bash
curl --location 'https://api.modelverse.cn/v1/images/edits' \
  --header "Authorization: Bearer $MODELVERSE_API_KEY" \
  -F "image=@/path/to/your/image.png" \
  -F "mask=@/path/to/your/mask.png" \
  -F "model=gpt-image-1" \
  -F "prompt=Add a beach ball in the center" \
  -F "size=1024x1024" \
  -F "n=1" \
  -F "quality=high" \
  -F "output_format=png" \
  -F "output_compression=100"
```

#### ** python **
```python
import os, base64, requests

url = "https://api.modelverse.cn/v1/images/edits"
headers = {"Authorization": f"Bearer {os.getenv('MODELVERSE_API_KEY', '$MODELVERSE_API_KEY')}"}

files = {
    "image": ("beach.png", open("beach.png", "rb"), "image/png"),
    # 可选：提供 mask 来限定编辑区域
    # "mask": ("mask.png", open("mask.png", "rb"), "image/png"),
}

data = {
    "model": "gpt-image-1",
    "prompt": "Add a beach ball in the center",
    "size": "1024x1024",
    "n": "1",
    "quality": "high",
    "output_format": "png",
    "output_compression": "100",
}

r = requests.post(url, headers=headers, files=files, data=data)
r.raise_for_status()
resp = r.json()

image_b64 = resp["data"][0]["b64_json"]
raw = image_b64.split(",")[-1] if image_b64.startswith("data:") else image_b64
with open("edit.png", "wb") as f:
    f.write(base64.b64decode(raw))
print("Saved to edit.png")
```
<!-- tabs:end -->

### 响应

```json
{
  "created": 1750667997,
  "data":
  [
    {
      "b64_json": "{image_base64_string}"
    }
  ],
  "usage":
  {
    "total_tokens": 4169,
    "input_tokens": 9,
    "output_tokens": 4160,
    "input_tokens_details":
    {
      "text_tokens": 9
    }
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

<!--
TODO:异步请求
### 异步请求

``` -->
