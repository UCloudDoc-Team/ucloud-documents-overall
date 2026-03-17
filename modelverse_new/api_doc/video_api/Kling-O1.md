# Kling/O1

全视频生成模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                          | 类型   | 是否必选 | 描述                                                                                                                                                                                                                                                                                                          |
| :---------------------------- | :----- | :------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| model                         | string | 是       | 模型名称，此处为 `kling-video-o1`                                                                                                                                                                                                                                                                                   |
| input.prompt                  | string | 是       | 提示词，用于指导视频生成                                                                                                                                                                                                                                                                                                |
| parameters.mode               | string | 否       | 生成模式，可选值：`std`、`pro`，默认为 `pro` 目前只支持`pro`                                                                                                                                                                                                                                                                   |
| parameters.aspect_ratio       | string | 否       | 视频长宽比，可选值：`16:9`、`9:16`、`1:1`                                                                                                                                                                                                                                                                               |
| parameters.duration           | int    | 否       | 视频时长（秒），可选值：`3`、`4`、`5`、`6`、`7`、`8`、`9`、`10`，默认为 `5` <br>   使用文生视频、首帧图生视频时，仅支持5和10s<br>使用视频编辑功能（“refer_type”:“base”）时，输出结果与传入视频时长相同，此时当前参数无效；此时，按输入视频时长四舍五入取整计量计费                                                                                                                                           |
| parameters.image_list         | array  | 否       | 图片列表，用于指定视频的首帧或尾帧。每个图片项包含：<br>- `image_url`：图片 URL 或 Base64 编码<br>- `type`：图片类型，可选值：`first_frame`（首帧）、`end_frame`（尾帧）                                                                                                                                                                                       |
| parameters.video_list         | array  | 否       | 视频列表，用于视频参考或编辑。每个视频项包含：<br>- `video_url`：视频 URL<br>- `refer_type`：参考类型，可选值：`feature`（特征参考）、`base`（待编辑）<br>- `keep_original_sound`：是否保留原音，可选值：`yes`、`no`                                                                                                                                                     |
| parameters.element_list         | array  | 否       | 主体参考列表 <br>- 基于主体库中主体的ID配置，用key:value承载，如下：<br>"element_list":[<br>{<br>"element_id":long<br>}<br>]<br>- 参考主体数量与有无参考视频、参考图片数量有关，其中：<br>- 有参考视频时，参考图片数量和参考主体数量之和不得超过4；<br>- 无参考视频时，参考图片数量和参考主体数量之和不得超过7                                                                                                      |

**注意**：
- O1 模型不支持自定义主体相关功能（`element_list` 参数），如需支持请联系技术支持。

### 请求示例

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "kling-video-o1",
    "input": {
      "prompt": "A beautiful sunset over the ocean with waves gently crashing"
    },
    "parameters": {
      "mode": "pro",
      "aspect_ratio": "16:9",
      "duration": 5,
      "image_list": [
        {
          "image_url": "https://example.com/first_frame.jpg",
          "type": "first_frame"
        }
      ]
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
