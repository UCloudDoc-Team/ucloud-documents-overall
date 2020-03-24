# HTML

```html
<script src="//unpkg.com/docsify/lib/docsify.min.js"></script>
<script src="//unpkg.com/prismjs/components/prism-bash.min.js"></script>
<script src="//unpkg.com/prismjs/components/prism-php.min.js"></script>
```

# CSS

```css
.docs-header .pull-right{
	right: 24px;
}
.docs-header .header-search-wrapper{
	vertical-align: top;
	width: 34px;
	overflow: hidden;
}
```

# JS

```js
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:1469719,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
```


# node

```js
const util = require('util');

async function fn() {
  return 'hello world';
}
const callbackFunction = util.callbackify(fn);

callbackFunction((err, ret) => {
  if (err) throw err;
  console.log(ret);
});
```

# CPP

```cpp
#include <iostream>
using namespace std;
 
// main() 是程序开始执行的地方
 
int main()
{
   cout << "Hello World"; // 输出 Hello World
   return 0;
}
```

# go

```go
func hypot(x, y float64) float64 {
    return math.Sqrt(x*x + y*y)
}
fmt.Println(hypot(3,4)) // "5"
```

# json

```json
{
    "sites": [
    { "name":"菜鸟教程" , "url":"www.runoob.com" }, 
    { "name":"google" , "url":"www.google.com" }, 
    { "name":"微博" , "url":"www.weibo.com" }
    ]
}
```

# java

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

# lua

```lua
--[[ 函数返回两个值的最大值 --]]
function max(num1, num2)

   if (num1 > num2) then
      result = num1;
   else
      result = num2;
   end

   return result;
end
-- 调用函数
print("两值比较最大值为 ",max(10,4))
print("两值比较最大值为 ",max(5,6))
```

# python

```python
if condition_1:
    statement_block_1
elif condition_2:
    statement_block_2
else:
    statement_block_3
```

# bash

```bash
  --base-url     string       Set base-url to override the base-url in local config file 

  --help, -h                  help for uhost 

  --max-retry-times     int   Set max-retry-times to override the max-retry-times in local
                              config file (default -1) 

  --private-key     string    Set private-key to override the private-key in local config file 

  --public-key     string     Set public-key to override the public-key in local config file 

  --timeout-sec     int       Set timeout-sec to override the timeout-sec in local config file 

```

# sql

```sql
UPDATE table_name
SET column1=value1,column2=value2,...
WHERE some_column=some_value;
```

# yaml

```yaml
companies:
    -
        id: 1
        name: company1
        price: 200W
    -
        id: 2
        name: company2
        price: 500W
```

# swift

```swift
import Cocoa

struct Number
{
   var digits: Int
   let pi = 3.1415
}

var n = Number(digits: 12345)
n.digits = 67

print("\(n.digits)")
print("\(n.pi)")
```

# objectivec

```objectivec
#import <UIKit/UIKit.h>

@interface ViewController : UIViewController<UIImagePickerControllerDelegate>
{   
   UIImagePickerController *imagePicker;
   IBOutlet UIImageView *imageView;    
}
- (IBAction)showCamera:(id)sender;

@end
```

# hcl

```hcl
# 指定 UCloud Provider 和配置信息
provider "ucloud" {
  region = "cn-bj2"
}

# 查询当前地域下的所有可用区，取第一个可用区作为默认可用区
data "ucloud_zones" "default" {}

# 查询默认可用区中的主机镜像
data "ucloud_images" "default" {
  availability_zone = "${data.ucloud_zones.default.zones.0.id}"
  name_regex        = "^CentOS 7.[1-2] 64"
  image_type        = "base"
}

# 查询默认推荐 web 外网防火墙
data "ucloud_security_groups" "default" {
    type = "recommend_web"
}

# 创建一台 web 服务器
resource "ucloud_instance" "web" {
    availability_zone = "${data.ucloud_zones.default.zones.0.id}"
    image_id          = "${data.ucloud_images.default.images.0.id}"
    instance_type     = "n-basic-2"
    root_password     = "${var.instance_password}"
    name              = "tf-example-web-server"
    tag               = "tf-example"

    # the default Web Security Group that UCloud recommend to users
    security_group = "${data.ucloud_security_groups.default.security_groups.0.id}"
}

# 创建云硬盘
resource "ucloud_disk" "default" {
    availability_zone = "${data.ucloud_zones.default.zones.0.id}"
    name              = "tf-example-web-server"
    disk_size         = 30
}

# 云硬盘挂载到主机
resource "ucloud_disk_attachment" "default" {
  availability_zone = "${data.ucloud_zones.default.zones.0.id}"
  disk_id           = "${ucloud_disk.default.id}"
  instance_id       = "${ucloud_instance.web.id}"
}

# 创建外网弹性 EIP
resource "ucloud_eip" "default" {
  bandwidth     = 2
  charge_mode   = "bandwidth"
  name          = "tf-example-web-server"
  tag           = "tf-example"
  internet_type = "bgp"
}

# EIP 绑定到主机
resource "ucloud_eip_association" "default" {
  resource_id = "${ucloud_instance.web.id}"
  eip_id      = "${ucloud_eip.default.id}"
}
```

# php

```php
<?php 
$x=10; 
$y=6;
echo ($x + $y); // 输出16
echo '<br>';  // 换行
 
echo ($x - $y); // 输出4
echo '<br>';  // 换行
 
echo ($x * $y); // 输出60
echo '<br>';  // 换行
 
echo ($x / $y); // 输出1.6666666666667
echo '<br>';  // 换行
 
echo ($x % $y); // 输出4
echo '<br>';  // 换行
 
echo -$x;
?>
```
# TAB
<!-- tabs:start -->

#### ** English **

Hello!

#### ** French **

Bonjour!

#### ** Italian **

Ciao!

#### ** Englishs **

Hello!

<!-- tabs:end -->

!> dhkajka

?> dfagadg
