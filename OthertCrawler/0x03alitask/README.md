练习爬虫阿里v任务

# 阿里v任务


### 0x01 思路

爬这个网站关键的地方就是`时间戳`，只有构造好当前的时间戳才能成功访问网站；但网站的时间戳的格式与python生成的时间戳格式有点不一样：

    #网站的时间戳：  
    _ksTS: 1553916935949_73
    
    #python生成的时间戳： 
    1553917060.5003772
    
其中，python的时间戳用time模块下的time()函数生成

可以看到，网站时间戳的前10位是标准的时间戳，但下划线前的三位(猜测是python时间戳小数点后的前三位)与下划线后面的两位(猜测是随机生成的)不知道；而且还发现网站请求的参数中的变量除了时间戳还有这样一个参数：

    callback: jsonp74
 
可以发现时间戳下划线后的两位是callback值最后两位-1 

则爬取时，需要构造`_ksTS`与`callback`这两个参数，之后更改`currentPage`参数即可更改爬取的页面

    cateType: 801
    role: 型男
    currentPage: 1
    _ksTS: 1553847286028_101   
    callback: jsonp102        
    
    
### 0x02 Ajax请求

这个爬虫练习就用到了Ajax请求的知识，Ajax是一种**原式HTML页面不被刷新的情况下，利用JavaScript向服务器交换数据并更新网页的技术**

虽然打开阿里这个网页时上面显示了一堆数据，但右键查看网页源代码的时候是什么数据都没有的，那要怎样查看数据呢？Ajax有其特殊的请求类型，即`XHR`；在Chrome下右键-检查-Network，选择XHR，即可过滤其他请求，只显示XHR的请求

选择一个XHR请求，在其request header中发现这样一个字段：`x-requested-with: XMLHttpRequest`，这也就标记了此请求是Ajax请求；在XHR请求的preview选项中可以看到请求得到的数据，这里是json格式的

另外，选中一个XHR请求，右键可以复制其请求的地址


### 0x03 用python对xlsx文件的一些基本操作

``` python
from openpyxl import Workbook

wb = Workbook()
sheet = wb.active

# 设置sheet页的标题
sheet.title = '爬取的数据sheet'

# 可以整行添加数据
sheet.append(['a','b','c'])

# 或指定添加位置
sheet['A1'].value = 'a'

# 生成文件
wb.save('spider.xlsx')
```


### 0x04 Contribution

ID|Address|Works
---|---|---
gtfly|[https://github.com/gtfly](https://github.com/gtfly)|[0x03alitask](0x03alitask/0x03alitask.py)
liangweiyang|[https://github.com/liangweiyang](https://github.com/liangweiyang)|[0x03alitask](0x03alitask/alitask.py)


