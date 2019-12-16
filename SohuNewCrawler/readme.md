
## 搜狐及时新闻采集——适合机器学习样本采集使用

### 爬取方式

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190512203013.jpg)


### 结构设计

多线程生产者消费者

### 使用框架

tk界面编程

### 演示：

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190512202741.jpg)



### 运行方式

运行环境win、python35、mongodb

1. 开启mongodb数据库

```
mongod.exe --dbpath=path
```

2. 安装依赖

```
pip install -r requirements.txt
```
3. python35

```
python TK_News.py
```

> 先确保数据库ok,然后点击采集，导出数据确保路径正确

**更新功能**

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190520213812.gif)

