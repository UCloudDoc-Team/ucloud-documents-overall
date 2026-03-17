# 在 Open WebUI 中使用 ModelVerse API

## 关于 Open WebUI

Open WebUI (https://github.com/open-webui/) 是一款适合企业内部部署的网页用户界面。

它会在您的计算机上启动一个本地服务，生成一个内部网络网址，企业内部的员工都可以通过该网址访问。Open WebUI 功能非常完善，支持多用户管理、函数调用、RAG (Retrieval-Augmented Generation) 和联网搜索等功能。

## 配置步骤

按照以下步骤，您可以在 Open WebUI 中配置并使用 ModelVerse 提供的 API 服务。

### 第一步：获取 API Key

首先，您需要 [点击这里获取您的 API Key](https://console.ucloud.cn/modelverse/experience/api-keys)。

### 第二步：配置 Open WebUI

1.  登录 Open WebUI，点击左下角的用户头像，然后选择「设置」。
    ![进入设置](https://static.ucloud.cn/docs/modelverse/images/openwebui/settings.png)

2.  在设置菜单中，点击「管理员设置」。
    ![管理员设置](https://static.ucloud.cn/docs/modelverse/images/openwebui/admin.png)

3.  在管理员设置页面，点击「外部连接」，然后点击「+」号按钮以添加新的外部模型服务。
    ![外部链接](https://static.ucloud.cn/docs/modelverse/images/openwebui/external_connection.png)

4.  在弹出的表单中，填入以下信息：
    *   **Base URL**: `https://api.modelverse.cn/v1`
    *   **API Key**: 粘贴您在第一步获取的 API Key

    填写完毕后，Open WebUI 会自动获取可用的模型。
    ![添加UCloud ModelVerse服务](https://static.ucloud.cn/docs/modelverse/images/openwebui/add_ucloud.png)

### 第三步：开始聊天

配置完成后，您就可以在模型选择列表中看到来自 ModelVerse 的模型，选择任意一个即可开始聊天。

![开始聊天](https://www-s.ucloud.cn/2025/02/c9174bd62ee33d00587935ba2e070da0_1739964081012.png)
