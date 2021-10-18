<meta http-equiv='content-type' content='text/html;charset=utf-8'>


## 容器管理


这里提到的容器为独立容器，区别于Pod。可以是持久化的也可以非持久化的。

### 创建容器

点击“创建容器”，进行创建容器操作；用户可以选择容器镜像、volume、环境变量等参数创建。

### 容器列表

可以按集群、按节点过滤容器列表，容器类型分为container（独立容器）、proxy（haproxy 容器）、pod（pod容器）
三类。可以单独过滤。

### 容器日志

在容器详情中的“容器日志”，可以查看容器的日志。在容器启动失败、安装失败后，可以通过查看容器日志排查原因。

### 删除容器

可以多选删除容器。会自动解绑EIP。

### 绑定EIP

选择对应容器，在功能菜单“…”中，选取“绑定弹性IP” ![](https://static.ucloud.cn/docs/udocker/images/guide/容器绑定eip.png?v=1624452073)

### 解绑EIP

![](https://static.ucloud.cn/docs/udocker/images/guide/容器解绑eip.png?v=1624452073)

### 外网防火墙

![](https://static.ucloud.cn/docs/udocker/images/guide/容器修改防火墙.png?v=1624452073)

### 监控告警

在容器详情中，选择“监控信息”tab，可以查看容器的监控数据。在Umon 产品中，可以设置对应的告警模板和新增告警监控。 UMon
参考：<https://docs.ucloud.cn/umon/README>
