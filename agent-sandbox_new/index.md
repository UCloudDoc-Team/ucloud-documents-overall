# 概览

UCloud Sandbox 为您提供安全可靠的弹性沙箱计算服务。只需几秒钟，您就可以在云端获取和启用具备完整操作系统能力的沙箱，用于执行 AI Agent 生成的代码、进行自动化测试或运行不可信的脚本。

随着业务需求的变化，您可以实时扩展或缩减计算资源。UCloud Sandbox 支持按实际使用的资源计费，可以为您节约计算成本。

#### <center>[快速开始](/agent-sandbox/docs/sdk/00-quick-start)   |   [核心概念](/agent-sandbox/docs/product/02-concepts)   |   [CLI 指南](/agent-sandbox/docs/cli/cli)   |   [常见问题](/agent-sandbox/docs/troubleshooting/00-overview)</center>

---

## 推荐学习路径

按「先跑起来 → 理解概念 → 深入能力」的顺序开始：

### 第一步：快速上手
1. [前置条件与认证](/agent-sandbox/docs/product/01-prerequisites) - 获取 API Key 并配置环境
2. [SDK 快速开始](/agent-sandbox/docs/sdk/00-quick-start) - 5 分钟创建第一个沙箱
3. [CLI 指南](/agent-sandbox/docs/cli/cli) - 命令行工具入门

### 第二步：理解核心概念
1. [概念速览](/agent-sandbox/docs/product/02-concepts) - 沙箱、模板、快照的关系
2. [产品架构](/agent-sandbox/docs/product/03-architecture) - 系统组件与数据流
3. [模板工作原理](/agent-sandbox/docs/sdk/template/02-how-it-works) - 快照机制详解

### 第三步：深入使用
1. [模板快速开始](/agent-sandbox/docs/sdk/template/01-quick-start) - 构建自定义模板
2. [命令执行](/agent-sandbox/docs/sdk/commands/01-overview) - 在沙箱中运行命令
3. [文件系统](/agent-sandbox/docs/sdk/filesystem/01-overview) - 文件读写与传输

---

## 核心能力

| 能力 | 说明 | 相关文档 |
|-----|------|---------|
| **代码执行** | 安全运行 Agent 生成的 Python、JavaScript 等代码 | [命令执行](/agent-sandbox/docs/sdk/commands/01-overview) |
| **文件操作** | 在沙箱与宿主机之间传输文件 | [文件系统](/agent-sandbox/docs/sdk/filesystem/01-overview) |
| **自定义模板** | 预装依赖、预置文件、毫秒级启动 | [模板指南](/agent-sandbox/docs/sdk/template/01-quick-start) |
| **网络控制** | 灵活控制沙箱的互联网访问权限 | [网络访问](/agent-sandbox/docs/sdk/sandbox/10-internet-access) |
| **数据持久化** | 挂载远程存储桶或持久化卷 | [持久化](/agent-sandbox/docs/sdk/sandbox/04-persistence) |
| **E2B 兼容** | 使用现有 E2B SDK 无缝接入 | [E2B 兼容模式](/agent-sandbox/docs/sdk/e2b-compatibility) |

---

## 典型应用场景

- **AI Agent 代码执行**：安全运行 LLM 生成的代码，隔离风险
- **自动化测试**：在隔离环境中运行测试用例
- **数据分析**：提供预装分析工具的沙箱环境
- **教育培训**：为学员提供独立的实验环境

?> 更多示例请参阅 [示例库](/agent-sandbox/docs/sdk/template/12-examples)

---

## 常见问题

遇到问题？请查阅 [常见问题与排障](/agent-sandbox/docs/troubleshooting/00-overview)，涵盖：

- 认证与权限问题
- 模板构建卡住
- 命令执行超时
- 网络访问失败
- 限流与资源限制

---

## 快速链接

| 类别 | 链接 |
|-----|------|
| **入门** | [前置条件](/agent-sandbox/docs/product/01-prerequisites) · [SDK 快速开始](/agent-sandbox/docs/sdk/00-quick-start) · [CLI 指南](/agent-sandbox/docs/cli/cli) |
| **概念** | [概念速览](/agent-sandbox/docs/product/02-concepts) · [产品架构](/agent-sandbox/docs/product/03-architecture) |
| **参考** | [词汇表](/agent-sandbox//glossary) · [常见问题](/agent-sandbox/docs/troubleshooting/00-overview) |


