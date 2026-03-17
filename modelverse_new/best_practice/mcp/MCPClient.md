# 通过UCloud API实现MCP Client


## 安装nodejs

 [https://nodejs.org/zh-cn](https://nodejs.org/zh-cn)



## 安装必要依赖

```plain
pip install mcp
pip install openai
```
 


## 运行代码

以下代码可以作为模版使用，但需注意**使用您实际的modelverse平台API_KEY**

> 我们选择无需密钥即可使用的MCP Server  [web-search](https://github.com/mzxrai/mcp-webresearch )。若您是windows系统，请打开代码中注释`# command="cmd.exe", args=\["/c", "npx", "-y", "@mzxrai/mcp-webresearch@latest"\]`

```python
import asyncio
import json
from typing import Optional
from contextlib import AsyncExitStack

from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


openai_client = OpenAI(
    base_url="https://api.modelverse.cn/v1",  # modelverse的API地址（无需更改）
    api_key="<您的api_key>",  # 控制台创建API Key 
)
model_name = "Qwen/QwQ-32B"  # 模型名称（无需更改）


class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.client = openai_client
        # 初始化 client
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self):
        # 使用无需密钥的MCP Server
        server_params = StdioServerParameters(
            # mac os系统使用下面的命令
            command="npx",
            args=["-y", "@mzxrai/mcp-webresearch@latest"],
            # windows 系统使用下面命令
            # command="cmd.exe", args=["/c", "npx", "-y", "@mzxrai/mcp-webresearch@latest"],
        )

        # 启动 MCP 服务器并建立通信
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # 列出 MCP 服务器上的工具
        list_tools_resp = await self.session.list_tools()
        list_prompt_resp = await self.session.list_prompts()
        list_resource_resp = await self.session.list_resources()
        self.session.get_prompt
        tools = list_tools_resp.tools
        print(
            "\n已连接到服务器，支持以下tools:",
            [tool.name for tool in tools],
            "以下prompts:",
            [prompt.name for prompt in list_prompt_resp.prompts],
            "以下resources:",
            [resource.name for resource in list_resource_resp.resources],
        )

    async def process_prompt(self, query: str) -> str:
        """
        使用大模型处理查询并调用可用的 MCP 工具 (tool Calling)
        """
        messages = [{"role": "user", "content": query}]

        list_tools_resp = await self.session.list_tools()
        self.session.complete

        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in list_tools_resp.tools
        ]

        resp = self.client.chat.completions.create(
            model=model_name, messages=messages, tools=available_tools
        )
        # 处理返回的内容
        content = resp.choices[0]
        if content.finish_reason == "tool_calls":
            # 如何是需要使用工具，就解析工具
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # 执行工具
            result = await self.session.call_tool(tool_name, tool_args)
            print(f"\n\n[Calling tool {tool_name} with args {tool_args}]\n\n")

            # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
            messages.append(
                {
                    "role": "tool",
                    "content": result.content[0].text,
                    "tool_call_id": tool_call.id,
                }
            )

            # 将上面的结果再返回给大模型用于生产最终的结果
            resp = self.client.chat.completions.create(
                messages=messages, model=model_name, tools=available_tools
            )
            return resp.choices[0].message.content

        return content.message.content

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\n🤖 MCP Host已启动！输入 'exit' 退出")

        while True:
            try:
                prompt = input("\n你: ").strip()
                if prompt.lower() == "exit":
                    break

                response = await self.process_prompt(prompt)
                print(f"\n🤖 ModelVerse QwQ-32B: {response}")

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":

    asyncio.run(main())

```
 


## 交互示例

用户请求：
> 请帮我阅读并总结网页 [https://XXXXXXXXXXXXXXXX)

![image](https://www-s.ucloud.cn/2025/04/fbf32af85c9cbc5650b8d45d9ab031f9_1744219791330.png)




