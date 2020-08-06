
关于微信的公众号的爬取，部分内容功能进行二次开发，推出商业版，自媒体的朋友可以先联系使用


![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190515130702.png)


关于公众号的爬取：[常规的分为三种方式](https://github.com/DropsDevopsOrg/ECommerceCrawlers/wiki/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7%E7%88%AC%E5%8F%96%E7%A0%94%E7%A9%B6)。

 - 1、爬取搜狗微信接口。
 - 2、通过代理拦截到微信的请求数据与响应数据。
 - 3、hook微信的对象被动爬取。


## 公众号聚合平台

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826114458.png)


公众号聚合平台采用layui前端模板与bootstrap模板结合开发，服务应用采用Python Flask语言开发。是一款为了获取微信安全方面的公众号聚合平台。为客户提供优质的聚合服务。

* 解决了常规公众号难以采集的技术难题。
* 能够无人监听模式自动化采集。
* 使用友好的界面展示。在三端设备做了自适应展示。
* 提供api数据接口方便调用。使用者可以进行二次开发。
* 数据索引语句高优化，服务响应速度快。
* 微信公众号数据同步到github。

## 展示地址

展示地址：[http://wechat.doonsec.com](http://wechat.doonsec.com)

## 部署条件

windows服务器（或加linux服务器）最低配即可。支持docker镜像部署。

## 平台有哪些内容？

**后台展示**

### 0x01 管理员登录页
 
 后台管理员通过后台程序添加。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826114639.png)


### 0x02 后台仪表板展示

展示当前监控文章数、收录微信数、监控微信数、当前任务数据、任务进度、可视化图标分析展示

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826112952.png)


### 0x03 标签管理展示

前台展示的标签分类可以在此处修改，不仅限与默认的后台分类。并包含分类的添加修改删除操作操作。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826112841.png)


### 0x04 社区贡献管理展示

展示前台中使用者提交的优质公众号，减少后端管理员的收录压力。在核实公众号可以选择是否收录此公众号。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826113117.png)

### 0x05 公众号任务展示

控制监控任务的开启与关闭，并展示最近发布公众号的时间。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826113504.png)



### 0x06 公众号展示

展示公众号的详情信息，包含头像、描述、二维码等。为方便提交github。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826113323.png)

二维码展示

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826114017.png)


### 0x07 文章展示

分页展示所有文章，支持快速搜索功能，模糊查询。为优质违章标星在前端展示标星。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826113647.png)

查看文章展示

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826113726.png)


### 0x08 同步github功能

适用场景当收录新的公众号或者不再收录监控某些公众号后，可提交上你的`commit`同步到项目仓库。例[仓库地址](https://github.com/Hatcat123/WechatTogeter)。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826113548.png)


**前台展示**

### 0x01 首页展示

支持下拉刷新，公众号分类展示。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826132116.png)


### 0x02 社区提交功能

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826153729.png)

本站为微信安全聚合平台，原则上只收录与网络安全相关的微信公众号。 


Q：如何参与公众号的贡献？ 
A：首先发现一个新的安全公众号后，不要着急提交，看到导航栏上面的搜索图标没？先搜搜看。没有结果再去提交公众号。 

Q：贡献公众号会需要哪些参数？ 
A：1、公众号的名字。 2、公众号的标签，不确定分类或者你想要的分类不在选项里面请选择其他。 3、公众号的链接,找到公众号的历史文章连接。 或者找到二维码的链接。链接中包含微信公众号的`__biz`字段才为有效的链接。否则系统可能不识别你的提交。 4、创建者，此选项不为必选项。选填你的名字或Github的名字。 

Q：为什么我提交了公众号，而没看到前台展示呢？ 
A：提交的公众号需要管理员后台审核，审核不通过的将不会加入到监控任务中。 

Q：参与贡献后会得到什么？ 
A：当你的提交的公众号被管理员收录后，将会将你的名字自动加入到Github贡献列表中(这是一 个测试仓库，最终仓库为awesome-security-weixin-official-accounts）。 所以提供一个有效的github名称(而不是链接)将会在Github中很好展示。 

Q：网站后续会有什么改进？ 
A：在提交的面板增加留言的选项。 提高网站的访问速度。 增加文章后台过滤功能，过滤`鸡汤`文章。 提供展示公众号的季度分析，筛选质量更高的公众号。

### 0x03 搜索展示

搜索展示的内容标红处理，提示关于关键字的有多少篇文章。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826153914.png)

### 0x04 分类展示

展示某个类别下所有公众号的内容。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826153638.png)


### 0x05 单公众号展示

展示某个公众号的所有文章内容。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826154202.png)


### 0x06 详情页展示

除了最基本的展示，还有换一页的功能，轮换关于公众号的其他文章。

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190826154321.png)








