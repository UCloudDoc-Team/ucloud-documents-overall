# 模板工作原理
<subtitle>深入了解 UCloud Sandbox 如何通过快照技术实现毫秒级的沙箱启动与环境还原。</subtitle>

## 配置环境

在使用 SDK 之前，请确保已配置 `AGENTBOX_API_KEY` 环境变量。

?> 您可以在 [控制台 API 密钥页面](/https://console.ucloud.cn/modelverse/experience/api-keys) 获取您的密钥。

```bash
export AGENTBOX_API_KEY=your_api_key
```

## 总体流程

每次您发起模板构建请求时，系统都会根据您的定义（Dockerfile 或 SDK 定义）启动一个临时的容器环境进行预处理。

具体的构建步骤如下：

1.  **环境初始化**：基于指定的镜像启动容器，并挂载文件系统。
2.  **依赖安装**：执行您定义的 `apt_install`、`pip_install` 或 `run_cmd` 指令。
3.  **服务启动**（可选）：执行您配置的 [启动命令](/agent-sandbox/docs/sdk/template/08-start-and-ready-commands)。
4.  **就绪检查**：执行 [就绪命令](/agent-sandbox/docs/sdk/template/08-start-and-ready-commands) 确认环境已完全可用。
5.  **快照持久化**：将整个沙箱的文件系统及**内存状态（运行中的进程）**一并序列化并保存。

我们将这个最终生成的持久化状态称为 **沙箱模板**。

---

## 核心技术：沙盒快照 (Snapshot)

快照是 UCloud Sandbox 核心竞争力的体现。它不仅仅是磁盘的镜像，更是运行状态的完整保存。

*   **极速启动**：由于快照包含了内存状态，启动沙箱不再需要执行传统的系统引导或应用初始化，通常在 **50-200ms** 内即可进入就绪状态。
*   **状态还原**：当您从模板创建沙箱时，所有预置的进程（如数据库、Web 服务器）都已经处于运行状态，无需再次启动。

---

## 注意事项

### 内核版本
沙箱统一运行在 **LTS 6.1 Linux 内核**之上。

!> **内核绑定说明**：内核版本在**模板构建瞬间**即被固定。如果基础镜像库更新了内核，且您希望应用这些更新，您必须**重新构建模板**。旧模板产生的沙箱无法直接在线升级内核。

### 用户与目录
关于沙箱内的默认权限与工作目录，请参阅 [用户与工作目录](/agent-sandbox/docs/sdk/template/03-user-and-work-dir)。
