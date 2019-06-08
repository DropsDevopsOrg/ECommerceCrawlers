# 简单的scrapy实例
## 爬取博客园首页：[srapy_cnblog](https://www.cnblogs.com/sitehome/p/1)

 首先还是命令行创建project，然后依次编写各项文件

 ### 首先是编写item文件，根据爬取的内容，定义爬取字段。代码如下：	


 	import scrapy
	class CnblogItem(scrapy.Item):
    title = scrapy.Field()　　#定义爬取的标题
    link = scrapy.Field()　　 #定义爬取的连接

 ### 在spiders目录下编写spider文件(这是关键)，这里命名为cnblog_spider，代码如下：


 	import scrapy
	from cnblog.items import CnblogItem


 	class CnblogSpiderSpider(scrapy.Spider):
    name = "cnblog_spider"
    allowed_domains = ["cnblogs.com"]
    url = 'https://www.cnblogs.com/sitehome/p/'
    offset = 1
    start_urls = [url+str(offset)]

     def parse(self, response):


         item = CnblogItem()

         item['title'] = response.xpath('//a[@class="titlelnk"]/text()').extract()       #使用xpath搜索
        item['link'] = response.xpath('//a[@class="titlelnk"]/@href').extract()

         yield item

         print("第{0}页爬取完成".format(self.offset))
        if self.offset < 10:        #爬取到第几页
            self.offset += 1
        url2 = self.url+str(self.offset)    #拼接url
        print(url2)
        yield scrapy.Request(url=url2, callback=self.parse)
### 编写pipelines文件，用于把我们爬取到的数据写入TXT文件。

 	class FilePipeline(object):
    def process_item(self, item, spider):

         data = ''

         with open('cnblog.txt', 'a', encoding='utf-8') as f:
            titles = item['title']
            links = item['link']
            for i, j in zip(titles, links):
                data += i+'     '+j+'\n'

             f.write(data)
            f.close()
        return item

 ### 更改setting文件 

 	DEFAULT_REQUEST_HEADERS = {
   	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   	'Accept-Language': 'en',
   	 #user-agent新添加
   	 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	}
		#新修改
	ITEM_PIPELINES = {
    	'cnblog.pipelines.FilePipeline': 300,    #实现保存到txt文件

 	}
### 编写一个main文件，scrapy是不能在编译器里面调试的，但我们可以自己写一个主文件，运行这个主文件就可以像普通的工程一样在编译器里调式了。代码如下


 	from scrapy import cmdline

 	cmdline.execute("scrapy crawl cnblog_spider --nolog".split())       #--nolog是以不显示日志的形式运行，如果需要看详细信息，可以去掉


 现在，我们这个例子就算是写完了，运行main.py，就会生成一个cnblog.Ttxt的文件，里面就是我们爬取下来的内容了。

