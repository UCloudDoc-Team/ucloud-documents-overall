# Qwen/Qwen-Image API

本文介绍 `Qwen/Qwen-Image` 模型调用 API 的输入输出参数，供您使用接口时查阅字段含义。

---

## 请求参数

### 请求体

| 字段名 | 类型   | 是否必须 | 默认值 | 描述                                                                                             |
| ------ | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------ |
| prompt | string | 必须     | -      | 提示词                                                                                           |
| model  | string | 必须     | -      | 本次请求使用的模型名称，此处为 `Qwen/Qwen-Image`。                                               |
| seed   | int    | 可选     | -1     | 随机数种子，用于控制模型生成内容的随机性。如果希望生成内容保持一致，可以使用相同的 seed 参数值。 |
| size   | string | 可选     | -      | 生成图像的尺寸（宽x高），每个维度范围 256 ~ 1536。例如：`1024x1024`                              |

## 响应参数

| 字段名        | 类型      | 描述                                                                                                                                                                                                                                                    |
| ------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| created       | `integer` | 本次请求创建时间的 Unix 时间戳（秒）。                                                                                                                                                                                                                  |
| data          | `array`   | 输出图像的信息，包括图像下载的 URL 或 Base64。<br>• 当指定返回生成图像的格式为 url 时，则相应参数的子字段为 url；<br>• 当指定返回生成图像的格式为 b64_json 时，则相应参数的子字段为 b64_json。<br>注意：链接将在生成后 7 天内失效，请务必及时保存图像。 |
| error         | `Object`  | 错误信息对象                                                                                                                                                                                                                                            |
| error.code    | `string`  | 错误码                                                                                                                                                                                                                                                  |
| error.message | `string`  | 错误提示信息                                                                                                                                                                                                                                            |
| error.param   | `string`  | 请求 id                                                                                                                                                                                                                                                 |

## 示例

### OPENAI 兼容接口

`POST https://api.modelverse.cn/v1/images/generations`

#### 同步请求

```bash
curl --location 'https://api.modelverse.cn/v1/images/generations' \
--header "Authorization: Bearer $MODELVERSE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "Qwen/Qwen-Image",
    "prompt": "Convert to quick pencil sketch",
    "size": "1024x1024"
}'
```

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("BASE_URL", "https://api.modelverse.cn/v1"),
    api_key=os.getenv("API_KEY", "$MODELVERSE_API_KEY")
)

response = client.images.generate(
    model="Qwen/Qwen-Image",
    prompt="Convert to quick pencil sketch",
    size="1024x1024"
)

print(response.data[0].url)
```

### 响应

```json
{
  "created": 1750667997,
  "data": [
    {
      "url": "https://xxxxx/xxxx.png",
      "b64_json": "data:image/png;base64,{image_base64_string}"
    }
  ],
  "usage": {
    "input_tokens_details": {}
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
