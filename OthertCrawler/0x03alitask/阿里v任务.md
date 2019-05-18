## 爬虫阿里v任务

### 目标url：[https://v.taobao.com/v/content/graphic](https://v.taobao.com/v/content/graphic)


![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190329154622.png)

点击网站`图文`->`型男`获得爬取目标

### 最终获得解析网站的结果

|达人名称|粉丝数|合作任务书|服务评分|任务完成率|垂直领域|7日浏览数|服务数量|累计用户数
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|null|null|null|null|null|null|null|null|null|
|null|null|null|null|null|null|null|null|null|
|null|null|null|null|null|null|null|null|null|

其中`累计用户数`需要进入到达人连接处寻找

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190329155057.png)
 * 对上图进行修改->`爬取累计用户数`
 
### 爬取方法：

1. 通过network抓包分析得到xml
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190329155432.png)
2. 分析构造请求的数据
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190329155510.png)

3. 数据构造：时间戳1553，cookie获取，页面currentPage
4. 写入Excel表中。使用python库`openpyxl`操作表格。
5. 使用pyinstaller将代码打包exe，或使用tk等界面编程写成界面打包exe。

注意：** 通过爬虫测试网站是否有反爬机制。cookie的获取是否有实效性。 **

代码格式参考[DemoSpider.py](https://github.com/DropsDevopsOrg/ECommerceCrawlers/blob/master/OthertCrawler/DemoSpider.py)
