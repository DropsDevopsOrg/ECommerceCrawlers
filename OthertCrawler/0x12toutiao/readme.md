## toutiao

### 爬取内容

在[今日头条](https://www.toutiao.com/)搜索“街拍”，爬取[结果页面](https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D)每篇文章的url，以及文章里面每张图片或视频的链接，存储到一个txt文件中


### 爬取过程
结果页面的内容时json数据，所以先找到对应的url，进行构造每页url，然后获取所有文章的链接，再爬取文章里面的图片或视频链接，而文章里面展示的图片和视频，也不再源码里面，而是使用js加载出来的，所以要使用selenium模拟浏览器。

### 知识点
selenium的使用，try except的使用，巩固xpath


### 爬取结果
![](https://raw.githubusercontent.com/liangweiyang/picbed/master/toutiao_result.PNG)