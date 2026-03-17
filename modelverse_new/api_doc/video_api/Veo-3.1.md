# Veo-3.1

文图生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                  | 类型   | 是否必选 | 描述                                           |
| :-------------------- | :----- | :------- | :--------------------------------------------- |
| model                 | string | 是       | 模型名称，此处为 `veo-3.1-generate-001`或`veo-3.1-fast-generate-001`         |
| input.prompt          | string | 是       | 提示词，用于指导视频生成                       |
| input.negative_prompt | string | 否       | 反向提示词，用于限制不希望出现的内容           |
| input.image           | object | 否       | 用于指导视频生成的图片对象，如果请求包含`last_frame`对象，则image为首帧对象 |
| input.image.bytesBase64Encoded | string | 否       | 图片的字节 `base64` 编码字符串。纯 base64 编码数据，不能包含 `data:image/jpeg;base64`, 这个前缀。           |
| input.image.mimeType | string | 否       | 图片的 MIME 类型，只接受以下 MIME 类型：<br> `image/jpeg` <br> `image/png` <br> `image/webp`           |
| input.last_frame           | object | 否       | 用于指导视频生成的尾帧图片对象 |
| input.last_frame.bytesBase64Encoded | string | 否       | 图片的字节 `base64` 编码字符串。纯 base64 编码数据，不能包含 `data:image/jpeg;base64`, 这个前缀。           |
| input.last_frame.mimeType | string | 否       | 图片的 MIME 类型，只接受以下 MIME 类型：<br> `image/jpeg` <br> `image/png` <br> `image/webp`           |
| parameters.resolution | string | 否       | 所生成视频的分辨率。可接受的值为 `720p`（默认值）或 `1080p`。 |
| parameters.duration   | int    | 否       | 视频生成时长（秒），支持`4`、`6` 或 `8`。默认为 `8`。               |
| parameters.aspect_ratio       | int    | 否       | 指定所生成视频的宽高比。接受的值如下：<br> `16:9` <br>`9:16` <br>默认值为 `16:9`。|
| parameters.generate_audio       | bool    | 是       | 必选参数，为视频生成音频。接受的值包括 `true` 或 `false`。              |
| parameters.person_generation       | string    | 否       | 用于控制是否允许人物或人脸生成的安全设置。以下项之一：<br>`allow_adult`（默认值）：仅允许生成成人<br>`dont_allow`：禁止在图片中包含人物/人脸。              |

### 请求示例
⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。
```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "veo-3.1-generate-001",
    "input": {
      "prompt": "make it run",
      "image" : {
        "bytesBase64Encoded": "xxxxx",
        "mimeType": "image/jpeg"
      },
      "last_frame" : {
        "bytesBase64Encoded": "xxxxx",
        "mimeType": "image/jpeg"
      }
    },
    "parameters": {
      "duration": 6,
      "aspect_ratio": "16:9",
      "resolution": "1080p",
      "generate_audio": true
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
| output.urls          | array   | 视频结果的 URL 列表，默认保留24小时，请及时下载。                               |
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
