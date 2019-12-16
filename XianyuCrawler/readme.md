练习[闲鱼](https://2.taobao.com/)关键字商品爬虫

#  [闲鱼商品爬取](https://2.taobao.com/)

### 0x01 爬取思路

闲鱼网站原关键字直接搜索地址关闭。

经过查找，找到能搜索关键字的链接`https://s.2.taobao.com/list/?q=关键字&page=2&search_type=item&_input_charset=utf8`

经过多次爬取发现闲鱼并没有太多的反爬虫验证，索性连ua都不用给。【2019-08-07[在之前爬取频率过多接口失效](https://github.com/DropsDevopsOrg/ECommerceCrawlers/issues/9#issuecomment-518585101)】目前只能做异步方式参考

闲鱼只能爬取某一个关键字商品前100页面。想要获取所有数据的思路：100页的数据量100x20=2k条左右，全部商品有200k，爬取商品总数量，按照地区分级爬取，如果分级后仍然大于2k，继续分地级。

*只提供思路，并未实现*
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190424140812.png)

### 0x02 pandas操作csv

在存储的过程中发现编码出现了问题。使用`utf_8_sig`解决。

``` 伪代码
import pandas as pd
data = pd.DataFrame(self.data_list)
csv_filename = os.path.join(self.base_path, 'temp', '{}.csv'.format(keyword))
data.to_csv(csv_filename, header=self.header, index=False, mode='a+', encoding='utf_8_sig')

```

### 0x03 pyquery解析数据

pyquery解析商品数据返回可迭代的对象。

pyquery可以根据`class`，`id`，`div`的属性进行解析。

### 0x04 异步爬取

核心使用异步请求的方式[传送门README](asyxianyuREADME.md)

[项目部分代码.py](https://github.com/Hatcat123/XianyuSdd/blob/master/asy.py)

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190426111615.png)

[具体项目](https://github.com/Hatcat123/XianyuSdd)在另外的仓库，文件太大没有搬运

~~更新使用方式、7-25日 项目仍然能继续运行~~
接口失效后，应该不能爬取，只能作为练习思路学习

### 0x05 结果对比

**单线程爬取时间**

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190424141200.png)

**异步爬取时间**

忘了截图*100次请求大概用了6-8s

### 0x06 运行环境

- [x] python3.5
- [x] requirements.txt

```
python xianyu.py

python asyxianyu.py
```