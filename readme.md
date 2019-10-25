# 新增仓库操作如下
请修改classification.json,nav.json。<br/>
classification.json用来管理产品在哪个大分类底下，nav.json用来管理产品的入口地址。<br/>

Note: 往classification添加新分类，无需排序，依次往下添加就可以。<br/>

account:账号<br/>
ai：人工智能<br/>
analysis：数据分析<br/>
beian：备案<br/>
cdn：云分发<br/>
charge：购买和计费<br/>
compute：计算<br/>
database：数据库<br/>
domain：域名与网站<br/>
management_monitor：管理与监控<br/>
middleware：中间件<br/>
network：网络<br/>
other：其他<br/>
policy：政策与规范<br/>
security：安全/优盾<br/>
software：程序应用<br/>
storage_cdn：存储<br/>
video：多媒体<br/>
iot：物联网<br/>
service：运维服务<br/>
developer:开发者工具<br/>


# 移动仓库操作如下
请修改moverepository.json,格式如下：<br/>
{
  [
  "repository":"",
  "from":"",
  "to":""
  ]
}<br/>
repository：仓库名<br/>
from:从哪个大类移除<br/>
to:到哪个大类<br/>
例如：cli从程序应用移动到开发者工具，
{
  [
  "repository":"cli",
  "from":"software",
  "to":"developer"
  ]
}

Note:
如果同时移动多个仓库，格式如下<br/>
{
  [
  "repository":"cli",
  "from":"software",
  "to":"developer"
  ],
  [
  "repository":"cli",
  "from":"software",
  "to":"developer"
  ]
}<br/>

    每次移动仓库时，请把上一次的记录删除重写

