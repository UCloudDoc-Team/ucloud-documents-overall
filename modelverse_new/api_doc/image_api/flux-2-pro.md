# flux-2-pro

本文介绍 `flux-2-pro` 模型调用 API 的输入输出参数，供您使用接口时查阅字段含义。

---

以下只展示部分使用到的字段说明，flux-2-pro API 详细字段见[flux-2-pro 官网文档](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-[pro])

## 请求地址

`POST https://api.modelverse.cn/v1/flux-2-pro`

## 认证方式

### API Key

与官方不同，我们不使用 `x-key`，而是使用 `Authorization`。

## 请求参数

### 请求体

|字段名|类型|是否必须|默认值|描述|
|---|---|---|---|---|
|prompt|string|是|无|提示词|
|input_image|string|否|无|图片base64|
|input_image_2|string|否|无|图片base64|
|input_image_3|string|否|无|图片base64|
|input_image_4|string|否|无|图片base64|
|input_image_5|string|否|无|图片base64|
|input_image_6|string|否|无|图片base64|
|input_image_7|string|否|无|图片base64|
|input_image_8|string|否|无|图片base64|
|seed|int|否|无|种子,可选种子以保证可重复性。|
|width|int|否|无|图片宽度,x >= 64，必须是32的倍数|
|height|int|否|无|图片高度,x >= 64，必须是32的倍数|
|safety_tolerance|string|否|无|输入和输出调节的容忍水平，可选值为1-6。0表示最严格，6表示最不严格。|
|output_format|jpeg/png|否|png|输出格式，可选值为png,jpg。|
|webhook_url|string|否|无|Webhook URL，用于接收生成结果。|
|webhook_secret|string|否|无|Webhook Secret，用于验证Webhook请求。|

## 响应参数

|字段名|类型|描述|
|---|---|---|
|createed|int|创建时间|
|input_mp|int|输入图片像素，单位 百万,向上取整|
|output_mp|int|输出图片像素，单位 百万,向上取整|
|total_pixels|int|总像素|
|data|[object]|图片数据|
|data.[].b64_json|string|图片base64|

## 示例

#### curl

```bash
curl -X POST "https://api.modelverse.cn/v1/flux-2-pro" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MODELVERSE_API_KEY" \
  -d '{
     "prompt" : "A photograph of a red fox in an autumn forest",
     "width": 1024,
     "height": 1024
    }' | jq -r '.data[0].b64_json' | base64 --decode > flux-2-pro.png
```

#### python
```python
import requests
import os

url = "https://api.modelverse.cn/v1/flux-2-pro"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('MODELVERSE_API_KEY')}"
}
payload = {
    "prompt": "A photograph of a red fox in an autumn forest",
    "width": 1024,
    "height": 1024
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(result)
```