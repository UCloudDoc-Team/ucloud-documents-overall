# Vidu/Img2Video

图生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                          | 类型   | 是否必选 | 描述                                                                                                                                                                                                                                                                                                    |
| :---------------------------- | :----- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| model                         | string | 是       | 模型名称，可选值：`viduq3-pro`、`viduq2-pro`、`viduq2-turbo`、`viduq2-pro-fast`<br> - viduq3-pro：支持音画同步，支持生成分镜视频<br> - viduq2-pro-fast：价格触底、效果好，生成速度较viduq2-turbo提高2-3倍<br> - viduq2-pro：新模型，情感表达强，动态细节丰富<br> - viduq2-turbo：新模型，效果好，生成快 |
| input.first_frame_url         | string | 是       | 首帧图片，支持图片 URL 或 Base64 编码                                                                                                                                                                                                                                                                   |
| input.prompt                  | string | 否       | 文本提示词，用于指导视频生成，最长 2000 字符。                                                                                                                                                                                                                                                          |
| parameters.vidu_type          | string | 是       | Vidu 接口类型，此处为 `img2video`                                                                                                                                                                                                                                                                       |
| parameters.duration           | int    | 否       | 视频时长<br> - viduq3-pro 默认为 5，可选：1 - 16<br> - viduq2-pro/viduq2-turbo/viduq2-pro-fast 默认为 5，可选：1-10                                                                                                                                                                                     |
| parameters.seed               | int    | 否       | 随机种子，默认 0 表示使用随机数                                                                                                                                                                                                                                                                         |
| parameters.resolution         | string | 否       | 分辨率<br> - viduq3-pro 1-16秒：默认 720p，可选：360p、540p、720p、1080p、2K<br> - viduq2-pro-fast/viduq2-pro/viduq2-turbo 1-10秒：默认 720p，可选：360p、540p、720p、1080p （其中Pro支持540p，fast不支持360p/540p）                                                                                    |
| parameters.movement_amplitude | string | 否       | 运动幅度，可选值：`auto`、`small`、`medium`、`large`，默认 `auto`<br> **注：q2、q3模型该参数不生效**                                                                                                                                                                                                    |
| parameters.bgm                | bool   | 否       | 是否添加背景音乐，默认 `false`<br> **注：q3模型该参数不生效**                                                                                                                                                                                                                                           |
| parameters.audio              | bool   | 否       | 是否使用音视频直出能力，默认为false，枚举值为：<br> - false：不需要音视频直出，输出静音视频 <br> - true：需要音视频直出，输出带台词以及背景音的视频 <br> 注1：该参数为true时，voice_id参数才生效<br> **注2：当model 为q3 时，该参数默认值为true，且不可关闭**                                           |
| parameters.voice_id           | string | 否       | 音色id <br> 用来决定视频中的声音音色，为空时系统会自动推荐，可选枚举值参考列表：[新音色列表](https://shengshu.feishu.cn/sheets/EgFvs6DShhiEBStmjzccr5gonOg)<br> **注：q3模型该参数不生效**                                                                                                              |

**注意事项：**
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
    "model": "viduq3-pro",
    "input": {
      "first_frame_url": "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/image2video.png",
      "prompt": "make it dance."
    },
    "parameters": {
      "vidu_type": "img2video",
      "duration": 5,
      "resolution": "1080p",
      "movement_amplitude": "auto",
      "audio": true
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
