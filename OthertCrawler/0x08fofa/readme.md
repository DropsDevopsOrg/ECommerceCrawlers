练习[Fofa](https://fofa.so/)数据采集

[https://fofa.so/](https://fofa.so/)



### 爬取思路

调用无头浏览器获得页面数据，进行解析

使用fofa进行获取某方面的资产，但是官方api的虽然快、多，但是竟然收取f币。
无奈写了爬虫，在使用别人写好的工具的时候，发现一个bug，软件按照固定时间间隔爬取，几分钟之后就会卡死在搜索页面，十分不爽，而且保存的数据单一。

注意爬取时间间隔的控制。

### 练习技巧

- 使用无头浏览器爬虫
- 数据库使用
- pyquery

### 实战

**调用浏览器**

页面加载的方式，增加了自适应
```
    def _init_browser(self):

        # 初始化浏览器
        self.browser = webdriver.Chrome(service_args=['--load-images=false', '--disk-cache=true'])

        self.wait = WebDriverWait(self.browser, 10)
        self.browser.set_window_size(1400, 900)
```

**获取页面信息**

url的搜索参数通过base64加密构造，页面直接传入

```
    def turn_to_start_page(self):
        qbase = base64.b64encode(self.q.encode(encoding="utf-8"))
        starturl = 'https://fofa.so/result?page={}&qbase64={}#will_page'.format(self.now_page, str(qbase, 'utf-8'))
        self.browser.get(url=starturl)

```

**解析页面信息**

页面数据的获取
```
   html = self.browser.page_source
```

数据的解析使用pyquery


**保存数据**

数据保存mongodb
```
   def _init_db(self):
        # 连接mongodb数据库
        client = pymongo.MongoClient(self.MONGO_URL)
        self.db = client[self.MONGO_DB]
```

### 结果展示

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190513023817.png)


> 如果有可能我应该使用requests爬取数据














