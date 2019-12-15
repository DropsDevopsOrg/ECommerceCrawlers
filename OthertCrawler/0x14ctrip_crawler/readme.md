## 携程酒店评论爬取


### 需求

爬取某个地区的所有酒店的所有评论保存excel


### 分析

酒店的评论通过移动端爬取。网页的信息太多太杂。

接口post    url = "https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031074110034723384"

限制较少。直接爬取。

其中有一点酒店的地址获取没时间写（数据量不多，写代码的时间大于数据获取的时间）。直接在web端的ajax中找到过滤出来即可

### 运行

手动批量获取酒店的id

```
python ctrip_req.py
```

### 展示效果

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img2/20191215174258.png)


