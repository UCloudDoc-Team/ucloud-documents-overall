# Vidu/首尾帧生视频

vidu 首尾帧生成视频 接口文档

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                          | 类型   | 是否必选 | 描述                                                                                                                                                                 |
| :---------------------------- | :----- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                         | string | 是       | 模型名称，可选值：`viduq2-pro`、`viduq2-turbo`、`viduq2-pro-fast`  <br> - viduq2-pro：新模型，效果好，细节丰富 <br> - viduq2-turbo：新模型，效果好，生成快 <br> - viduq2-pro-fast：价格触底、效果稳定，生成速度较viduq2-turbo提高2-3倍                              |
| input.first_frame_url         | string | 是       | 首帧图片，支持图片 URL 或 Base64 编码                                                                                                                                |
| input.last_frame_url          | string | 是       | 尾帧图片，支持图片 URL 或 Base64 编码                                                                                                                                |
| input.prompt                  | string | 否       | 文本提示词，用于指导视频生成，最长 2000 字符。                                                                                                                       |
| parameters.vidu_type          | string | 是       | Vidu 接口类型，此处为 `start-end2video`                                                                                                                              |
| parameters.duration           | int    | 否       | 视频时长参数，默认值依据模型而定：<br> - viduq2-pro 默认为 5，可选：1、2、3、4、5、6、7、8  <br> - viduq2-turbo 默认为 5，可选：1、2、3、4、5、6、7、8 <br> - viduq2-pro-fast 默认为 5，可选：1、2、3、4、5、6、7、8               |
| parameters.seed               | int    | 否       | 随机种子，默认 0 表示使用随机数                                                                                                                                      |
| parameters.resolution         | string | 否       | 分辨率参数，默认值依据模型和视频时长而定： <br> - viduq2-pro 1-8秒：默认 720p，可选：540p、720p、1080p <br> - viduq2-turbo 1-8秒：默认 720p，可选：540p、720p、1080p <br> - viduq2-pro-fast 1-8秒：默认 720p，可选：720p、1080p |
| parameters.movement_amplitude | string | 否       | 运动幅度，可选值：`auto`、`small`、`medium`、`large`，默认 `auto`                                                                                                    |
| parameters.bgm                | bool   | 否       | 是否添加背景音乐，默认 `false`                                                                                                                                       |

**注意事项：**
- 必须同时提供 `first_frame_url` 和 `last_frame_url` 两个参数
- 首尾帧两张图的分辨率需相近，首帧分辨率/尾帧分辨率需在 0.8～1.25 之间
- 图片支持 png、jpeg、jpg、webp 格式
- 图片比例需要小于 1:4 或者 4:1
- 图片大小不超过 50 MB
- Base64 编码格式示例：`data:image/png;base64,{base64_encode}`

### 请求示例

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "viduq2-pro",
    "input": {
      "first_frame_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg",
      "last_frame_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg",
      "prompt": "Continue the video with smooth camera movement."
    },
    "parameters": {
      "vidu_type": "start-end2video",
      "duration": 5,
      "resolution": "1080p",
      "movement_amplitude": "auto",
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
