# MiniMax/Hailuo-2.3-T2V

文生视频模型

## 异步提交任务

### 接口

`https://api.modelverse.cn/v1/tasks/submit`

### 输入

| 参数                          | 类型    | 是否必选 | 描述                                                                                                                                    |
| :---------------------------- | :------ | :------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| model                         | string  | 是       | 模型名称，此处为 `MiniMax-Hailuo-2.3`                                                                                                   |
| input.prompt                  | string  | 是       | 视频文本描述，最大长度 2000 字符<br>支持运镜指令，详见「运镜控制说明」                                                                  |
| parameters.duration           | int     | 否       | 视频时长（秒），与模型和分辨率相关，详见「时长与分辨率对应关系」，默认 `6`                                                               |
| parameters.resolution         | string  | 否       | 视频分辨率，与模型和时长相关，详见「时长与分辨率对应关系」                                                                              |
| parameters.prompt_optimizer   | boolean | 否       | 是否自动优化文本描述，默认 `true`                                                                                                       |
| parameters.fast_pretreatment | boolean | 否       | 是否缩短文本优化耗时（仅对 MiniMax-Hailuo-2.3 生效），默认 `false`                          |
| parameters.aigc_watermark     | boolean | 否       | 是否在视频中添加水印，默认 `false`                                                                                                      |

### 运镜控制说明

MiniMax-Hailuo-2.3 系列模型支持运镜指令，可在 `input.prompt` 中使用以下运镜指令：

#### 支持的运镜指令（共15种）

| 类别   | 指令           |
| :----- | :------------- |
| 左右移 | [左移]、[右移] |
| 左右摇 | [左摇]、[右摇] |
| 推拉   | [推进]、[拉远] |
| 升降   | [上升]、[下降] |
| 上下摇 | [上摇]、[下摇] |
| 变焦   | [变焦推近]、[变焦拉远] |
| 其他   | [晃动]、[跟随]、[固定] |

#### 运镜使用规则

1. **组合运镜**：同一组 `[]` 内可添加多个指令（建议不超过3个），同时生效。示例：`"prompt": "一只猫在草地上跑[左摇,上升]"`
2. **顺序运镜**：prompt 中前后指令依次生效。示例：`"prompt": "一只猫在草地上跑[推进], 然后[拉远]"`
3. **自然语言支持**：也可通过自然语言描述运镜，但使用标准指令效果更精准

### 时长与分辨率对应关系

#### 1. 不同模型支持的时长（秒）

| 模型                    | 720P 分辨率 | 768P 分辨率 | 1080P 分辨率 |
| :---------------------- | :---------- | :---------- | :------------ |
| MiniMax-Hailuo-2.3     | -           | 6、10       | 6             |

#### 2. 不同模型支持的分辨率

| 模型                    | 6秒时长              | 10秒时长        |
| :---------------------- | :------------------- | :-------------- |
| MiniMax-Hailuo-2.3     | 768P（默认）、1080P  | 768P（默认）    |

### 请求示例

⚠️ 如果您使用 Windows 系统，建议使用 Postman 或其他 API 调用工具。

```shell
curl --location --globoff 'https://api.modelverse.cn/v1/tasks/submit' \
--header 'Authorization: <YOUR_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "MiniMax-Hailuo-2.3",
    "input": {
      "prompt": "A beautiful sunset over the ocean with waves gently crashing on the shore. [推进, 跟随]"
    },
    "parameters": {
      "duration": 6,
      "resolution": "1080P",
      "prompt_optimizer": true,
      "fast_pretreatment": false,
      "aigc_watermark": false
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
    "task_id": "106916112212032"
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
    "task_id": "176843862716480",
    "task_status": "Success",
    "urls": ["https://xxxxx/xxxx.mp4"],
    "submit_time": 1756959000,
    "finish_time": 1756959050
  },
  "usage": {
    "duration": 6
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
    "duration": 6
  },
  "request_id": ""
}
```

