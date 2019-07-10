泛目录解析程序

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190625160323.gif)


## 需求

给一个特定的网站域名，设置百度的蜘蛛爬虫，然后构造一个随机目录，如'isnsa/jasoh212.html'。收集返回结果的标题。对标题进行去重处理。结果保存在一个文件夹中，随机命名标题txt文件，每300kb保存一个文件。

做成界面。根据传入的值判断程序是否结束。

目标在短时间内尝试进行50w次扫描。

## 分析

界面效果

传入值：目标网站、线程数、爬取次数、睡眠时间、标题文件保存目录。
>目录长度，前目录长度，后目录长度大于4

输出：标题txt、界面标题展示、进度展示

功能：启动爬虫、暂停爬虫、重启爬虫、退出程序

## 实现

### 泛目录生成

使用随机random生成前目录与后目录字符，长度暂时固定，代码如下
```
import random
import string

def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str
print(generate_random_str(6))
print(generate_random_str(8))
```

### 爬虫功能
运用python requests库，设置百度蜘蛛爬虫UA访问目标网站，解析网站内容获取标题。在这个过程中遇到标题编码不能解析的问题。导致不能够通用爬虫吧！

使用html库进行解析，将unicode转换成中文
```
print(html.unescape(title))

>&#28595;&#38376;&#38134;&#27827;&#30340;&#32593;&#22336;&#52;&#48;&#48;-2019动画片大全
>澳门银河的网址400-2019动画片大全

```


使用多线程，线程可设置成100左右，

多线程的方式参考`其他`项目中的基础



## 展示

下载[编译完成项目](https://github.com/DropsDevopsOrg/ECommerceCrawlers/releases/download/V11_0.1/tk_zzc.exe)
打开exe后自动初始化项目

在配置中输入域名`http://richuriluo.qhdi.com/yl`，次数100，线程10，频率0，路径等。

点击`更新配置`后

点击开启采集，程序自动采集，上端进度条能展示当前任务的进度，点击暂停采集便能暂停爬虫，开启`继续采集`爬虫继续。

采集结束后，日志输出采集的成果，文件输出到保存的路径中。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190625160301.png)

测试域名参数

http://www.taopic.com/poc

http://www.kan300.com/doc

http://www.kan300.com/hot
