# 常见问题

## 如何查看支持的模型列表

您可以通过 `/v1/models` 接口获取所有支持的模型：

```shell
curl https://api.modelverse.cn/v1/models \
  -H "Content-Type: application/json"
```

推荐使用 `Cherry Studio` 客户端，配置 API 地址后点击管理按钮即可直观查看所有支持的模型。详细配置教程请参考：[Cherry Studio 配置教程](https://docs.ucloud.cn/modelverse/best_practice/scenario/cherry-studio)。

![获取模型](https://static.ucloud.cn/docs/modelverse/images/cherry-studio/model.png)

## GPT-5/o 系列模型参数报错

![官方文档](https://static.ucloud.cn/docs/modelverse/images/api-doc/gpt-5-para.png)

OpenAI 官方已将 `max_tokens` 参数标记为废弃（deprecated），GPT-5 系列和 o 系列模型均不再支持该参数。详情请参考 [OpenAI 官方文档](https://platform.openai.com/docs/api-reference/chat/create)。

如需传入图像文件，请使用 base64 编码，暂不支持 URL 方式。

## gpt-5-codex 和 gpt-5.1-codex 系列模型说明

这两个系列模型仅支持 `/v1/response/` 接口。

## Gemini 系列模型如何开启/关闭思考过程

使用 Gemini 协议的 `v1beta/models` 接口，并配置以下参数。详细文档请参考 [Gemini 协议兼容](https://docs.ucloud.cn/modelverse/api_doc/text_api/gemini_compatible)：

```json
"generationConfig": {
    "thinkingConfig": {
        "include_thoughts": true,
        "thinkingBudget": 0
    }
}
```

参数说明：
- `include_thoughts`：设置为 `true` 开启思考过程输出，设置为 `false` 关闭
- `thinkingBudget`：控制思考时间预算

## Claude *系列模型说明*

Claude Sonnet 4.5 仅支持指定 `temperature` 或 `top_p` 参数中的一个，不能同时使用这两个参数。详见 [官方文档说明](https://docs.aws.amazon.com/zh_cn/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-request-response.html)。

## Gemini 系列模型安全等级说明

Gemini API 提供了灵活的安全设置功能，允许您在原型设计和生产环境中根据应用场景调整内容过滤策略。通过配置安全等级，您可以在五个过滤器类别中精确控制内容审核的严格程度。

相关文档：
- [Gemini API 兼容文档](https://docs.ucloud.cn/modelverse/api_doc/text_api/gemini_compatible)
- [Google 官方安全设置文档](https://ai.google.dev/gemini-api/docs/safety-settings?hl=zh-cn)

### 安全设置配置示例

以下示例展示如何关闭所有内容过滤（`BLOCK_NONE`），适用于需要最大灵活性的开发场景：

```json
{
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_CIVIC_INTEGRITY",
      "threshold": "BLOCK_NONE"
    }
  ]
}
```

### 可用的过滤类别

- `HARM_CATEGORY_HATE_SPEECH`：仇恨言论
- `HARM_CATEGORY_SEXUALLY_EXPLICIT`：色情内容
- `HARM_CATEGORY_DANGEROUS_CONTENT`：危险内容
- `HARM_CATEGORY_HARASSMENT`：骚扰内容
- `HARM_CATEGORY_CIVIC_INTEGRITY`：公民诚信

### 可用的阈值选项

阈值（HarmBlockThreshold）用于控制在达到或超过指定有害概率时进行内容屏蔽：

- `HARM_BLOCK_THRESHOLD_UNSPECIFIED`：阈值未指定
- `BLOCK_LOW_AND_ABOVE`：允许"可忽略"风险的内容，屏蔽"低"及以上风险的内容
- `BLOCK_MEDIUM_AND_ABOVE`：允许"可忽略"和"低"风险的内容，屏蔽"中"及以上风险的内容
- `BLOCK_ONLY_HIGH`：允许"可忽略"、"低"和"中"风险的内容，仅屏蔽"高"风险内容
- `BLOCK_NONE`：允许所有内容，不进行任何屏蔽
- `OFF`：关闭安全过滤功能

根据您的应用需求和使用场景选择合适的阈值配置。建议在生产环境中使用更严格的过滤策略以确保内容安全。