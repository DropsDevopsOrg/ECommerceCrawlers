微博数据爬取练习

# 好用的微博轮子

个人微博内容获取的轮子，实测好用[https://github.com/dataabc/weiboSpider](https://github.com/dataabc/weiboSpider)

本项目其他文件夹包含：

- 微博关键字采集：search_word（免cookie）
- 微博评论内容采集：comment
- 微博转发内容采集：zhuanfa
- 微博mid转化url：tools


# 微博数据爬取(免cookie)

> 有个老吊让**300**块爬微博全网美妆博主的微博中带有淘宝链接的商品，（/-\）于是就有了这篇**价值300的**全网微博的爬虫。后期需求改的一塌糊涂，可恨的是要分析这些淘宝链接到底卖了啥，意思**顺带**爬下淘宝，套他猴子！

但是代码一点不虚，一个小时爬了6万微博用户信息。5分钟解析了这6万微博中到底在卖啥。数据量还是很丰富，主要还是免cookie。

### 0x01 需求分析


```
抓取微博美妆博主发送的微博带有三方推广的链接

1.抓取的数据不需要重复，必要需要的是KOL的微博昵称，KOL的微博链接,KOL的微博粉丝数，KOL的自身的淘宝链接，其他的KOL的微博关注数也可以添加。
2.数据里面包含了服装的kol，目前只需要美妆的KOL（有的kol是服装、美妆同时做的，ok的也）
3.数据里面的淘宝链接，有的是KOL发的品牌方的天猫店铺推广的链接，目前只需要kol自身的淘宝店铺，一般情况下KOL都是淘宝C店。
```
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190926163203.png)


* 用户获取
* 用户微博获取
* 用户微博中带有三方链接获取


### 0x02 用户获取

这里用户获取的方式有两种。一：通过搜索入口搜索指定关键字的人群。二：老哥提供了几个大V的微博，然后就没然后了。


**通过搜搜获取微博用户**

直接使用webdriver，通过搜索入口获取到用户的信息，但是点击下一页会出现登录的跳转请求，通过增加选择参数如页数、省份地区、年龄、性别等参数。大约能获取某个关键字下10万用户
`https://s.weibo.com/user?q={KEYWORD}&Refer=weibo_user&page={page}&region=custom:{custom}:{sec}`

在获取用户信息的html中，使用pyquery这个库不能部分信息，很奇怪选择了使用正则的方法。其中有个坑，微博的个人主页不仅仅可以通过id还有博主的是英文的方式。

### 0x03 获取微博

获取个人博主全部微博找到一个请求接口`'https://weibo.cn/%s/info' % (self.user_id)`，但是在这里获取的微博中没有淘宝的连接。

### 0x04 获取淘宝商品链接

使用橱窗获取某微博博主的全部分享链接`https://shop.sc.weibo.com/h5/shop/index?weiboUid=1907518591`，这里有ajax请求。没有什么限制直接构造访问。

返回数据中`out_type`参数含义：`2淘宝 3天猫 0 自身`


## 使用

```python
python weibo_search_people.py
python SinaShop.py
```

## 总结

新浪服务器挺强，线程并发这么多，响应速度还是极快的。

**练习点**

* 多线程编程
* 优化了生产者消费者的代码。逻辑更清晰
* webdriver
* pyquery
* re
* pyopenxy







