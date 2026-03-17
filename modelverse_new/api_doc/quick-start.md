# 快速开始

本指南旨在帮助您快速熟悉并调用模型服务平台的API。跟随以下步骤，您将在几分钟内完成第一次API调用。

> 我们强烈推荐你使用OpenAI API的调用方式。因为OpenAI的API已经成为大模型行业的事实标准，这意味着有海量的教程、工具和代码库都可以直接复用。我们的服务完全兼容这套标准，让你能无缝衔接主流生态，节约大量学习成本。

OpenAI 兼容接口当前支持：

- `/v1/chat/completions` 核心接口，用于与模型进行对话。
- `/v1/response` OpenAI 最先进的模型响应生成接口。支持文本和图像输入，以及文本输出。
- `/v1/models` 用于获取模型列表。

## 第一步：获取API密钥

在调用任何API之前，您需要一个有效的API密钥。请前往【[认证鉴权](/api_doc/common/certificate)】文档，查看如何获取和管理您的密钥。

## 第二步：选择模型

你可以通过下方API获取模型列表，选择你需要的模型。

```
GET https://api.modelverse.cn/v1/models

#主要用于海外无法使用`.cn`域名场景
GET https://api.umodelverse.ai/v1/models
```

请求示例：
```
curl https://api.modelverse.cn/v1/models \
  -H "Content-Type: application/json" | jq .
```

预期返回：

```json
{
  "data": [
    {
      "created": 1762741377,
      "id": "deepseek-ai/DeepSeek-R1",
      "object": "model",
      "owned_by": "UCloud_UModelverse"
    },
    {
      "created": 1762741326,
      "id": "gpt-5",
      "object": "model",
      "owned_by": "UCloud_UModelverse"
    },
    ......
  ],
  "object": "list"
}
```

其中`id`字段即为模型名称，以实际返回为准。

## 第三步：调用API

### 典型方式1 - 任何语言通过http调用

> 这是最基础、最通用的调用方式。无论你使用什么编程语言，只要能发送网络请求（HTTP请求），就可以通过这种方式调用API。你需要知道三个核心信息：模型名称、你的API密钥和我们的API地址。

我们完全支持OpenAI API请求规范，因为OpenAI API接口标准也经常更新，所以建议直接以[OpenAI API官网文档](https://platform.openai.com/docs/api-reference/chat/create)为准。

请将`{api_key}`替换为您的API密钥，将`{model_name}`替换为您上一步获取到列表中的模型名称（选择一个即可）。

```bash
curl https://api.modelverse.cn/v1/chat/completions \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer {api_key}" \
 -d '{
   "model": "{model_name}",
   "messages": [
     {
       "role": "system",
       "content": "You are a helpful assistant."
     },
     {
       "role": "user",
       "content": "一句话描述UCloud这家公司。"
     }
   ],
   "stream": true
 }' | jq .
```

参数说明：

- model：模型名称，填入上一步获取的 id，例如 "deepseek-ai/DeepSeek-R1"。
- messages：你要发送给模型的内容。
- stream：是否“流式”返回。
	- true：模型会像打字一样，逐字或逐词地返回结果，适合用于实时聊天界面。（任然是json格式数据）
	- false：模型会一次性生成全部答案后，再完整地返回给你。

预期返回如下，其中主要关注`choices`字段，它包含模型的回复，`usage`字段包含模型的使用情况（内容可能不相同，仅供参考）：

```json
{
  "id": "52ba2d24-f745-42b3-82c3-610a7b2658b0",
  "object": "chat.completion",
  "created": 1763020876,
  "model": "gemini-2.5-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "UCloud (优刻得) 是一家中立、安全、可靠的云计算服务平台，致力于为全球企业级客户提供全面的云服务解决方案。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 1505,
    "total_tokens": 1514,
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    },
    "completion_tokens_details": {
      "audio_tokens": 0,
      "reasoning_tokens": 1357,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": "",
  "search_result": null
}
```

### 典型方式2 - OpenAI SDK

> OpenAI官方为开发者提供了非常便捷的SDK（软件开发工具包），它把复杂的HTTP请求封装成了简单的函数调用，代码更易读、更易维护。这是我们最推荐开发者使用的方式。

> 可以参考[OpenAI SDK文档](https://github.com/openai/openai-python)。也可在[OpenAI GitHub](https://github.com/openai)中寻找需要的语言SDK。


```python
pip install -U openai
```

```python
from openai import OpenAI
import os

client = OpenAI(
   api_key="{api_key}",
   base_url="https://api.modelverse.cn/v1/",
)

chat_completion = client.chat.completions.create(
   messages=[
       {
           "role": "user",
           "content": "一句话描述UCloud这家公司。",
       }
   ],
   model="{model_name}",
)

print(chat_completion.choices[0].message.content)

```

### 典型方式3 - LangChain

> 当你不再满足于简单的“一问一答”，想要构建更复杂的AI应用（比如能调用工具的AI助理、能分析文档的机器人等）时，LangChain就是一个强大的开发框架。它能很好地与我们的API兼容。

可以参考[LangChain Python SDK文档](https://docs.langchain.com/oss/python/langchain/overview) 或 [LangChain JavaScript SDK文档](https://docs.langchain.com/oss/javascript/langchain/overview)。

```python
from langchain_openai import ChatOpenAI
from langchain import LLMChain
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model_name="{model_name}",
    openai_api_key="{api_key}",
    openai_api_base="https://api.modelverse.cn/v1/",
)

prompt = ChatPromptTemplate.from_template(
    """
    {input}
    """
)

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("一句话描述UCloud这家公司。"))
```

