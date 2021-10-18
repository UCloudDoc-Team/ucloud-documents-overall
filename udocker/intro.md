<meta http-equiv='content-type' content='text/html;charset=utf-8'>


# 产品简介



容器集群 UDocker 是UCloud推出的类 Kubernetes 的容器微服务管理平台。

UDocker可以让用户灵活创建、管理单个容器或容器集群。容器具有独立的内网IP，可以绑定一个或多个EIP，也有独立的防火墙、ULB、Nat网关等。

## 主要概念

UDocker的容器管理，分为资源池、节点、容器、服务、Pod 几个概念。

### 集群 (Cluster)

集群是一组资源的逻辑抽象。用户可以创建多个集群，每个集群可以包含多个节点。

### 节点 (Node)

节点是实际承载容器运行的宿主环境，目前节点相当于UCloud的云主机，之后会扩展到物理机环境。同一资源池下，允许加入异构配置的节点。

### 容器 (Container)

可以在节点上创建单个容器。容器可以绑定EIP，具有独立的出外网能力。

### 服务 (Service)

服务由 Proxy（Ingress）和 Pod 组成。Proxy 负责对 Pod请求做负载均衡，Pod 是一组同类型容器; Proxy 和Pod
都是容器，可以绑定EIP，具有独立的出外网能力。 服务的 Proxy 可以绑定ULB，提供高可用的外网服务能力。

### Pod (Pod)

Pod 是服务里面，提供同样功能的容器; 可以独立绑定EIP，具有独立的出外网能力。
