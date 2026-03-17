# 错误码

如果请求错误，服务器返回的 JSON 文本包含以下参数。

| HTTP 状态码 | 类型                  | 错误码                | 错误信息                                                  | 描述                                                                                      |
| ----------- | --------------------- | --------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 400         | invalid_request_error | param_error           | Invalid param                                             | 参数不合法，调用我们未支持的接口时会触发                                                                                |
| 400         | invalid_request_error | invalid_messages      | Sensitive chat messages                                   | 对话内容触发敏感词/合规校验                                                               |
| 400         | invalid_request_error | sensitive_check_error | Sensitive check error                                     | 合规/敏感内容检测失败                                                                     |
| 400         | invalid_request_error | websearch_error       | Web search error                                          | 联网搜索失败或不可用                                                                      |
| 400         | invalid_request_error | model_error           | No permission to use the model                            | 没有模型权限                                                                              |
| 400         | invalid_request_error | tokens_too_long       | Prompt tokens too long                                    | 提示词过长                                                                                |
| 401         | invalid_request_error | auth_error            | Validate Certification failed                             | token 无效，用户可以参考[鉴权说明](/api_doc/common/certificate)获取最新密钥 |
| 408         | timeout               | timeout               | Request timeout, please try again later                   | 请求超时，请稍后重试                                                                      |
| 429         | rate_limit_error      | rate_limit            | Rate limit exceeded, please try again later               | 触发限流，请稍后重试                                                                      |
| 500         | internal_error        | internal_error        | Internal Server Error                                     | 服务器内部错误                                                                            |
| 500         | internal_error        | model_server_error    | Request llm server Error                                  | LLM 服务异常                                                                              |
| 504         | timeout               | gateway_timeout_error | Gateway timeout, please try again later or use stream api | 网关超时，请稍后重试或使用流式接口                                                        |
