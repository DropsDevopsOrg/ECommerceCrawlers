## OtherCrawler

其他有趣的爬虫

*难易程度不分先后*


## 有趣的爬虫


- [x] [0x01 百度贴吧](#0x01baidutieba)
- [x] [0x02 豆瓣电影](#0x02doubanmovie)
- [x] [0x03 阿里任务](#0x03alitask)
- [x] [0x04 包图网视频](#0x04baotu)
- [x] [0x05 全景网图片](#0x05quanjing) 
- [x] [0x06 douban_music](#0x06douban_music)
- [x] [0x07 药监局](#0x07gdfda_pharmacy)
- [x] [0x08 fofa](#0x08Fofa)
- [x] [0x09 autohome](#0x09autohome)
- [x] [0x10 baidu](#0x10baidu)
- [x] [0x11 蜘蛛泛目录](#0x11zzc) 
- [x] [0x12 今日头条爬取](#0x12toutiao)
- [x] [0x13 豆瓣影评](#0x13douban_yingping)
- [x] [0x14 协程评论爬取](#0x14ctrip_crawler)
- [x] [0x15 小米应用商店爬取](0x15xiaomiappshop)
- [x] [0x16 安居客信息采集](0x16anjuke)
## 有趣的爬虫介绍

### [0x01baidutieba](0x01baidutieba)

**关于百度贴吧的爬虫[分析与描述](0x01baidutieba/README.md)**

**练习知识点**

- re正则表达式


### [0x02doubanmovie](0x02doubanmovie)

**关于豆瓣影评的爬虫[分析与描述](0x02doubanmovie/README.md)**

返回数据为json对象，解析json。

**练习知识**

- json数据请求

### [0x03alitask](0x03alitask)

**关于阿里任务的爬虫[分析与描述](0x03alitask/README.md)**

爬这个网站关键的地方就是`时间戳`，只有构造好当前的时间戳才能成功访问网站；但网站的时间戳的格式与python生成的时间戳格式有点不一样。

**练习知识点**
- 参数时间戳
- ajxa
- xlsx

### [0x04baotu](0x04baotu)

**练习知识点**

- 使用队列，多线程优化爬虫


### [0x06douban_music](0x06douban_music)

**关于爬取豆瓣音乐排的爬虫[分析与描述](0x06douban_music/readme.md)**

**练习知识点**

 - re正则表达式、csv文件存储和Beautifulsoup库



### [0x07gdfda_pharmacy](0x07gdfda_pharmacy)

**关于某省药监局的爬取[分析与描述](0x07gdfda_pharmacy/readme.md)**

**练习知识点**

 - 队列编程
 - re正则表达式、csv文件存储
 - 单线程与多线程编程使用


### [0x08fofa](0x08fofa)

**关于fofa资产信息采集[分析与描述](0x08fofa/readme.md)**

**练习知识点**

- 使用无头浏览器爬虫
- 数据库使用
- pyquery


### [0x09autohome](0x09autohome)

**关于汽车之家信息采集[分析与描述](0x09autohome/readme.md)**

**练习知识点**

- 无

### [0x10baidu](0x10baidu)

**关于百度搜索关键词收录数爬取[分析与描述](0x10baidu/百度关键词收录数爬取.md)**

**练习知识点**

- 多线程
- csv
- xpath

### [0x11蜘蛛泛目录](0x11zzc)

**关于网站泛目录的蜘蛛爬取[分析与描述](0x11zzc/readme.md)**

**练习知识点**

- tkinter界面编程
- 多线程
- queue队列


### [0x12今日头条](0x12toutiao)
关于今日头条的[分析与描述](https://github.com/DropsDevopsOrg/ECommerceCrawlers/blob/master/OthertCrawler/0x12toutiao/readme.md)

**练习知识点**

- selenium
- try except
- xpath

### [0x13豆瓣影评分析](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler/0x13douban_yingping)

关于豆瓣影评分析的[分析与描述](https://github.com/DropsDevopsOrg/ECommerceCrawlers/blob/master/OthertCrawler/0x13douban_yingping/readme.md)

**练习知识点**
- jieba分词
- pyplot画图
- wordcloud词云
- Snownlp情感分析
- selenium模拟浏览器

### [0x14 协程评论爬取](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler/0x14ctrip_crawler)
关于协程评论爬取的[分析与描述](https://github.com/DropsDevopsOrg/ECommerceCrawlers/blob/master/OthertCrawler/0x14ctrip_crawler/readme.md)

**练习知识点**
- ajax
- mysql数据库操作
- sqlalchemy操作
