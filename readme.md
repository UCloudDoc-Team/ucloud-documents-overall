# 移动仓库和删除仓库的操作如下-----

请修改moverepository.json, 格式如下<br/>
{
    "type": "add", // 变更类型：add move delete <br/>
    "repository": "uhost", // 仓库名称<br/>
    "classification": "compute" // 所属分类(仓库增加到哪个分类)<br/>
},<br/>
{
    "type": "move", // 变更类型：add move delete<br/>
    "repository": "uhost", // 仓库名称<br/>
    "classification": "compute" // 所属分类(移动之后的仓库的分类)<br/>
},<br/>
{
    "type": "delete", // 变更类型：add move delete<br/>
    "repository": "uhost", // 仓库名称<br/>
    "classification": "compute" // 所属分类(删除仓库之前的分类)<br/>
}<br/>

    每次移动仓库时，请把上一次的记录删除重写
    
    




