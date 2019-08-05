## FindJob

 爬取各大招聘公司，将招聘信息保存到本地。

### 招聘网站

- [BOSS直聘](https://www.zhipin.com/)
- [前程无忧51Job](https://www.51job.com/)
- [智联招聘](https://www.zhaopin.com/)

**持续更新**

### 参数设计

由于这些招聘网站架构设计不同，参数杂而不同，统一到此项目上有点吃力，最终传入两个参数：
```text
city：招聘地点（北京、上海等等）
keyword: 搜索关键词（如：java、python、平面设计等等）
```
同时可以选择使用其中一个网站获取数据，也可以选择所有网站进行数据获取。

### How To Use

```text
pip install requests
pip install lxml==4.3.0
python findjob.py   
```
### 数据展示

![测试数据](https://raw.githubusercontent.com/Joynice/image/master/img/TIM%E6%88%AA%E5%9B%BE20190710155357.png)
