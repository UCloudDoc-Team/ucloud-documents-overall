# 认证鉴权

## 简介

ModelVerse API 使用 API Key 进行认证。所有 API 请求都必须在 HTTP 请求头中包含有效的 API Key。

## 获取API Key

请访问 [ModelVerse 控制台](https://console.ucloud.cn/modelverse/experience/api-keys) 来创建和管理您的 API Key。

> 注意：请妥善保管您的 API Key，不要泄露给他人。

![API Key 页面](https://static.ucloud.cn/docs/modelverse/images/api-doc/certificate-page.png)

## 调用地址

Modelverse API地址提供两种方式，两个地址调用内容一样。

调用地址1：
```
GET https://api.modelverse.cn/v1/models
```

调用地址2：

主要用于海外无法使用`.cn`域名场景
```
GET https://api.umodelverse.ai/v1/models
```

## 最简调用

请将 `{api_key}` 替换为您的 API Key。

```bash
curl --location 'https://api.modelverse.cn/v1/chat/completions' \
--header "Authorization: Bearer {api_key}" \
--header 'Content-Type: application/json' \
--data '{
    "model": "deepseek-ai/DeepSeek-R1",
    "messages": [
        {
            "role": "user",
            "content": "一句话描述UCloud这家公司。"
        }
    ]
}' | jq .
```

你可能看到的返回结果。

```
{
  "id": "0a7919c4-981e-438b-ad30-e943b96882b6",
  "object": "chat.completion",
  "created": 1763015400,
  "model": "deepseek-r1-250528",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "用中立、安全、本土化的云计算服务，专注服务中国企业数字化转型的科创板上市云服务商。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 348,
    "total_tokens": 358,
    "prompt_tokens_details": null,
    "completion_tokens_details": {
      "audio_tokens": 0,
      "reasoning_tokens": 185,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": "",
  "search_result": null
}
```