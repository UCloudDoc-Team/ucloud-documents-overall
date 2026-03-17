# doubao-seedream-4.5 API

本文介绍 `doubao-seedream-4.5` 模型调用 API 的输入输出参数，供您使用接口时查阅字段含义。

---

## 请求参数

### 请求体

| 字段名                              | 类型   | 是否必须 | 默认值            | 描述                               |
| ----------------------------------- | ------ | -------- | ----------------- | ---------------------------------- |
| model                            | string  | 必须     | -                 | 本次请求使用的模型名称，此处为doubao-seedream-4.5   |
| prompt                       | string | 必须     | -            | 用于生成图像的提示词，支持中英文，建议不超过300个汉字或600个英文单词。    |
| images                     | array(string)  | 可选     | -                 | 输入的图片信息，支持 URL 或 Base64 编码。支持单图或多图输入，最多支持传入 14 张参考图。                   |
| size                 | string | 可选     | -                 | 指定生成图像的尺寸信息，支持以下两种方式，不可混用。<br>方式 1 ： 指定生成图像的分辨率，并在prompt中用自然语言描述图片宽高比、图片形状或图片用途，最终由模型判断生成图片的大小。可选值：2K、4K。<br>方式2：指定生成图像的宽高像素值，默认值：2048x2048，总像素取值范围：[2560x1440=3686400, 4096x4096=16777216] ，宽高比取值范围：[1/16, 16]，推荐：2048x2048，2304x1728，1728x2304，2560x1440，1440x2560，2496x1664，1664x2496，3024x1296                       |
| sequential_image_generation          | string | 可选     | disabled                | 控制是否关闭组图功能。<br>auto：自动判断模式，模型会根据用户提供的提示词自主判断是否返回组图以及组图包含的图片数量。<br>disabled：关闭组图功能，模型只会生成一张图。 |
| sequential_image_generation<br>_options  | object | 可选     | -                 | 组图功能的配置。仅当 sequential_image_generation 为 auto 时生效。 |
| sequential_image_generation<br>_options.max_images      | integer | 可选     | -                 | 指定本次请求，最多可生成的图片数量。取值范围： [1, 15]                |
| stream             | Boolean | 可选     | false                 | 控制是否开启流式输出模式。<br>false：非流式输出模式，等待所有图片全部生成结束后再一次性返回所有信息。<br>true：流式输出模式，即时返回每张图片输出的结果。在生成单图和组图的场景下，流式输出模式均生效。 |
| response_format    | string | 可选     | url                 | 指定生成图像的返回格式。<br>生成的图片为 jpeg 格式，支持以下两种返回方式：<br>url：返回图片下载链接；链接在图片生成后24小时内有效，请及时下载图片。<br>b64_json：以 Base64 编码字符串的 JSON 格式返回图像数据。 |
| watermark     | Boolean | 可选     | true                 | 是否在生成的图片中添加水印。<br>false：不添加水印。<br>true：在图片右下角添加“AI生成”字样的水印标识。 |
| optimize_prompt_options                    | object | 可选     | -                 | 提示词优化功能的配置。                         |
| optimize_prompt_options.mode | string  | 可选     | standard | 设置提示词优化功能使用的模式。当前仅支持 standard 模式。 |

## 非stream响应参数

| 字段名        | 类型      | 描述                                                                                                                                                                                                                                                    |
| ------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model      | `string` | 本次请求使用的模型 ID （模型名称-版本）。                                                                                                                                                                                                                  |
| created          | `integer`   | 本次请求创建时间的 Unix 时间戳（秒）。 |
| data         | `array`  | 输出图像的信息。可能是图像信息，也可能是错误信息。  |
| data.url    | `string`  | 图片的 url 信息，当 response_format 指定为 url 时返回。该链接将在生成后 24 小时内失效，请务必及时保存图像。|
| data.b64_json | `string`  | 图片的 base64 信息，当 response_format 指定为 b64_json 时返回。                                                                                                                  |
| data.size   | `string`  | 图像的宽高像素值，格式 <宽像素>x<高像素>，如2048×2048。   |
| data.error | `object`  | 错误信息结构体。                                                                                                                                                                                                                                            |
| data.error.code   | `string`  | 某张图片生成错误的错误码。                                                                                                                                                                                                                                                 |
| data.error.message | `string`  | 某张图片生成错误的提示信息。                                                                                                                                                                                                                                            |
| usage   | `object`  | 本次请求的用量信息。                                                                                                                                                                                                                                                 |
| usage.generated_images | `integer`  | 模型成功生成的图片张数，不包含生成失败的图片。仅对成功生成图片按张数进行计费。                                                                                                                                                                                                                                            |
| usage.output_tokens   | `integer`  | 模型生成的图片花费的 token 数量。<br>计算逻辑为：计算 sum(图片长*图片宽)/256 ，然后取整。                                                                                                                                                                                                                                               |
| usage.total_tokens | `integer`  | 本次请求消耗的总 token 数量。<br>当前不计算输入 token，故与 output_tokens 值一致。                                                                                                                                                                                                                                            |
| error   | `object`  | 本次请求，如发生错误，对应的错误信息。                                                                                                                                                                                                                                                 |
| error.code | `string`  | 错误码。                                                                                                                                                                                                                                            |
| error.message   | `string`  | 错误提示信息。                                                                                                                                                                                                                                                |

## stream响应参数

当您调用图片生成API 并将 stream 设置为 true 时，服务器会在生成响应的过程中，通过 Server-Sent Events（SSE）实时向客户端推送事件。以下为服务器会推送的各类事件。

### image_generation.partial_succeeded：
在流式响应模式下，当任意图片生成成功时返回该事件。

| 字段名                                       | 类型      | 描述                                     |
| -------------------------------------------- | --------- | ---------------------------------------- |
| type                                   | `string`   | 在流式响应模式下，当任意图片生成成功时返回该事件。这里应为：image_generation.partial_succeeded。                     |
| model                           | `string`  | 本次请求使用的模型 ID。                               |
| created                     | `integer`   | 本次请求创建时间的 Unix 时间戳（秒）。 |
| image_index                | `integer`  | 本次生图请求中，本次事件对应图片在请求中的序号。从 0开始累加，不管生图是否成功，即在 image_generation.partial_succeeded、image_generation.partial_failed 事件，均会自动累加 1。                     |
| url          | `string`  | 本次事件对应图片的下载 URL。当请求中配置字段 response_format 为 url 时返回。                        |
| b64_json     | `string`  | 本次事件对应图片的 Base64 编码。当请求中配置字段 response_format 为 b64_json 时返回。                  |
| size | `string`  | 图像的宽高像素值，格式<宽像素>×<高像素>，如 2048×2048。     |

### image_generation.partial_failed：
在流式返回模式下，当任意图片生成失败时返回该事件。

| 字段名                                       | 类型      | 描述                                     |
| -------------------------------------------- | --------- | ---------------------------------------- |
| type                                   | `string`   | 此处应为 image_generation.partial_failed                     |
| model                           | `string`  | 本次请求使用的模型 ID。                               |
| created                     | `integer`   | 本次请求创建时间的 Unix 时间戳（秒）。 |
| image_index                | `integer`  | 本次生图请求中，本次事件对应图片在请求中的序号。从 0开始累加，不管图片是否生成成功，即在image_generation.partial_succeeded、image_generation.partial_failed 事件，均会自动累加 1。                     |
| error          | `object`  | 本次生图请求中，本次事件对应的错误原因。                        |
| error.code     | `string`  | 错误码。                  |
| error.message | `string`  | 错误提示信息。     |

### image_generation.completed：
请求的所有图片（无论成功或失败）均处理完毕后返回，是该流式返回的最后一个响应事件。

| 字段名                                       | 类型      | 描述                                     |
| -------------------------------------------- | --------- | ---------------------------------------- |
| type                                   | `string`   | 此处应为 image_generation.completed。                    |
| model                           | `string`  | 本次请求使用的模型 ID。                               |
| created                     | `integer`   | 本次请求创建时间的 Unix 时间戳（秒）。 |
| usage                | `object`  | 本次请求的用量信息。                     |
| usage.generated_images          | `integer`  | 模型成功生成的图片张数，不包含生成失败的图片。仅对成功生成图片按张数进行计费。                     |
| usage.output_tokens    | `integer`  | 模型生成的图片花费的 token 数量。<br>计算逻辑为：计算sum(图片长*图片宽)/256 ，然后取整                  |
| usage.total_tokens | `integer`  | 本次请求消耗的总 token 数量。当前不计算输入 token，故与 output_tokens 值一致。     |

## 示例

### OPENAI 兼容接口

`POST https://api.modelverse.cn/v1/images/generations`

<!-- tabs:start -->
#### ** curl **
```bash
curl --location 'https://api.modelverse.cn/v1/images/generations' \
  --header "Authorization: Bearer $MODELVERSE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "doubao-seedream-4.5",
    "prompt": "将图片转换为铅笔素描",
    "images": ["https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg"],
    "size": "2k",
    "watermark": false,
    "stream": false,
    "response_format":"url"
  }'
  ```
#### ** python **
```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.modelverse.cn/v1",
    api_key=os.getenv("MODELVERSE_API_KEY", "YOUR_API_KEY")
)

response = client.images.generate(
    model="doubao-seedream-4.5",
    prompt="Convert to quick pencil sketch",
    extra_body={
        "images":["https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg"],
        "size":"2K",
        "response_format":"url",
        "watermark":False
    }
)

print(response.data[0].url)
```
<!-- tabs:end -->
###响应
```json
{
	"model": "doubao-seedream-4-5-251128",
	"created": 1767939740,
	"data": [{
		"url": "https://xxxxxx",
		"size": "2048x2048"
	}],
	"usage": {
		"generated_images": 1,
		"output_tokens": 16384,
		"total_tokens": 16384
	}
}
```