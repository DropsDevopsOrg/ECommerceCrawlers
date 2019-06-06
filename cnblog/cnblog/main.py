from scrapy import cmdline

cmdline.execute("scrapy crawl cnblog_spider --nolog".split())       #--nolog是以不显示日志的形式运行，如果需要看详细信息，可以去掉
