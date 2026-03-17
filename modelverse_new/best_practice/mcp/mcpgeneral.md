# MCP协议
Anthropic开源了一套[MCP协议](https://modelcontextprotocol.io/introduction)，它为连接AI系统与数据源提供了一个通用的、开放的标准，用单一协议取代了碎片化的集成方式。

其结果是，能以更简单、更可靠的方式让人工智能系统获取所需数据。通过该协议，开发者无需为不同数据源编写定制化代码，仅需通过MCP标准化接口即可完成多源数据对接，显著降低集成复杂度并提升可靠性。

这种"即插即用"的特性，让企业能快速将业务数据流注入大模型训练与推理环节，加速知识学习与模式挖掘。

# MCP架构简述
![架构图](https://www-s.ucloud.cn/2025/04/20acf058dbf10d527eba13c72fe35583_1744250962037.png)
- MCP Hosts: 如 Claude Desktop、IDE 或 AI 工具，希望通过 MCP 访问数据的程序
- MCP Clients: 维护与服务器一对一连接的协议客户端
- MCP Servers: 轻量级程序，通过标准的 Model Context Protocol 提供特定能力
- 本地数据源: MCP 服务器可安全访问的计算机文件、数据库和服务
- 远程服务: MCP 服务器可连接的互联网上的外部系统（如通过 APIs）
