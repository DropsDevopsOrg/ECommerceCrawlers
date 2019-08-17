## FindJob

 爬取各大招聘公司，将招聘信息保存到本地。

### 招聘网站

- [BOSS直聘](https://www.zhipin.com/)
- [前程无忧51Job](https://www.51job.com/)
- [智联招聘](https://www.zhaopin.com/)
- [拉钩网](https://www.lagou.com/)

**持续更新**

### 参数设计

由于这些招聘网站架构设计不同，参数杂而不同，统一到此项目上有点吃力，最终传入两个参数：
```text
city：招聘地点（北京、上海等等）
keyword: 搜索关键词（如：java、python、平面设计等等）
```
同时可以选择使用其中一个网站获取数据，也可以选择所有网站进行数据获取。


### How To Use

使用之前在config.py文件中设置智联招聘的cookie，不然智联招聘反爬会验证cookie，同时Boss直聘存在反爬，会验证ip，频繁访问导致封禁IP。

![](https://raw.githubusercontent.com/Joynice/image/master/img/TIM%E6%88%AA%E5%9B%BE20190805153420.png)


```text
pip install requests
pip install lxml==4.3.0
python findjob.py   
```
### 数据展示

![数据展示](https://raw.githubusercontent.com/Joynice/image/master/img/TIM%E6%88%AA%E5%9B%BE20190812150305.png)
