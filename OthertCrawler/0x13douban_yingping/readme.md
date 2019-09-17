## 豆瓣影评分析

### 爬虫过程

输入电影的电影名、id或链接，模拟登陆爬取五百条短评，存到一个txt文件里，利用jieba、wordcloud和pyplot生成词云，利用Snownlp和pyplot对短评进行情感分析并展示。

### 生成词云
	def cut_word():
    with open('result.txt', 'r', encoding='utf-8') as file:
        # 读取文件里面的全部内容
        comment_txt = file.read()
        # 使用jieba进行分割
        wordlist = jieba.cut(comment_txt)
        print('***********',wordlist)
        wl = "/".join(wordlist)
        # print(wl)
        return wl


	def create_word_cloud():
	    # 设置词云形状图片,numpy+PIL方式读取图片
	    wc_mask = np.array(Image.open('Emile.jpg'))
	    # 数据清洗词列表
	    stop_words = ['就是', '不是', '但是', '还是', '只是', '这样', '这个', '一个', '什么', '电影', '没有']
	    # 设置词云的一些配置，如：字体，背景色，词云形状，大小,生成词云对象
	    wc = WordCloud(mask=wc_mask, background_color="white", stopwords=stop_words, max_words=50, scale=4,
	                   max_font_size=50, random_state=42)
	    # 生成词云
	    wc.generate(cut_word())
	
	    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
	    # 开始画图
	    plt.imshow(wc, interpolation="bilinear")
	    # 为云图去掉坐标轴
	    plt.axis("off")
	    plt.figure()
	    plt.show()

### 生成情感分析表
	def data_show():
	    f = open('result.txt', 'r', encoding='UTF-8')
	    list = f.readlines()
	    sentimentslist = []
	    for i in list:
	        s = SnowNLP(i)
	        sentimentslist.append(s.sentiments)
	    print(sentimentslist)
	    print(len(sentimentslist))
	    plt.hist(sentimentslist, bins=10, facecolor='g')
	    plt.xlabel('情感概率')
	    plt.ylabel('数量')
	    plt.title('情感分析')
    	plt.show()

### 结果

Snownlp是针对商品品论的，拿来对影评做情感分析会有些误差。为了区别明显，这里选了流浪地球和逐梦演艺圈两部电影。后者豆瓣评分高达2.多。

流浪地球的词云
![](https://raw.githubusercontent.com/liangweiyang/picbed/master/%E6%B5%81%E6%B5%AA%E5%9C%B0%E7%90%83%E8%AF%8D%E4%BA%91.png)

流浪地球的情感分析
![](https://raw.githubusercontent.com/liangweiyang/picbed/master/%E6%B5%81%E6%B5%AA%E5%9C%B0%E7%90%83%E5%88%86%E6%9E%90.png)

逐梦演艺圈的词云
![](https://raw.githubusercontent.com/liangweiyang/picbed/master/%E9%80%90%E6%A2%A6%E6%BC%94%E8%89%BA%E5%9C%88%E8%AF%8D%E4%BA%91.png)

逐梦演艺圈的分析
![](https://raw.githubusercontent.com/liangweiyang/picbed/master/%E9%80%90%E6%A2%A6%E6%BC%94%E8%89%BA%E5%9C%88%E5%88%86%E6%9E%90.png)

Snownlp情感分析在0.5以上算是好评，可以看到两部电影的评论差距明显。

### 遇到的一些问题
- 登陆：
	不登陆的话只能查看前200条评论，登陆之后可以查看500条。利用burpsuite抓包，找到登陆时的账号密码再url中的参数。name=xxxx&password=xxx&remember=false。登陆多了之后会需要验证码
- ip被封：
	到[西刺](https://www.xicidaili.com/)上寻找代理，设置proxies参数
- pip安装包命令无效：
	网上看了很多方案都说直接运行?python3 -m pip install --upgrade pip 来升级pip版本就好了，这个在大多数情况下都是有用的。因为重装以后会根据更改后的python的执行文件来创建关联。但是如果你的pip已经是最新版本的话就行不通了，因为已经是最新的版本根本就不让你升级。那么就用下面的命令来强制重装 pip
		python3 ?-m pip install --upgrade --force-reinstall pip

- pip安装包时失败：
	换源安装：豆瓣：http://pypi.douban.com/simple/		清华：https://pypi.tuna.tsinghua.edu.cn/simple

- matplotlib不显示中文：
	更改配置文件，放一个大佬的回答链接：[解决matplotlib不显示中文](https://www.jianshu.com/p/b02ec7dc39dd)

- 词云不现实中文：
	设置字体路径。

### 使用知识点

- jieba分词
- pyplot画图
- wordcloud词云
- Snownlp情感分析
- selenium模拟浏览器
