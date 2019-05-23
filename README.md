[![](https://img.shields.io/badge/language-Python35-green.svg)]()         [![](https://img.shields.io/badge/Branch-master-green.svg?longCache=true)]()           [![](https://img.shields.io/github/followers/DropsDevopsOrg.svg?label=Follow)]()      ![GitHub contributors](https://img.shields.io/github/contributors/DropsDevopsOrg/ECommerceCrawlers.svg)    [![](https://img.shields.io/github/forks/DropsDevopsOrg/ECommerceCrawlers.svg?label=Fork&style=social)]()       [![](https://img.shields.io/github/stars/DropsDevopsOrg/ECommerceCrawlers.svg?style=social)]()             [![](https://img.shields.io/github/watchers/DropsDevopsOrg/ECommerceCrawlers.svg?label=Watch&style=social)]() 

# ECommerceCrawlers

多种电商商品数据🐍爬虫，整理收集爬虫练习。通过实战项目练习解决一般爬虫中遇到的问题。

通过每个项目的readme，了解爬取过程分析。

对于精通爬虫的pyer，这将是一个很好的例子减少重复收集轮子的过程。项目经常更新维护，确保即下即用，减少爬取的时间。

对于小白通过✍️实战项目，了解爬虫的从无到有。爬虫过程的分析可以移步[项目wiki]()。爬虫可能是一件非常复杂、技术门槛很高的事情，但掌握正确的方法，在短时间内做到能够爬取主流网站的数据，其实非常容易实现，但建议从一开始就要有一个具体的目标。
 
在目标的驱动下，你的学习才会更加精准和高效。那些所有你认为必须的前置知识，都是可以在完成目标的过程中学到的😁😁😁。
 
欢迎大家对本项目的不足加以指正，⭕️Issues或者🔔Pr

>在之前上传的大文件贯穿了3/4的commits，发现每次clone达到100M，这与我们最初的想法违背，我们不能很有效的删除每一个文件（太懒），将重新进行初始化仓库的commit。并在今后不上传爬虫数据，优化仓库结构。

## CrawlerDemo
- [x] [DianpingCrawler](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/DianpingCrawler)：大众点评爬取
- [x] [📛TaobaoCrawler](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/TaobaoCrawler)：淘宝商品爬取
- [x] [📛XianyuCrawler](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/XianyuCrawler)：闲鱼商品爬取
- [x] [SohuNewCrawler](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/SohuNewCrawler)：新闻网爬取
- [ ] [📛WechatCrawler](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/WechatCrawler)：微信公众号爬取
- [x] [OtherCrawlers](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler)：一些有趣的爬虫例子
  - [x] [0x01 百度贴吧](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x01baidutieba)
  - [x] [0x02 豆瓣电影](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x02doubanmovie)
  - [x] [0x03 阿里任务](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x03alitask)
  - [x] [0x04 包图网视频](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x04baotu)
  - [ ] [0x05 全景网图片](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x05quanjing) 
  - [x] [0x06 豆瓣音乐](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x06douban_music)
  - [x] [0x07 某省药监局](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x07gdfda_pharmacy)
  - [x] [0x08 fofa](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x08fofa)
  - [ ] [0x09 汽车之家](https://github.com/DropsDevopsOrg/ECommerceCrawlers/tree/master/OthertCrawler#0x09autohome)

## Contribution👏

|||
|:-:|:-:|
|![](https://avatars0.githubusercontent.com/u/37971213?s=40&v=4)|![](https://avatars0.githubusercontent.com/u/22851022?s=40&v=4)|

> wait for you

## What You Learn ?

本项目使用了哪些有用的技术

- 数据分析
  - [x] chrome Devtools
  - [x] Fiddler
  - [x] Firefox
  - [ ] appnium
- 数据采集
  - [x] [urllib]()
  - [x] [requests](https://2.python-requests.org//zh_CN/latest/user/quickstart.html)
  - [ ] scrapy
  - [x] selenium
  - [ ] pypputeer 
- 数据解析
  - [x] re
  - [x] beautifulsoup
  - [x] xpath
  - [x] pyquery
  - [x] css 
- 数据保存 
  - [x] txt文本
  - [x] csv
  - [x] excel
  - [ ] mysql
  - [x] redis
  - [x] mongodb
- 反爬验证
  - [x] mitmproxy 绕过淘宝检测
  - [x] js数据解密
  - [x] js数据生成对应指纹库
  - [x] 文字混淆
  - [ ] 穿插脏数据
- 效率爬虫
  - [x] 单线程
  - [x] 多线程
  - [x] 多进程
  - [x] 异步协成
  - [ ] 分布式爬虫系统 

> *链接标识官方文档或推荐例子*

## What`s Spider 🕷？

### 🙋0x01 爬虫简介

**爬虫**

爬虫是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。

**爬虫作用**
- 市场分析：电商分析、商圈分析、一二级市场分析等
- 市场监控：电商、新闻、房源监控等
- 商机发现：招投标情报发现、客户资料发掘、企业客户发现等

**网页介绍**

- url
- html
- css
- js

**Roobots协议**

无规矩不成方圆，Robots协议就是爬虫中的规矩，它告诉爬虫和搜索引擎哪些页面可以抓取，哪些不可以抓取。
通常是一个叫作robots.txt的文本文件，放在网站的根目录下。

### 🙋0x02爬取过程

**获取数据**

**模拟获取数据**

### 🙋0x03解析数据

**re**

**beautifulsoup**

**xpath**

**yquery**

**css**

### 🙋0x04 存储数据

小规模数据存储（文本）

 - txt文本
- csv
- excel

大规模数据存储（数据库）

- mysql
- redis
- mongodb

### 🙋0x05 反爬措施

反爬

反反爬

### 🙋0x06 效率爬虫

异步协程

scrapy框架

## Padding

…………

## Awesome-Example😍:

- [CriseLYJ/awesome-python-login-model](https://github.com/CriseLYJ/awesome-python-login-model)

- [lb2281075105/Python-Spider](https://github.com/lb2281075105/Python-Spider)

- [SpiderCrackDemo](https://github.com/wkunzhi/SpiderCrackDemo)
