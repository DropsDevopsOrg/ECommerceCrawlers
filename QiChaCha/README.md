# 说明

## cookie 策略

- 代码公布不过两周, 部分高德功能被禁用, 当然, 还有其他方法实现

- 企查查

      	1. taobao 几块钱买入 企查查 一天\一个月 会员, 并登陆查询, 获得cookie 中 `QCCSESSID` 和 `acw_tc`

- 高德

      	1. 高德对 IP地址 无反爬机制
      	2. 高德POI信息查询,若数据量小于3万,可通过认证个人开发者,获取免费api接口,实现每天 3万次 / 50-200 并发量
      	3. 若数据量远大于3万,可通过页面爬虫,若 CPU\内存\网速 够用,可开 50-100 条线程并发(python内核是伪线程,可以自己测试并发效率, 并非数越多越好)

- 注意

  1. 不登录`企查查`，不能显示的数据，若不用 vip cookie 也无法爬取（后台没有相关数据传过来）
  2. 在研究免 cookie 策略，不用 vip cookie，也能得到部分数据，但很多链接等不能得到
  3. 以后有时间时再完善
  4. 短时间内测试，vip cookie 的策略有效，小伙伴测试过程中发现有问题，请及时与我联系，谢谢

## 爬虫思路

1. 先获取园区信息(省份\城市-区\占地面积\企业数\详情链接),存为 csv
2. 逐个访问详情链接, 获得所有企业数
3. 将所有数据合并在一张表里(因爬虫过程中被反爬等,中断继续,导致部分数据重复,进行 csv 去重\排序)
4. 高德地图 POI 信息爬取(园区、企业)
5. Tableau & echarts、django、mysql 等在线可视化

## 文件说明

1. `config.py` 配置文件(企查查需要代理,高德不需要)
2. `get_parks.py` 获取园区信息
3. `get_parks_companies.py` 获取企业信息(单线程,有 bug,未修复)
4. `get_parks_companies_threads.py` 获取企业信息(多线程,修复 bug)
5. `deal_error.py` 处理企查查爬虫中的错误(该部分重新爬取\其他策略等)
6. `deal_result.py` 处理企业信息 csv 文件: 去重\排序
7. `get_addr_longitude_latitude.py` 高德 POI 获取(地址\经度\维度),作为中间函数被其他文件导入
8. `get_parks_addr_long_lati.py` 园区高德 POI 获取(地址\经度\维度)
9. `get_companies_addr_long_lati.py` 企业高德 POI 获取(地址[已有]\经度\维度)
10. `echarts_parks.py` 基于园区的数据进行可视化, 调用 `pyecharts` 模块
11. `jn_parks.json` 程序运行中生成的中间文件, 标记各园区的经纬度, 被 `pyecharts` 模块调用
12. `map.html` 可以直接在 chrome 或 firefox 浏览器中打开看效果

    - 注意: 1. 数据可视化简单的可用 `Tableau` ,更好的是用 `Echarts`, python 对应的模块为 `pyecharts` 2. 新版的 `pyecharts` 针对 `pandas` 有 bug, 我在文件 `echarts_parks.py` 中对其修正

## 关于作者

本人从事 `大数据`、`数据分析` 工作，欢迎各位大牛叨扰~

- github : [https://github.com/SoliDeoGloria31](https://github.com/SoliDeoGloria31)

- 码云 Gitee : [https://gitee.com/joseph31](https://gitee.com/joseph31)

- 微信 : mortaltiger

  <img src="https://gitee.com/joseph31/picture_bed/raw/master/mortaltiger.jpg" width="20%">

- 个人公众号: JosephNest(Joseph 的小窝)
  经常测试新功能导致服务器不稳定,可能会出故障, 实现`自动推荐系统`、`自动回复功能`、`需求留言功能`、`人工智能集成（图片识别）`、`其他功能定制`

  <img src="https://gitee.com/joseph31/picture_bed/raw/master/JosephNest.jpg" width="20%">
