# 说明

## 进度说明

- 阿里是一家伟大的公司, 此项目不再公开维护

- 本程序设计思路对阿里系自主平台(如:淘宝 taobao、天猫 tmall、闲鱼、菜鸟裹裹等平台均有效)，此处提供 淘宝 taobao 的程序

- 已完成

  1. 整体框架设计
  2. 搜索页面 csv 存储
  3. 多线程

- 未完成
  1. 详情页面 csv 存储
  2. 搜索页面 mysql 存储
  3. 详情页面 mysql 存储
  4. 搜索页面与详情页面同时爬取, mysql + redis 存储

## 使用方法

1. 在 `config.py` 文件中根据需要配置
2. 运行 `python3 main.py`

## 思路

1. 生产-消费 模式
2. 各功能单独建文件
3. 多线程
4. 数据库: csv \ redis \ mysql

## 阿里系自主平台(非收购)cookie 自动配置策略

1. 第一次无 cookie 请求，返回 cookie
2. 从返回的 cookie 提取 token 并计算 sign(token, timestamp, appKey, data),拼接新的 url
3. 第二次带返回的 cookie 请求 url，得到结果

- 注：
  1. cookie、token 有效期为 30 天，sign 有效期为 1 小时
  2. 理论上：只要一个小时跟换一次时间戳、重新计算一次 sign 即可，不断重复第二次请求
  3. 实践中：一小时更换一次有被反爬虫风险；可用 30 秒隧道代理，每次都重复第一步生成新 cookie(效率极高，时间可忽略)，理论上无反爬虫风险
  4. 程序中对第一次请求 url 固定(不影响程序)，若以后能从 js 文件中看懂其生成机制，则可改为每次自动生成

## taobao 入口

http://uland.taobao.com/sem/tbsearch?keyword=XXX

把最后的 XXX 换成您要搜索的内容即可

（用以第一步请求，得到真正的请求地址，程序中已经配置，不用管）

## Tmall 入口

http://www.tmall.com/

（用以第一步请求，得到真正的请求地址，程序中已经配置，不用管）

## mysql 表结构

## 关于作者

本人从事 `大数据`、`数据分析` 工作，欢迎各位大牛叨扰~

- github : [https://github.com/SoliDeoGloria31](https://github.com/SoliDeoGloria31)

- 码云 Gitee : [https://gitee.com/joseph31](https://gitee.com/joseph31)

- 微信 : mortaltiger

  <img src="https://gitee.com/joseph31/picture_bed/raw/master/mortaltiger.jpg" width="15%">

- 个人公众号: JosephNest(Joseph 的小窝)
  经常测试新功能导致服务器不稳定,可能会出故障, 实现`自动推荐系统`、`自动回复功能`、`需求留言功能`、`人工智能集成（图片识别）`、`其他功能定制`

  <img src="https://gitee.com/joseph31/picture_bed/raw/master/JosephNest.jpg" width="15%">
