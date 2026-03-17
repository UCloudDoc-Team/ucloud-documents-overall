# Vidu/Text2Video

文生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                      | 类型    | 是否必选 | 描述                                                                                                 |
| :------------------------ | :------ | :------- | :--------------------------------------------------------------------------------------------------- |
| model                     | string  | 是       | 模型名称，可选值：`viduq2`                                                                           |
| input.prompt              | string  | 是       | 文本提示词，用于生成视频的描述，最长 2000 字符                                                       |
| parameters.vidu_type      | string  | 是       | Vidu 接口类型，此处为 `text2video`                                                                   |
| parameters.duration       | int     | 否       | 视频时长参数，默认值依据模型而定：<br> - viduq2 : 默认5秒，可选：1-10                                |
| parameters.seed           | int     | 否       | 随机种子，默认 0 表示使用随机数                                                                      |
| parameters.aspect_ratio   | string  | 否       | 长宽比，可选值：`16:9`、`9:16`、`3:4`、`4:3`、`1:1`，默认 `16:9`                                     |
| parameters.resolution     | string  | 否       | 分辨率参数，默认值依据模型和视频时长而定： <br> - viduq2(1-10秒)：默认 720p，可选：540p、720p、1080p |
| parameters.guidance_scale | float64 | 否       | 引导系数，控制生成结果与提示词的相关性                                                               |
| parameters.bgm            | bool    | 否       | 是否添加背景音乐，默认 `false`                                                                       |

### 请求示例

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "viduq2",
    "input": {
      "prompt": "In an ultra-realistic fashion photography style featuring light blue and pale amber tones, an astronaut in a spacesuit walks through the fog. The background consists of enchanting white and golden lights, creating a minimalist still life and an impressive panoramic scene."
    },
    "parameters": {
      "vidu_type": "text2video",
      "duration": 5,
      "aspect_ratio": "16:9",
      "resolution": "720p",
      "bgm": true
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
| output.task_status   | string  | 任务状态：`Pending`,`Running`,`Success`,`Failure` |
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
