# Vidu/视频延长

视频延长 Extend 接口描述

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                  | 类型   | 是否必选 | 描述                                                     |
| :-------------------- | :----- | :------- | :------------------------------------------------------- |
| model                 | string | 是       | 模型名称，可选值：`viduq2-turbo`、`viduq2-pro`           |
| input.video_url       | string | 否       | 视频 URL。传入的视频时长不能低于 4 秒，不能超过 1 分钟   |
| input.last_frame_url  | string | 否       | 延长到尾帧的参考图像，支持图片 URL 或 Base64 编码        |
| input.prompt          | string | 否       | 延长提示词，用来控制延长的视频内容                       |
| parameters.vidu_type  | string | 是       | Vidu 接口类型，此处应为 `extend` 视频延长                |
| parameters.duration   | int    | 否       | 延长时长（秒），可选值 1-7，默认 5                       |
| parameters.resolution | string | 否       | 视频分辨率，可选值：`540p`、`720p`、`1080p`，默认 `720p` |

**注意事项：**
- `video_url`
  -  需要延长的视频链接必须提供，需要公网访问
-  `last_frame_url` 参数
   - 支持传入图片 Base64 编码或图片URL（确保可访问）；
   - 参考图片支持 png、jpeg、jpg、webp 格式
   - 图片比例需要小于 1:4 或者 4:1
   - 图片大小不超过 50 MB
   - 请注意，base64 decode之后的字节长度需要小于10M，且编码必须包含适当的内容类型字符串，例如：`data:image/png;base64,{base64_encode}`

### 请求示例（使用 video_url）

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "viduq2-turbo",
    "input": {
      "video_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/maxcot-dance.mp4",
      "last_frame_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg",
      "prompt": "Continue the video with smooth camera movement"
    },
    "parameters": {
      "vidu_type": "extend",
      "duration": 5,
      "resolution": "720p"
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
| usage.duration       | integer | 延长的视频时长（秒）                              |
| request_id           | string  | 请求的唯一标识                                    |

### 响应示例（成功）

```json
{
  "output": {
    "task_id": "task_id",
    "task_status": "Success",
    "urls": ["https://xxxxx/xxxx-extended.mp4"],
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
