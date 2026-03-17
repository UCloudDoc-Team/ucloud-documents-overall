# doubao-seedance-1-5-pro

文图生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                               | 类型    | 是否必选 | 描述                                                                                                     |
| :--------------------------------- | :------ | :------- | :------------------------------------------------------------------------------------------------------- |
| model                              | string  | 是       | 模型名称，此处为 `doubao-seedance-1-5-pro-251215`                                                                     |
| input.content              | object[]  | 是       | 输入给模型生成视频的信息对象，支持三种对象类型：<br>  `文本信息`<br>  `图片信息`<br>  `样片信息`<br>参考下方content介绍。                                                                     |  |
| parameters.execution_expires_after              | int  | 否       | 任务超时阈值。指定任务提交后的过期时间（单位：秒），默认值 `172800` 秒，即 `48` 小时。取值范围：`[3600，259200]`。                                                                                         |
| parameters.generate_audio                    | boolean  | 否       | 控制生成的视频是否包含与画面同步的声音，默认`false`。<br>`true`：模型输出的视频包含同步音频。<br>`false`：模型输出的视频为无声视频。 |
| parameters.draft                       | boolean  | 否       |  控制是否开启样片模式，默认`false`。<br>`true`：开启样片模式，生成一段预览视频，快速验证场景结构、镜头调度、主体动作与 prompt 意图是否符合预期。消耗 token 数较正常视频更少，使用成本更低。<br>`false`：关闭样片模式，正常生成一段视频。                                                                                 |
| parameters.resolution              | string  | 否       | 视频分辨率，默认`720p`<br>分辨率：支持`480p`、`720p`，`1080p`。<br>样片模式只支持480p。                                                                  |
| parameters.ratio              | string  | 否       | 生成视频的宽高比例，支持：`16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`21:9`、`adaptive`。默认是`adaptive`，智能选择最合适的宽高比。                                                                  |
| parameters.duration                | int     | 否       | 生成视频时长（秒）：`4~12` 秒，默认为 `5`                                                       |
| parameters.seed                    | int     | 否       | 随机数种子，范围`[0, 2147483647] `                                                           |
| parameters.camera_fixed                    | boolean     | 否       | 是否固定摄像头，默认`false`。<br>`true`：固定摄像头。<br>`false`：不固定摄像头。`                                                           |
| parameters.watermark                    | boolean     | 否       | 生成视频是否包含水印，默认`false`。<br>`false`：不含水印。<br>`true`：含有水印。                                                           |
| parameters.service_tier                    | string     | 否       | 指定处理本次请求的服务等级类型，默认default。<br>`default`：在线推理模式，适合对推理时效性要求较高的场景。<br>`flex`：离线推理模式，适合对推理时延要求不高的场景。                                                           |

#### 输入input.content对象介绍
样片信息对象是通过样片生成视频，不支持与文本信息，图片信息对象混用。
#### 文本信息对象
| 参数                               | 类型    | 是否必选 | 描述                                                                                                     |
| :--------------------------------- | :------ | :------- | :------------------------------------------------------------------------------------------------------- |
| content.type                              | string  | 是       | 输入内容的类型，此处应为 `text`。                                                                     |
| content.text              | string  | 是       | 输入给模型的文本内容，描述期望生成的视频，支持中英文。建议不超过500字。                                                                     |  

#### 图片信息对象
| 参数                               | 类型    | 是否必选 | 描述                                                                                                     |
| :--------------------------------- | :------ | :------- | :------------------------------------------------------------------------------------------------------- |
| content.type                              | string  | 是       | 输入内容的类型，此处应为 `image_url`。支持图片URL或图片 Base64 编码。                                                                     |
| content.image_url              | object  | 是       | 输入给模型的图片对象。                                                                     |  
| content.image_url.url              | string  | 是       | 图片信息，可以是图片URL或图片Base64编码。<br>图片URL：请确保图片URL可被访问。<br>Base64编码：请遵循此格式data:image/<图片格式>;base64,<Base64编码>，注意 <图片格式> 需小写，如 data:image/png;base64,{base64_image}。                                                                     |  
| content.role             | string  | 否       | 图片的位置或用途。<br>1个image_url对象，字段role可不填，或字段role为：`first_frame`。<br>2个image_url对象时，字段role必填。<br>首帧图片对应的字段role为：`first_frame`。<br>尾帧图片对应的字段role为：`last_frame`。                                                                     |  

#### 样片信息对象
| 参数                               | 类型    | 是否必选 | 描述                                                                                                     |
| :--------------------------------- | :------ | :------- | :------------------------------------------------------------------------------------------------------- |
| content.type                              | string  | 是       | 输入内容的类型，此处应为 `draft_task`。                                                                     |
| content.draft_task              | object  | 是       | 输入给模型的样片任务。                                                                     |  
| content.draft_task.id              | string  | 是       | 样片任务 ID。                                                                     |  

### 请求示例
⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。
```shell
curl -v 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "doubao-seedance-1-5-pro-251215",
    "input": {
        "content": [
        {
            "type": "text",
            "text": "让他跑起来。"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg"
            },
            "role": "first_frame"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://umodelverse-inference.cn-wlcb.ufileos.com/ucloud-maxcot.jpg"
            },
            "role": "last_frame"
        }
      ]
    },
    "parameters": {
      "generate_audio": true,
      "duration": 5,
      "execution_expires_after": 3600,
      "generate_audio": true,
      "resolution": "720p",
      "camera_fixed": false,
      "watermark": false,
      "draft": false
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
| output.task_status   | string  | 任务状态：`Pending`,`Running`,`Success`,`Failure`,`Expired` |
| output.urls          | array   | 视频结果的 URL 列表                               |
| output.submit_time   | integer | 任务提交时间戳                                    |
| output.finish_time   | integer | 任务完成时间戳                                    |
| output.error_message | string  | 失败时返回的错误信息                              |
| usage.duration       | integer | 视频时长（秒）                                |
| usage.completion_tokens       | integer | 模型输出视频花费的 token 数量                                |
| usage.total_tokens       | integer | 本次请求消耗的总 token 数量。视频生成模型不统计输入 token，输入 token 为 0，故 total_tokens=completion_tokens。                                |
| request_id           | string  | 请求的唯一标识                                    |

### 响应示例（成功）

```json
{
	"output": {
		"task_id": "xxxxxxx",
		"task_status": "Success",
		"urls": ["http://xxxxxxxx/xx.mp4"],
		"submit_time": 1768460826,
		"finish_time": 1768460932
	},
	"usage": {
		"completion_tokens": 108900,
		"total_tokens": 108900,
		"duration": 5
	},
	"request_id": ""
}
```

### 响应示例（失败）

```json
{
  "output": {
    "task_id": "xxxxxxx",
    "task_status": "Failure",
    "submit_time": 1756959000,
    "finish_time": 1756959019,
    "error_message": "error_message"
  },
  "usage": {
  	"completion_tokens": 0,
		"total_tokens": 0,
    "duration": 5
  },
  "request_id": ""
}

```

