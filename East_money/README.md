##	East_money

### 爬取内容

获取前十页的200条新闻，将每一条新闻保存为一个txt，以新闻名命名，内容是该新闻文章的全部文字


### 爬取过程
首先将前十页的url添加到start_urls列表中，然后再parse中获取到每页的二十个新闻链接，调用spider函数，传入一个新闻链接，对每个新闻进行爬取。

### 知识点
scrapy框架和xpath语法

### 结果

![结果展示](https://raw.githubusercontent.com/liangweiyang/picbed/master/result.PNG)