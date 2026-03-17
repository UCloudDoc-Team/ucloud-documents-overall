# Kling/v2.6-T2V

文生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                    | 类型   | 是否必选 | 描述                                                                                                                                    |
| :---------------------- | :----- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| model                   | string | 是       | 模型名称，此处为 `kling-v2-6`                                                                                                       |
| input.prompt            | string | 是       | 提示词，用于指导视频生成                                                                                                                |
| input.negative_prompt    | string | 否       | 反向提示词，用于限制不希望出现的内容                                                                                                    |
| parameters.mode         | string | 否       | 生成模式，可选值：`std`、`pro`，默认为 `pro` 目前只支持`pro`                                                                                              |
| parameters.aspect_ratio | string | 否       | 视频长宽比，可选值：`16:9`、`9:16`、`1:1`                                                                                               |
| parameters.duration     | int    | 否       | 视频时长（秒），可选值：`5`、`10`，默认为 `5`                                                                                            |

**注意**：
-v2.6 不支持有声视频（包含音色 `voice_list`、`sound` 参数），如需支持请联系技术支持。

### 请求示例

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "kling-v2-6",
    "input": {
      "prompt": "A beautiful girl is dancing in a garden"
    },
    "parameters": {
      "mode": "pro",
      "aspect_ratio": "16:9",
      "duration": 5
    }
  }'
```

### 输出

| 参数           | 类型   | 描述               |
| :------------- | :----- | :----------------- |
| output.task_id | string | 异步任务的唯一标识 |
| request_id     | string | 请求的唯一标识     |

### 响应示例

```json
{
  "output": {
    "task_id": "task_id"
  },
  "request_id": "request_id"
}
```

## 查询任务状态

### 接口

`https://api.modelverse.cn/v1/tasks/status?task_id=<task_id>`

### 请求示例

```shell
curl --location 'https://api.modelverse.cn/v1/tasks/status?task_id=<task_id>' \
--header 'Authorization: <YOUR_API_KEY>'
```

### 输出

| 参数                 | 类型    | 描述                                              |
| :------------------- | :------ | :------------------------------------------------ |
| output.task_id       | string  | 异步任务的唯一标识                                |
| output.task_status   | string  | 任务状态：`Pending`、`Running`、`Success`、`Failure` |
| output.urls          | array   | 视频结果的 URL 列表                               |
| output.submit_time   | integer | 任务提交时间戳                                    |
| output.finish_time   | integer | 任务完成时间戳                                    |
| output.error_message | string  | 失败时返回的错误信息                              |
| usage.duration       | integer | 视频时长（秒）                                    |
| request_id           | string  | 请求的唯一标识                                    |

### 响应示例（成功）

```json
{
  "output": {
    "task_id": "task_id",
    "task_status": "Success",
    "urls": ["https://xxxxx/xxxx.mp4"],
    "submit_time": 1756959000,
    "finish_time": 1756959050
  },
  "usage": {
    "duration": 5
  },
  "request_id": ""
}
```

### 响应示例（失败）

```json
{
  "output": {
    "task_id": "task_id",
    "task_status": "Failure",
    "submit_time": 1756959000,
    "finish_time": 1756959019,
    "error_message": "error_message"
  },
  "usage": {
    "duration": 5
  },
  "request_id": ""
}
```
