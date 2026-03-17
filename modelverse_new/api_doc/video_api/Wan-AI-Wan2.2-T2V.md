# Wan-AI/Wan2.2-T2V

文生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                  | 类型   | 是否必选 | 描述                                                                                                           |
| :-------------------- | :----- | :------- | :------------------------------------------------------------------------------------------------------------- |
| model                 | string | 是       | 模型名称，此处为 `Wan-AI/Wan2.2-T2V`                                                                           |
| input.prompt          | string | 是       | 提示词，用于生成视频的内容描述                                                                                 |
| input.negative_prompt | string | 否       | 反向提示词，用于限制不希望出现的内容                                                                           |
| parameters.size       | string | 否       | 输出尺寸，分辨率选择 480P 时，size 支持`832x480, 480x832`<br>分辨率选择 720P 时，size 支持`1280x720, 720x1280` |
| parameters.resolution | string | 否       | 生成视频的分辨率档位，当前仅支持`720P`、`480P`                                                                 |
| parameters.duration   | int    | 否       | 视频生成时长（秒），支持`5` `8`                                                                                |
| parameters.seed       | int    | 否       | 随机数种子，范围`[0, 2147483647]`                                                                              |

### 请求示例
⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。
```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "Wan-AI/Wan2.2-T2V",
    "input": {
      "prompt": "a beautiful flower",
      "negative_prompt": "low quality"
    },
    "parameters": {
      "resolution": "720P",
      "seed": 12345
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
--header 'Authorization: <YOUR_API_KEY>' \
```

### 输出

| 参数                 | 类型    | 描述                                              |
| :------------------- | :------ | :------------------------------------------------ |
| output.task_id       | string  | 异步任务的唯一标识                                |
| output.task_status   | string  | 任务状态：`Pending`,`Running`,`Success`,`Failure` |
| output.urls          | array   | 视频结果的 URL 列表                               |
| output.submit_time   | integer | 任务提交时间戳                                    |
| output.finish_time   | integer | 任务完成时间戳                                    |
| output.error_message | string  | 失败时返回的错误信息                              |
| usage.duration       | integer | 任务执行时长（秒）                                |
| request_id           | string  | 请求的唯一标识                                    |

### 响应示例（成功）

```json
{
  "output": {
    "task_id": "task_id",
    "task_status": "Success",
    "urls": ["https://xxxxx/xxxx.mp4"],
    "submit_time": 1756958375,
    "finish_time": 1756958428
  },
  "usage": {
    "duration": 5
  },
  "request_id": "request_id"
}
```

### 响应示例（失败）

```json
{
  "output": {
    "task_id": "task_id",
    "task_status": "Failure",
    "submit_time": 1756958375,
    "finish_time": 1756958380,
    "error_message": "error_message"
  },
  "usage": {
    "duration": 5
  },
  "request_id": ""
}
```
