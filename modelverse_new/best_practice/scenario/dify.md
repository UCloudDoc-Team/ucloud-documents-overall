# 在Dify中使用ModelVerse API  
## 关于Dify
Dify 是一款开源的大语言模型(LLM) 应用开发平台。它融合了后端即服务（Backend as Service）和 LLMOps 的理念，使开发者可以快速搭建生产级的生成式 AI 应用。

## 在Dify中使用LLM API
### 第一步：[获取 API Key](https://console.compshare.cn/light-gpu/api-keys)

### 使用方式一：通过Dify插件市场安装
1. 登录Dify，进入Dify插件市场 https://cloud.dify.ai/plugins?category=discover

2. 搜索**UCloud**，找到对应插件并安装

![dify](https://static.ucloud.cn/docs/modelverse/images/dify/market.png)

3. 输入UCloud模型API Key

![dify](https://static.ucloud.cn/docs/modelverse/images/dify/api.png)

4. 接入完成

![dify](https://static.ucloud.cn/docs/modelverse/images/dify/complete.png)

## 在Dify中实现文生图
### 第一步：下载工作流模版，浏览器输入如下地址即可下载
```
https://docs.ucloud.cn/modelverse/best_practice/scenario/ucloud-image-template.yml
```
在Dify的工作室中单击**导入DSL文件**并选择下载好的模板文件

### 第二步：配置API Key
在**请求设置**模块中将Authorization的值替换成您的API Key。

![dify](https://static.ucloud.cn/docs/modelverse/images/dify/request_set.png)

### 第三步：运行测试
1.单击**测试运行**按钮并在提示词中输入您想要生成的图片内容，以“一只狗”为例，可以生成图片：

![dify](https://static.ucloud.cn/docs/modelverse/images/dify/result_dog.png)

2.您也可以在模型选择中测试不同UCloud支持的文生图模型

![dify](https://static.ucloud.cn/docs/modelverse/images/dify/select_model.png)




