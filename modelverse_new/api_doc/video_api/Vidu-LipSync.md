# Vidu/LipSync

对口型视频生成模型，支持音频驱动和文字驱动两种方式。

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                 | 类型   | 是否必选 | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| :------------------- | :----- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                | string | 是       | 模型名称，请固定填写：`vidu-lip-sync`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| input.video_url      | string | 是       | 原视频 URL（需要确保可访问），模型将以此视频为画面来匹配口型。<br><br>**格式要求**：仅支持 mp4、mov、avi<br>**时长要求**：1-600 秒，建议时长 10-120 秒<br>**大小要求**：不超过 5GB<br>**分辨率要求**：单边像素需在 360p-4096p 之间<br>**编码要求**：视频编码格式需为 H.264，若不是请参见 [编码格式转换](https://shengshu.feishu.cn/docx/FIQHdcreYoCYX6x4kORckwmWnjf)<br>**内容要求**：视频内容需免涉肖像权，否则会被下架或销毁<br>**视频素材规范**：<br>&nbsp;&nbsp;- **人脸画面**：要求真人出镜（如果是卡通人物，需要人物五官和真人比例相近），画面中的人脸说话时建议正对镜头，水平转动不超过 45 度，俯仰不超过 15 度；人脸尽量不遮挡，面部光线稳定<br>&nbsp;&nbsp;- **说话音频**：对音频无限制 |
| input.audio_url      | string | 否       | 音频文件 URL（与 text 二选一），对口型视频中使用的文字、音色以音频文件内容为准。<br><br>**格式要求**：支持 wav、mp3、wma、m4a、aac、ogg<br>**时长要求**：大于 1 秒，小于 600 秒<br>**大小要求**：不超过 100MB                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| input.text           | string | 否       | 文本内容（与 audio_url 二选一），对口型视频生成时使用的文本内容。<br><br>**字符要求**：不少于 4 个字符，不超过 2000 字符（2-1000 个汉字或 4-2000 个英文）<br>**优先级**：与 audio_url 同时有值时，以 audio_url 中的内容生成<br>**段落切换**：用换行符标记<br>**停顿控制**：支持自定义文本之间的语音时间间隔，使用 `<#x#>` 标记：<br>&nbsp;&nbsp;- x 为停顿时长（单位：秒），范围 [0.01, 99.99]，最多保留两位小数<br>&nbsp;&nbsp;- 文本间隔时间需设置在两个可以语音发音的文本之间，不可连续使用多个停顿标记<br>&nbsp;&nbsp;- **示例**：`你好<#2#>我是modelverse<#2#>很高兴见到你`                                                                                                                 |
| input.ref_photo_url  | string | 否       | 人脸参考图 URL，用于在视频包含多张人脸时指定目标人物。<br><br>**格式要求**：支持 jpg、jpeg、png、bmp、webp<br>**分辨率要求**：单边分辨率在 192-4096px<br>**大小要求**：不超过 10MB<br>**内容要求**：图片需包含一张清晰的人物正脸，且为视频中出现的人物<br>**默认行为**：若不输入人脸参考图，默认选择视频中第一个有人脸的画面中人脸占比最大的人物为目标                                                                                                                                                                                                                                                                                                                                           |
| parameters.vidu_type | string | 是       | Vidu 接口类型，此处为 `lip-sync`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| parameters.speed     | float  | 否       | 语速，默认 1.0，范围 [0.5, 2]。0.5 为最慢语速，2 为最快语速。<br>仅文字驱动时生效                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| parameters.voice_id  | string | 否       | 音色 ID，仅文字驱动时生效。参考 [音色列表](https://shengshu.feishu.cn/sheets/EgFvs6DShhiEBStmjzccr5gonOg)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| parameters.volume    | int    | 否       | 音量大小，范围 0-10，默认 0（正常音量），值越大音量越高。<br>仅文字驱动时生效                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

**注意事项：**

- `audio_url` 和 `text` 必须提供其中一个
- `speed`、`voice_id`、`volume` 参数仅在使用文字驱动时生效

### 请求示例（音频驱动）

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "vidu-lip-sync",
    "input": {
      "video_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/maxcot-dance.mp4",
      "audio_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/%E6%AC%A2%E8%BF%8E%E4%BD%BF%E7%94%A8Modelverse_API.mp3"
    },
    "parameters": {
      "vidu_type": "lip-sync"
    }
  }'
```

### 请求示例（文字驱动）

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "vidu-lip-sync",
    "input": {
      "video_url": "https://umodelverse-inference.cn-wlcb.ufileos.com/maxcot-dance.mp4",
      "text": "你好，欢迎使用对口型功能"
    },
    "parameters": {
      "vidu_type": "lip-sync",
      "voice_id": "your_voice_id",
      "speed": 1.0,
      "volume": 4
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
    "urls": ["https://xxxxx/xxxx-lipsync.mp4"],
    "submit_time": 1756959000,
    "finish_time": 1756959050
  },
  "usage": {
    "duration": 30
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