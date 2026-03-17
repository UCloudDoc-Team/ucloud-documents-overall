# Wan-AI/Wan2.6-T2V

文生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                     | 类型   | 是否必选 | 描述                                                                                                                                                                                                                                |
| :----------------------- | :----- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                    | string | 是       | 模型名称，此处为 `Wan-AI/Wan2.6-T2V`                                                                                                                                                                                                |
| input.prompt             | string | 是       | 提示词，用于指导视频生成                                                                                                                                                                                                            |
| input.negative_prompt    | string | 否       | 反向提示词，用于限制不希望出现的内容                                                                                                                                                                                                |
| input.audio_url          | string | 否       | 频 URL，用于指导生成。如果音频时长超过指定的视频时长，将被截断；如果短于视频时长，视频后半部分将无声。可选                                                                                                                                                                                                    |
| parameters.size          | string | 是       | 生成视频的尺寸。 <br>可选的视频分辨率及其对应的视频宽高比为： <br>720P档位：<br>- 1280x720：16:9<br>- 720x1280：9:16 <br>1080P档位：<br>- 1920x1080： 16:9<br>- 1080x1920： 9:16 。|
| parameters.duration      | int    | 否       | 视频生成时长（秒），可选值 `5` 或 `10` 或 `15`，默认为 `5`                                                                                         
| parameters.seed          | int    | 否       | 随机数种子，范围`[0, 2147483647]`                                                                                                 |
| parameters.prompt_extend | boolean | 否       | 是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。默认值：`true`。示例值：`true` |
| parameters.shot_type   | string | 否       | 指定生成视频的镜头类型，即视频是由一个连续镜头还是多个切换镜头组成。生效条件：仅当 `prompt_extend` 为 `true` 时生效。参数优先级：`shot_type` > `prompt`。例如，若 `shot_type` 设置为 `single`，即使 `prompt` 中包含"生成多镜头视频"，模型仍会输出单镜头视频。可选值：`single`（默认值，输出单镜头视频）、`multi`（输出多镜头视频）。示例值：`single` |

### 请求示例
⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。
```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "Wan-AI/Wan2.6-T2V",
    "input": {
      "prompt": "A beautiful girl is dancing",
      "audio_url": "https://example.com/audio.mp3"
    },
    "parameters": {
      "size": "1280x720",
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