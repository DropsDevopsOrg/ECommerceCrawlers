练习[药监局](http://219.135.157.143/gdyj/sjwz/yp/sjwzYpjyxkzList.faces)信息爬虫

#  [药监局爬取](http://219.135.157.143/gdyj/sjwz/yp/sjwzYpjyxkzList.faces)


![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190507124859.png)


## 0x01 爬取思路

网站解析：网站的数据 通过post的方式提交服务器
获得源码，解析id，此id为详细页面的id，提交数据获得详细页面信息。

**获取的详情页网站id**
通过post，构造页数，获得页面内容，解析数据，得到id，保存标题、id、页数字典的列表

**获得详细信息**

通过post请求。构造页数、id的请求，获得页面内容、解析数据、得到对应数据[证书编号、经营方式]等数据 然后保存字典列表

**保存数据，保存成excel的数据**

可以使用我们之前讲的`csv`或者`openpyxl`

最好是通过异步的方式请求数据，--看下服务器数据有没有反爬机制--,存在反爬机制，爬取的频率过快，id将失效，一直获取首页的信息，产生重复数据。

走个本地的代理ssr

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190507124945.png)



## 0x02 实战

所有使用过的技术都是我们之项目练习中使用过的。可以反复回看练习项目。

采集了[5W的数据](广东省食品药品监督管理局56453.xlsx)。

**线程对比：**

|线程数|消耗时间|
|---|---|
|大概15|30Min|
|大概90|14Min|
|大概200|20Min|

每输出控制台3行完成一次请求，每秒请求大概为60-80次。
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190505185835.gif)
