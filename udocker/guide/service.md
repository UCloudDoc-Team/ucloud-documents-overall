<meta http-equiv='content-type' content='text/html;charset=utf-8'>


## 服务管理



### 服务的概念

功能跟 kubernetes 的ingress+service 相同

![](https://static.ucloud.cn/docs/udocker/images/guide/service模型.png?v=1624452073)

### 创建服务

创建服务需要指定Proxy 的个数、端口映射；创建完成后，会自动创建基于haproxy 的proxy 容器，用来做服务的请求转发和对Pod
的负载均衡，提供service 的内网服务能力。 ![](https://static.ucloud.cn/docs/udocker/images/guide/创建服务.png?v=1624452073)

### 创建Pod

Pod 为服务里真正工作的容器；创建好服务后，可以在服务列表中选择查看某个服务详情，在服务详情里创建Pod、调整Pod个数等。

### 服务详情

服务详情里可以绑定ULB、EIP、查看监控、查看Pod 列表、进行滚动升级等操作
![](https://static.ucloud.cn/docs/udocker/images/guide/服务详情2.png?v=1624452073)

### 绑定ULB

可以把Proxy 绑定到ULB；ULB 提供service
的外网访问能力。首先要先创建好ULB（ULB的vserver后端端口，需要跟Proxy的前端端口一致），然后选择对应的服务，选择详情，选择Proxy
绑定ULB，选择对应的ULB进行绑定； ![](https://static.ucloud.cn/docs/udocker/images/guide/服务绑定ULB.png?v=1624452073)

### 绑定EIP

在服务详情页面，可以选择某个Proxy，点击“…”功能菜单里面的“独立IP管理”，可以进行IP 绑定。

### 外网防火墙

在服务详情页面，可以选择“外网防火墙”，进行所有的proxy的外网防火墙的修改。

### 监控告警

在服务详情，在“监控信息”里可以查看Proxy 和Pod 的性能监控情况。在Umon 里可以设置告警模板。 UMon
参考：<https://docs.ucloud.cn/umon/README>
