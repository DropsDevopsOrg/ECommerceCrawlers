# 酷安应用商店爬虫

### 缘由

继续帮朋友爬取各大应用商店的apk下载链接，主要记录实现方法，经典的两层爬虫，如何在服务器允许的情况下，快速爬完。

### 技术点

- 生产者消费者模型
- 分析下载链接不能使用，最后发现下载的时候需要带`cookie`。

### 如何使用
酷安的app分两个类别`apk`和`game`实例类的时候传入其中之一，以及爬取的页数即可。