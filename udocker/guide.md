<meta http-equiv='content-type' content='text/html;charset=utf-8'>


# 操作指南



## 资源池管理

### 创建资源池

登录控制台后，在左侧选择“容器集群 UDocker”，默认进入欢迎页，点击“创建资源池”按钮。

![image](https://static.ucloud.cn/docs/udocker/images/welcome.png?v=1624452073)

在“创建资源池”弹窗页填写要创建的资源池名称。

![image](https://static.ucloud.cn/docs/udocker/images/create_cluster.png?v=1624452073)

创建完资源池后，可以继续创建节点，在弹窗中选择节点配置、数量、付费信息等。

![image](https://static.ucloud.cn/docs/udocker/images/create_node.png?v=1624452073)

确定后创建成功，在列表中可以看到刚刚创建的资源池。

![image](https://static.ucloud.cn/docs/udocker/images/cluster_list.png?v=1624452073)

### 开通外网

如果创建容器依赖的镜像库是第三方镜像库，而非内网环境下的私有镜像库，则需要将资源池开通外网能力。

外网能力在一个地域下是全局开通的，所有资源池可以共享整个外网能力。

在资源池管理面板，点击“开通外网”按钮，选择外网带宽、付费信息等。

![image](https://static.ucloud.cn/docs/udocker/images/enable_network.png?v=1624452073)

最后点击“确定”，完成外网开通。

## 节点管理

### 节点列表

点击资源池id，进入资源池详情页，可以看到资源池下的节点列表。

![image](https://static.ucloud.cn/docs/udocker/images/node_list.png?v=1624452073)

### 关闭节点

点击管理面板上的“关闭”按钮，可以关闭已启动的节点。

![image](https://static.ucloud.cn/docs/udocker/images/node_poweroff.png?v=1624452073)

### 删除节点

想要删除不需要的节点，需要先将节点关闭，然后点击面板上的“删除”按钮。

![image](https://static.ucloud.cn/docs/udocker/images/node_delete.png?v=1624452073)

## 容器管理

### 创建容器

登录控制台后，在左侧选择“容器集群 UDocker”，然后选择“容器管理”标签，进入容器管理页，点击“创建容器”按钮。

![image](https://static.ucloud.cn/docs/udocker/images/docker_guide.png?v=1624452073)

在弹出的“创建容器”对话框中，选择容器的资源池和节点归属、镜像信息、容器配置等。

![image](https://static.ucloud.cn/docs/udocker/images/create_docker1.png?v=1624452073)

其中，镜像的选择，可以有多种方式。最方便的是直接从UCloud提供的镜像库中选择。

![image](https://static.ucloud.cn/docs/udocker/images/create_docker2.png?v=1624452073)

也可以从用户自制的镜像，或者任意的合法地址创建。镜像的合法格式为‘地址:版本’，其中版本可以省略，例如：uhub.service.ucloud.cn/ucloud/centos6-ssh

![image](https://static.ucloud.cn/docs/udocker/images/create_docker3.png?v=1624452073)

点击“确定”，完成创建。

### 容器列表

在容器管理页，可以看到已创建的容器列表。允许按照资源池和节点筛选列表。

![image](https://static.ucloud.cn/docs/udocker/images/docker_list.png?v=1624452073)

### 删除容器

想要删除不需要的容器，则将容器选中，然后点击面板上的“删除”按钮。

![image](https://static.ucloud.cn/docs/udocker/images/docker_delete.png?v=1624452073)

### 绑定EIP

在容器管理页，选择“绑定EIP”，可以给容器绑定1个或多个EIP。

![image](https://static.ucloud.cn/docs/udocker/images/bind_eip.png?v=1624452073)

### 修改防火墙

可以给不同容器加载不同的防火墙。在容器管理页，选择“修改防火墙”，可以调整防火墙配置。

![image](https://static.ucloud.cn/docs/udocker/images/bind_firewall.png?v=1624452073)

## 镜像管理

### 使用uhub 提交镜像

参考uhub 文档： <https://docs.ucloud.cn/uhub/guide>

### 创建镜像

在UDocker中选择“镜像管理”标签，进入镜像管理页，点击“创建镜像”按钮，可以以dockerfile方式创建镜像。

![image](https://static.ucloud.cn/docs/udocker/images/build_image1.png?v=1624452073)

在对话框中编辑dockerfile，并点击“确定”按钮，就创建了一个镜像。

![image](https://static.ucloud.cn/docs/udocker/images/build_image2.png?v=1624452073)
