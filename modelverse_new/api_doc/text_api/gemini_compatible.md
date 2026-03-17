# Gemini 快速开始

UModelverse 平台提供了与 Google Gemini API 兼容的 **Models** 接口，开发者可以使用 Gemini SDK 或其他支持的工具直接调用 Modelverse 上的 **Gemini 模型**。

本文将向您介绍如何快速在 UModelverse 平台发出您的第一个 Gemini API 请求。

## 快速开始

### 安装 Google GenAI SDK
安装 python 语言的 sdk

> 使用 Python 3.9 及更高版本，通过以下 pip 命令安装 google-genai 软件包：

```python
pip install google-genai
```

### 示例
以下示例使用 generateContent 方法，通过`gemini-3-flash-preview`模型向 UModelverse API 发送请求。

> 请确保将 `$MODELVERSE_API_KEY` 替换为您自己的 API Key，获取 [API Key](https://console.ucloud.cn/modelverse/experience/api-keys)。


#### 非流式调用
您可以使用以下代码进行调用。请注意，我们需要通过 `http_options` 来指定 Modelverse 的 API 地址。

 <!-- tabs:start -->
#### ** python **

```python
from google import genai
from google.genai import types

client = genai.Client(
   api_key="<MODELVERSE_API_KEY>",
   http_options=types.HttpOptions(
       base_url="https://api.modelverse.cn"
   ),
)

response = client.models.generate_content(
   model="gemini-3-flash-preview",
   contents=[
       {"text": "How does AI work?"},
   ],
   config=types.GenerateContentConfig(
       thinking_config=types.ThinkingConfig(thinking_budget=0),
   ),
)
print(response.text)
```
#### 参数说明：开启思考总结
详细内容可参考[官方文档](https://ai.google.dev/gemini-api/docs/thinking?hl=zh-cn#summaries)

如需开启思考总结，可在 `thinking_config` 中添加：

```python
config=types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True
    )
)
```
#### ** curl **

```bash
curl "https://api.modelverse.cn/v1beta/models/gemini-3-flash-preview:generateContent" \
    -H "x-goog-api-key: $MODELVERSE_API_KEY" \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{
          "contents": [
            {
              "parts": [
                {
                  "text": "How does AI work?"
                }
              ]
            }
          ],
          "generationConfig": {
            "thinkingConfig": {
              "thinkingBudget": 0
            }
          }
        }'
```
<!-- tabs:end -->


#### 流式调用

 <!-- tabs:start -->
#### ** python **

```python
from google import genai
from google.genai import types

client = genai.Client(
    api_key="<MODELVERSE_API_KEY>",
    http_options=types.HttpOptions(
        base_url="https://api.modelverse.cn"
    ),
)

response = client.models.generate_content_stream(
    model="gemini-3-flash-preview", contents=["Explain how AI works"]
)
for chunk in response:
    print(chunk.text, end="")

```

#### ** curl **

```bash
curl "https://api.modelverse.cn/v1beta/models/gemini-3-flash-preview:GenerateContent?alt=sse" \
    -H "Authorization: Bearer $MODELVERSE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "contents": [
        {
          "role": "user",
          "parts": [
            {
              "text": "Explain how AI works"
            }
          ]
        }
      ]
    }'
```
<!-- tabs:end -->

### 文档理解

Gemini 模型可以处理 PDF 格式的文档，并使用原生视觉功能来理解整个文档的上下文。这不仅仅是提取文本，还让 Gemini 能够：

*   分析和解读内容，包括文本、图片、图表、图表和表格，即使是长达 1,000 页的文档也能轻松应对。
*   以结构化输出格式提取信息。
*   根据文档中的视觉和文本元素总结内容并回答问题。
*   转写文档内容（例如转写为 HTML），同时保留布局和格式，以便在下游应用中使用。
您也可以通过相同的方式传递非 PDF 文档，但 Gemini 会将这些文档视为普通文本，从而消除图表或格式等上下文。

#### 以内嵌方式传递 PDF 数据
您可以在向 generateContent 发出的请求中内嵌传递 PDF 数据。此方法最适合处理较小的文档或临时处理，因为您无需在后续请求中引用该文件。

以下示例展示了如何从网址提取 PDF 并将其转换为字节以进行处理：

 <!-- tabs:start -->
#### ** python **

```python
from google import genai
from google.genai import types
import httpx

client = genai.Client(
    api_key="<MODELVERSE_API_KEY>",
    http_options=types.HttpOptions(
        base_url="https://api.modelverse.cn"
    ),
)

doc_url = "https://umodelverse-inference.cn-wlcb.ufileos.com/gemini-pdf.pdf"

# Retrieve and encode the PDF byte
doc_data = httpx.get(doc_url).content

prompt = "Summarize this document"
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part.from_bytes(
            data=doc_data,
            mime_type='application/pdf',
        ),
        prompt
    ]
)

print(response.text)
```

#### ** curl **

```bash
DOC_URL="https://umodelverse-inference.cn-wlcb.ufileos.com/gemini-pdf.pdf"
PROMPT="Summarize this document"
DISPLAY_NAME="base64_pdf"

# Download the PDF
wget -O "${DISPLAY_NAME}.pdf" "${DOC_URL}"

# Check for FreeBSD base64 and set flags accordingly
if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
  B64FLAGS="--input"
else
  B64FLAGS="-w0"
fi

# Base64 encode the PDF
ENCODED_PDF=$(base64 $B64FLAGS "${DISPLAY_NAME}.pdf")

# Generate content using the base64 encoded PDF
curl "https://api.modelverse.cn/v1beta/models/gemini-3-flash-preview:generateContent" \
    -H "x-goog-api-key: $MODELVERSE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"inline_data": {"mime_type": "application/pdf", "data": "'"$ENCODED_PDF"'"}},
          {"text": "'$PROMPT'"}
        ]
      }]
    }' 2> /dev/null > response.json

cat response.json
echo

jq ".candidates[].content.parts[].text" response.json

# Clean up the downloaded PDF
rm "${DISPLAY_NAME}.pdf"
```
<!-- tabs:end -->

您还可以从本地文件读取 PDF 以进行处理：

```python
from google import genai
from google.genai import types
import pathlib

client = genai.Client(
    api_key="<MODELVERSE_API_KEY>",
    http_options=types.HttpOptions(
        base_url="https://api.modelverse.cn"
    ),
)

# Retrieve and encode the PDF byte
filepath = pathlib.Path('file.pdf')

prompt = "Summarize this document"
response = client.models.generate_content(
  model="gemini-3-flash-preview",
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)
```

## 模型ID说明
更多受支持的gemini模型，请参考【获取模型列表】


> 更多字段详情，见[Gemini官方文档](https://ai.google.dev/api/models?hl=zh-cn)

