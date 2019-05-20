练习[汽车之家全部车型](https://www.autohome.com.cn/grade/carhtml/A.html)爬虫

## [汽车之家](https://www.autohome.com.cn/car/)爬取

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190522101639.png)

### 0x01 爬取要求

- 获取全部车型
- 指导价格
- 车型配置参数

### 0x02 爬虫分析

参数不好爬取，通过分析找到接口

如 [车型接口:](https://www.autohome.com.cn/grade/carhtml/A.html) https://www.autohome.com.cn/grade/carhtml/A.html

换对应字符`A`，`B`，`C`爬取到对应车型

通过ascll码变换
```
start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]
```

配置信息不太容易分析

找来找去  找到这个接口


[https://dealer.autohome.com.cn/5925/spec_32040.html](https://dealer.autohome.com.cn/5925/spec_32040.html)

地区厂商
[https://carif.api.autohome.com.cn/dealer/LoadDealerPrice.ashx?_callback=LoadDealerPrice&type=1&seriesid=3170](https://carif.api.autohome.com.cn/dealer/LoadDealerPrice.ashx?_callback=LoadDealerPrice&type=1&seriesid=3170)

配置接口

[https://dealer.autohome.com.cn/Price/_SpecConfig?DealerId=5925&SpecId=36601&seriesId=3170](https://dealer.autohome.com.cn/Price/_SpecConfig?DealerId=5925&SpecId=36601&seriesId=3170)



### 0x03 实战



### 0x04 结果分析






