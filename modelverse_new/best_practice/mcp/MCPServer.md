# 通过CLINE插件快速连接MCP服务（以MCP SQLITE为示例）

## 安装VSCODE

从官网 [https://code.visualstudio.com/下载vscode安装包进行安装。](https://code.visualstudio.com/)

## 安装CLINE

在vscode extension列表中找到CLINE并选择安装。

![image1](https://www-s.ucloud.cn/2025/04/a2f325d3afe05070ee59d10319d5e0f3_1744219330796.png)

## 配置CLINE使用UCloud QWQ API

### 1.点击VSCODE左侧的小机器人图标

![image2](https://www-s.ucloud.cn/2025/04/7476289be66d52f95188a9685ad96a2b_1744368546129.png)

### 2.首次使用会提示配置chatbot的api,如果之前使用过，可以点击CLINE的设置齿轮进行配置。

| 设置项                     | 描述                                                                 |
|---------------------------|---------------------------------------------------------------------|
| API Provider              | 选择 OpenAI Compatible                                              |
| Base url|  https://api.modelverse.cn/v1                                          |
|API key|  进入UModelVerse控制台-体验中心-Key页面获取                                          |
|Model ID | Qwen/QwQ-32B                                           |
| Model Configuration       | 由于 QWQ 是思维链模型，需要选择 **Enable R1 messages format**        |
| Context Window Size       | 限制为 40000                                                         |


![image3](https://www-s.ucloud.cn/2025/04/8fdd8534ac59221dda1debf068c4ba4b_1744219330789.png)

### 3.配置好后可以进行对话测试

看到回复表明配置成功。

![image](https://www-s.ucloud.cn/2025/04/8b3e8cd2ec7a1ac4524291d8fa54d53f_1744219330788.png)

## 安装UV 和SQLITE

Windows 用户在cmd中运行

```
winget install --id=astral-sh.uv -e
winget install sqlite.sqlite
```
 
Mac用户使用

```
brew install uv
brew install sqlite3
```
 
## 配置CLINE使用mcp-server-sqlite

点击小机器人图标打开CLINE

选择页面上方server的小图标

在MCP Servers中选择installed标签，下面会有Configure MCP Servers,点击打开Cline的MCP配置文件

![image](https://www-s.ucloud.cn/2025/04/44185ccda7bfdf90d52ef8fef4421077_1744219330785.png)

修改CLine MCP配置文件。

Windows修改参考：

```
{
  "mcpServers": {
    "sqlite_server" :{
        "command": "cmd.exe",
      "args": [
      "/c",
      "uvx",
      "mcp-server-sqlite",
      "--db-path",
      "D:\\tmp\\test.db"
    ]
    }
  }
}
```
 
Mac修改参考：

```
{
  "mcpServers": {
    "sqlite_server": {
      "command": "uvx",
      "args": [
        "mcp-server-sqlite",
        "--db-path",
        "/tmp/test.db"
      ]
    }
  }
}
```
 
其中："D:\\tmp\\test.db"和"/tmp/test.db"修改为希望储存sqlite数据库的位置，可以为已有db文件，如果没有会自动创建。

文件保存后会提示

![image](https://www-s.ucloud.cn/2025/04/32c28070c025c1cc183861dbc337a3e1_1744219330783.png)

installed选项卡下会出现sqlite_server的选项卡，如下图绿色状态说明已经启用。

![image](https://www-s.ucloud.cn/2025/04/7faa7486521eed8cc82ea77d94063940_1744219330782.png)


## 交互示例

**注意⚠️：以下prompt请在同一次对话内完成，不要清空上下文；或请二次提问时强调使用sqlite。**
### 列出database

对话框内输入以下指令并发送：

```
你能打开哪些database？
```
 
![image](https://www-s.ucloud.cn/2025/04/2c6abb7f8542c6f9be6d45c775d62135_1744219330781.png)

模型会返回需要运行的命令并询问是否要运行，选择run command或approve会执行命令。

一次任务可能会涉及多次运行，每次都需要人类进行批准。

如果想要模型全自动执行，可以配置auto approve选项，但是会有一定安全风险。

![image](https://www-s.ucloud.cn/2025/04/8b668dd4878c8fa917ba87db031acdc9_1744219330780.png)

运行后得到以下回答：

![image](https://www-s.ucloud.cn/2025/04/cc2c2543be0cb3505b98b91cd2d8e951_1744219330777.png)

### 创建table

```
我需要创建一个员工名单列表，里面需要记录11位数员工id,员工名称，员工职级和员工入职日期，帮我创建一下。
```
 
![image](https://www-s.ucloud.cn/2025/04/dbd7b094eb5e5b287c23cdf2b184e70b_1744219330774.png)

模型请求执行创建table命令，选择批准。

![image](https://www-s.ucloud.cn/2025/04/e83241b4c15d0c0b9df838ecc149d5d7_1744219330773.png)

这样就创建好了一个table用于存储数据。

![image](https://www-s.ucloud.cn/2025/04/8256f8993e00f06210cfb50ef737e75a_1744219330770.png)

### 插入随机示例数据

```
帮我生成20个随机的员工样本，我需要看一下表格是否符合预期。
```
 
模型请求执行插入命令，选择批准。

![image](https://www-s.ucloud.cn/2025/04/59197da0e18d784151756c8d352b27ad_1744219330766.png)

模型请求执行select命令用于检查是否插入成功，选择批准。

![image](https://www-s.ucloud.cn/2025/04/b7cf5bb4f815d83e2b9ed5457c1b055b_1744219330763.png)

模型执行完了select命令，可以看到成功在sqlite中插入了随机数据，任务完成。

![image](https://www-s.ucloud.cn/2025/04/53081111a50301871aa4044f41767a39_1744219330755.png)



### 清空数据

```
帮我把数据和列表都删除掉，我需要空的database。
```
 
模型请求执行删除列表命令，选择批准。

![image](https://www-s.ucloud.cn/2025/04/ea73eba196390170b4fa0e27039baedf_1744219330752.png)

模型请求执行列表查看功能，选择批准。

![image](https://www-s.ucloud.cn/2025/04/08e19e2605acfc11e2c29504a82dad2f_1744219330746.png)

模型确认数据已清空，任务完成。

![image](https://www-s.ucloud.cn/2025/04/2244261dd3c25c7cc948c69328c9ead0_1744219330742.png)




