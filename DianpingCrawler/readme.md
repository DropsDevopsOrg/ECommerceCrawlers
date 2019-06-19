## DianpingCrawler

爬取大众点评

爬取的难度在于获取坐标偏移的文字字典，页面中的部分文字标签是靠js依照坐标解析svg文件获得文字。

##更新爬虫项目2019-6-18
 
大众点评的前端dom结构更变。导致之前的代码不能够继续适用。

如`http://www.dianping.com/shop/4122621/review_all/p3`中的所有的评论的类标签都变成review。中间隐藏的文字`应该`是16进制，暂时没有进行解密。类似：

```
<svgmtsi class="review"></svgmtsi>
<svgmtsi class="review"></svgmtsi>
"的"
<svgmtsi class="review"></svgmtsi>
<svgmtsi class="review"></svgmtsi>
```

在之前的爬取项目中，我们采取获取网站css中的标签，然后与svg图片进行解析组合成字典库。评论中的class中的属性对应字典库中的信息。这样便能将所有的评论爬取。
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190619165133.png)


### 新的思路方法

我们不选择绕过最近字库加密的方式。仍然选择原来的爬取方式，生成一个字典库，然后将评论的属性与字典库中的文字匹配。

通过发现解析网页的html发现不能只接对评论网站，返回结果内容如上面代码，class内容全部隐藏。


我们选择使用回应链接`http://www.dianping.com/review/551096310`，发现这里的评论竟然还是原来的解析方式。通过评论隐藏内容的属性的class的区别。()

这样我们就仍然可以使用过去的思想来进行修改。迭代新爬虫。



### 爬取方法

爬取的过程中需要我们在登录的情况下才能查看更多的评论，所以我们需要在浏览器中进行登录，获取登录后的cookie。

输入待爬取的目标的网站，内部解析网站中所有评论的详细评论链接、解析本次爬取过程的字典库需要两个条件，字库所对应的坐标与字典的svg矢量图的位置。然后对网站评论隐藏内容于字典库中的数据替换。解析所需要构造的内容如：头像、用户、标签、评论内容、图片、评分等。然后保存到txt或者其他，如有需要清洗成word格式。

**0x01、解析评论链接**

传入cookie并且设置好headers后进行爬取与解析评论回应链接。根据页面中是否有下一页来决定是否终止爬虫。

```
def _get_review_conment_page(self):  # 获得评论内容
    """
        请求评论页，并将<span></span>样式替换成文字
    """
    while self._cur_request_url:
        print('[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=self._cur_request_url))
        res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=self._cookies)
        html = res.text
        review_link = re.findall(r'><ahref="//(.*?)"target="_blank"class="reply"',
                                 html.replace(' ', '').replace('\n', ''))
        del (review_link[0])
        first_url = re.findall('ing.com/review/(.*?)', review_link[0])
        review_link.extend(first_url) # 将评论列表加入到总队列中
        self.review_links.extend(review_link)
        doc = etree.HTML(html)
        try:
            self._default_headers['Referer'] = self._cur_request_url
            next_page_url = 'http://www.dianping.com' + doc.xpath('.//a[@class="NextPage"]/@href')[0]
        except IndexError:
            next_page_url = None
        self._cur_request_url = next_page_url
```

**0x02、构造字典库**

这一步是比较麻烦的一个过程，只能点到为止，具体内容还需要你仔细观察代码。

首先我们通过F12找到对应的评论中的隐藏的字，然后根据class的属性就能找到索要加载的css与svg。我们发现一个文字有对应的一个标签，且相同的字体拥有同样的标签。这样就好办了。找到对应的文字，大概3-5个不同标签。记录下对应的标签-css中坐标位置-svg中文字的xy坐标位置。

一般找到3-5个文字就能猜出了文字库的规律。

```
def _get_font_dict_by_offset(self, url):
    """
        获取坐标偏移的文字字典, 会有最少两种形式的svg文件（目前只遇到两种）
    """
    res = requests.get(url, timeout=60)
    html = res.text
    font_dict = {}
    y_list = re.findall(r'd="M0 (\d+?) ', html)
    if y_list:
        font_list = re.findall(r'<textPath .*?>(.*?)<', html)
        for i, string in enumerate(font_list):
            y_offset = self.start_y - int(y_list[i])

            sub_font_dict = {}
            for j, font in enumerate(string):
                x_offset = -j * self.font_size
                sub_font_dict[x_offset] = font

            font_dict[y_offset] = sub_font_dict

    else:
        font_list = re.findall(r'<text.*?y="(.*?)">(.*?)<', html)

        for y, string in font_list:
            y_offset = self.start_y - int(y)
            sub_font_dict = {}
            for j, font in enumerate(string):
                x_offset = -j * self.font_size
                sub_font_dict[x_offset] = font

            font_dict[y_offset] = sub_font_dict
    # print('字体字典', font_dict)
    return font_dict

def _get_font_dict(self, url):
    """
        获取css样式对应文字的字典
    """
    print('解析svg成字典的css', url)
    res = requests.get(url, headers=self._css_headers, cookies=self._cookies, timeout=60)
    html = res.text

    background_image_link = re.findall(r'background-image: url\((.*?)\);', html)
    print('带有svg的链接', background_image_link)
    assert background_image_link
    background_image_link = 'http:' + background_image_link[1]
    html = re.sub(r'span.*?\}', '', html)
    group_offset_list = re.findall(r'\.([a-zA-Z0-9]{5,6}).*?round:(.*?)px (.*?)px;', html)  # css中的类
    # print('css中class对应坐标', group_offset_list)
    font_dict_by_offset = self._get_font_dict_by_offset(background_image_link)  # svg得到这里面对应成字典
    # print('解析svg成字典', font_dict_by_offset)

    for class_name, x_offset, y_offset in group_offset_list:
        y_offset = y_offset.replace('.0', '')
        x_offset = x_offset.replace('.0', '')
        # print(y_offset,x_offset)
        if font_dict_by_offset.get(int(y_offset)):
            self.font_dict[class_name] = font_dict_by_offset[int(y_offset)][int(x_offset)]

    return self.font_dict

```
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190619165041.png)


**0x03、替换标签内容**

得到对应的字典库，匹配详情页面中的隐藏评论标签，换成对应的文字。

```
class_set = set()
for span in re.findall(r'<svgmtsi class="([a-zA-Z0-9]{5,6})"></svgmtsi>', html):
    class_set.add(span)
for class_name in class_set:
    html = re.sub('<svgmtsi class="%s"></svgmtsi>' % class_name, self._font_dict.get(class_name,''), html)
```


**0x04、得到数据**

运用你想用的任何解析html的方式，re、bs4、pyquery、xpath、css等都可以将数据提取出来。这里写的仓促不值得借鉴。

```
None
```
![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190619165204.png)


**0x05、保存数据**

应别人要求，将数据保存在word中，并且图片也要保存下来


我们使用`docx`的库来操作word。为每一部分都设置格式。

```
pensize.font.name = '宋体'
pensize._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
pensize.font.size = Pt(15)
pensize.bold=True

```

看到docx文件说能读取内存中的图片，找了好久都没发现这个用法。就临时设置缓存文件进行保留爬取的图片。

```
req = requests.get(p)
with open('capth.png','wb')as f:
    f.write(req.content)

doc.add_picture('capth.png', width=Inches(2.5))

```


### 成品数据样式

![](https://raw.githubusercontent.com/Hatcat123/GraphicBed/master/Img/20190619165116.png)
