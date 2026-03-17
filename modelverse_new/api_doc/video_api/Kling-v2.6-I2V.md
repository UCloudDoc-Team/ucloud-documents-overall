# Kling/v2.6-I2V

图生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                      | 类型   | 是否必选 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|:------------------------| :----- | :------- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| model                   | string | 是       | 模型名称，此处为 `kling-v2-6`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| input.prompt            | string | 是       | 提示词，用于指导视频生成                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| input.negative_prompt   | string | 否       | 反向提示词，用于限制不希望出现的内容                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| parameters.mode         | string | 否       | 生成模式，可选值：`std`、`pro`，默认为 `pro`   目前只支持`pro`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| parameters.aspect_ratio | string | 否       | 视频长宽比，可选值：`16:9`、`9:16`、`1:1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| parameters.duration     | int    | 否       | 视频时长（秒），可选值：`5`、`10`，默认为 `5`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| parameters.image        | string | 是       | 参考图像 <br>支持传入图片Base64编码或图片URL（确保可访问）<br>请注意，若您使用base64的方式，请确保您传递的所有图像数据参数均采用Base64编码格式。在提交数据时，请不要在Base64编码字符串前添加任何前缀，例如data:image/png;base64,。正确的参数格式应该直接是Base64编码后的字符串。<br>示例：<br>正确的Base64编码参数：<br><br> iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==<br><br>错误的Base64编码参数（包含data:前缀）：<br><br> data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==<br><br>请仅提供Base64编码的字符串部分，以便系统能够正确处理和解析您的数据<br>- 图片格式支持.jpg / .jpeg / .png<br>- 图片文件大小不能超过10MB，图片宽高尺寸不小于300px，图片宽高比介于1:2.5 ~ 2.5:1之间<br>- image 参数与 image_tail 参数至少二选一，二者不能同时为空 |
| parameters.image_tail   | string | 否       | 视频尾帧图片 URL，支持 URL 或 Base64 编码。具体要求参照 parameters.image                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

**注意**：
- v2.6 不支持有声视频（包含音色 `voice_list`、`sound` 参数），如需支持请联系技术支持。

### 请求示例

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "kling-v2-6",
    "input": {
      "prompt": "The image comes to life with gentle movement"
    },
    "parameters": {
      "mode": "pro",
      "aspect_ratio": "16:9",
      "duration": 5,
      "image": "https://example.com/first_frame.jpg"
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
