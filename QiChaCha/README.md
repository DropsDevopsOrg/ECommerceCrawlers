# 说明

## cookie策略

1. taobao 买入 企查查 一天会员, 并登陆查询, 获得cookie 中 
2. 经验证, QCCSESSID=i1bie6vpgudru9g56pkf8a**** 即可

- 注意
  
  1. 不登录`企查查`，不能显示的数据，若不用 vip cookie 也无法爬取（后台没有相关数据传过来）
  2. 在研究免 cookie 策略，不用 vip cookie，也能得到部分数据，但很多链接等不能得到
  3. 以后有时间时再完善
  4. 短时间内测试，vip cookie 的策略有效，小伙伴测试过程中发现有问题，请及时与我联系，谢谢
  5. `csv示例`中 csv 文件为 `utf-8` 格式，win平台乱码可在浏览器打开，或用 EditPlus 改为 `ascii` 格式

## 爬虫思路

1. 先获取园区信息(省份\城市-区\占地面积\企业数\详情链接),存为 csv
2. 逐个访问详情链接, 获得所有企业数
3. 将所有数据合并在一张表里

## 关于作者

本人从事 `大数据`、`数据分析` 工作，欢迎各位大牛叨扰~

- github : [https://github.com/SoliDeoGloria31](https://github.com/SoliDeoGloria31)

- 码云 Gitee : [https://gitee.com/joseph31](https://gitee.com/joseph31)

- 微信 : mortaltiger

  <img src="https://gitee.com/joseph31/picture_bed/raw/master/mortaltiger.jpg" width="20%">

- 个人公众号: JosephNest(Joseph 的小窝)
  经常测试新功能导致服务器不稳定,可能会出故障, 实现`自动推荐系统`、`自动回复功能`、`需求留言功能`、`人工智能集成（图片识别）`、`其他功能定制`

  <img src="https://gitee.com/joseph31/picture_bed/raw/master/JosephNest.jpg" width="20%">
