import requests,re
from lxml import etree
from openpyxl import Workbook

class AnpelSpider(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["商品编号","商品名称","CAS号","品牌","规格型号","标准价","库存与货期"])
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.12 Safari/537.36"}
        self.start_url = "http://www.anpel.com.cn/Search.aspx?Types=6&Type=0&KeyWord=CDAA"
        self.post_url = "http://www.anpel.com.cn/Search.aspx?Types=6&Type=0&KeyWord=CDAA"

    def get_url(self):
        resp = requests.get(self.start_url, headers=self.headers)
        content = resp.content.decode()
        return content

    def postUrl(self,__VIEWSTATE,__EVENTVALIDATION,pageNum):
        post_data = {
        "ScriptManager": "UpdatePanel1|btnNext",
        "__EVENTTARGET": "btnNext",
        "__EVENTARGUMENT":"",
        "__VIEWSTATE":__VIEWSTATE,
        "__VIEWSTATEGENERATOR": "BBBC20B8",
        "__VIEWSTATEENCRYPTED": "",
        "__EVENTVALIDATION":__EVENTVALIDATION,
        "txtHidd":"",
        "txtAuto":"",
        "txtshowBrand": 1,
        "txtbrands": 0,
        "txtcatalog": 0,
        "txtQty": "",
        "txtPrice": "",
        "txtShowType": 0,
        "dtList$ctl00$lblNewPrice1": 0,
        "dtList$ctl05$lblNewPrice1": 0,
        "dtList$ctl10$lblNewPrice1": 0,
        "dtList$ctl15$lblNewPrice1": 0,
        "dtList$ctl20$lblNewPrice1": 0,
        "dtList$ctl24$lblNewPrice1": 0,
        "dtList$ctl01$lblNewPrice1": 0,
        "dtList$ctl06$lblNewPrice1": 0,
        "dtList$ctl11$lblNewPrice1": 0,
        "dtList$ctl16$lblNewPrice1": 0,
        "dtList$ctl21$lblNewPrice1": 0,
        "dtList$ctl25$lblNewPrice1": 0,
        "dtList$ctl02$lblNewPrice1": 0,
        "dtList$ctl07$lblNewPrice1": 0,
        "dtList$ctl12$lblNewPrice1": 0,
        "dtList$ctl17$lblNewPrice1": 0,
        "dtList$ctl22$lblNewPrice1": 0,
        "dtList$ctl26$lblNewPrice1": 0,
        "dtList$ctl03$lblNewPrice1": 0,
        "dtList$ctl08$lblNewPrice1": 0,
        "dtList$ctl13$lblNewPrice1": 0,
        "dtList$ctl18$lblNewPrice1": 0,
        "dtList$ctl23$lblNewPrice1": 0,
        "dtList$ctl27$lblNewPrice1": 0,
        "dtList$ctl04$lblNewPrice1": 0,
        "dtList$ctl09$lblNewPrice1": 0,
        "dtList$ctl14$lblNewPrice1": 0,
        "dtList$ctl19$lblNewPrice1": 0,
        "gridview$ctl02$lblNewPrice1": 0,
        "gridview$ctl02$txtTrnQty": 1,
        "gridview$ctl03$lblNewPrice1": 0,
        "gridview$ctl03$txtTrnQty": 1,
        "gridview$ctl04$lblNewPrice1": 0,
        "gridview$ctl04$txtTrnQty": 1,
        "gridview$ctl05$lblNewPrice1": 0,
        "gridview$ctl05$txtTrnQty": 1,
        "gridview$ctl06$lblNewPrice1": 0,
        "gridview$ctl06$txtTrnQty": 1,
        "gridview$ctl07$lblNewPrice1": 0,
        "gridview$ctl07$txtTrnQty": 1,
        "gridview$ctl08$lblNewPrice1": 0,
        "gridview$ctl08$txtTrnQty": 1,
        "gridview$ctl09$lblNewPrice1": 0,
        "gridview$ctl09$txtTrnQty": 1,
        "gridview$ctl10$lblNewPrice1": 0,
        "gridview$ctl10$txtTrnQty": 1,
        "gridview$ctl11$lblNewPrice1": 0,
        "gridview$ctl11$txtTrnQty": 1,
        "gridview$ctl12$lblNewPrice1": 0,
        "gridview$ctl12$txtTrnQty": 1,
        "gridview$ctl13$lblNewPrice1": 0,
        "gridview$ctl13$txtTrnQty": 1,
        "gridview$ctl14$lblNewPrice1": 0,
        "gridview$ctl14$txtTrnQty": 1,
        "gridview$ctl15$lblNewPrice1": 0,
        "gridview$ctl15$txtTrnQty": 1,
        "gridview$ctl16$lblNewPrice1": 0,
        "gridview$ctl16$txtTrnQty": 1,
        "gridview$ctl17$lblNewPrice1": 0,
        "gridview$ctl17$txtTrnQty": 1,
        "gridview$ctl18$lblNewPrice1": 0,
        "gridview$ctl18$txtTrnQty": 1,
        "gridview$ctl19$lblNewPrice1": 0,
        "gridview$ctl19$txtTrnQty": 1,
        "gridview$ctl20$lblNewPrice1": 0,
        "gridview$ctl20$txtTrnQty": 1,
        "gridview$ctl21$lblNewPrice1": 0,
        "gridview$ctl21$txtTrnQty": 1,
        "gridview$ctl22$lblNewPrice1": 0,
        "gridview$ctl22$txtTrnQty": 1,
        "gridview$ctl23$lblNewPrice1": 0,
        "gridview$ctl23$txtTrnQty": 1,
        "gridview$ctl24$lblNewPrice1": 0,
        "gridview$ctl24$txtTrnQty": 1,
        "gridview$ctl25$lblNewPrice1": 0,
        "gridview$ctl25$txtTrnQty": 1,
        "gridview$ctl26$lblNewPrice1": 0,
        "gridview$ctl26$txtTrnQty": 1,
        "gridview$ctl27$lblNewPrice1": 0,
        "gridview$ctl27$txtTrnQty": 1,
        "gridview$ctl28$lblNewPrice1": 0,
        "gridview$ctl28$txtTrnQty": 1,
        "gridview$ctl29$lblNewPrice1": 0,
        "gridview$ctl29$txtTrnQty": 1,
        "txtToPageNum": pageNum,
        "txtUserID": "",
        "txtPassWo|0|rd": "",
        "IfChoose2": "on",
        "__ASYNCPOST": "true"}
        resp1 = requests.post(self.post_url, headers=self.headers, data=post_data)#, cookies=cookies)
        content1 = resp1.content.decode()
        content1 = re.sub("1\|#\|\|4\|[\d]+\|updatePanel\|UpdatePanel1\|", "", content1)
        __VIEWSTATE = re.findall("\|__VIEWSTATE\|(.*?)\|", content1)[0]
        __EVENTVALIDATION = re.findall("\|__EVENTVALIDATION\|(.*?)\|", content1)[0]
        content =re.sub("\|0\|hiddenField\|.*?\|$","",content1)
        return content,__VIEWSTATE,__EVENTVALIDATION

    def parse_content(self,content,VIEWSTATE="",EVENTVALIDATION="",flag=True):
        html = etree.HTML(content)
        tr_list = html.xpath("//table[@id='gridview']/tr")[1:]
        if len(tr_list):
            for tr in tr_list:
                item = {}
                # 商品编号
                item['id'] = "".join(tr.xpath("./td[1]/a//text()"))
                # 商品名称
                item['name'] = tr.xpath("./td[2]/a/text()")[0]
                # CAS号
                item['CAS'] = tr.xpath("./td[3]/span/text()")[0] if len(tr.xpath("./td[3]/span/text()"))>0 else ""
                # 品牌
                item['brand'] = tr.xpath("./td[4]/span/text()")[0]
                # 规格型号
                item['specificationsAndModels'] = tr.xpath("./td[5]/span/text()")[0]
                # 标准价
                item['normalPrice'] = tr.xpath("./td[6]/span/text()")[0] if len(tr.xpath("./td[6]/span/text()"))>0 \
                    else tr.xpath("./td[6]/a/text()")[0]
                # 库存与货期
                item['InventoryAndLeadTime'] = tr.xpath("./td[8]/span/text()")[0]
                self.ws.append([str(item['id']),str(item['name']),str(item['CAS']),str(item['brand']),str(item['specificationsAndModels']),
                                    str(item['normalPrice']),str(item['InventoryAndLeadTime'])])
                self.wb.save(r'anpel商品数据.xlsx')
                print(item)
        if flag:
            VIEWSTATE = html.xpath("//input[@id='__VIEWSTATE']/@value")[0]
            EVENTVALIDATION = html.xpath("//input[@id='__EVENTVALIDATION']/@value")[0]
            pageNum = int(html.xpath("//span[@id='lblPageNum2']/text()")[0])
            for i in range(2,pageNum+1):
                content, VIEWSTATE, EVENTVALIDATION = self.postUrl(VIEWSTATE, EVENTVALIDATION, i)
                self.parse_content(content, VIEWSTATE, EVENTVALIDATION, False)

    def run(self):
        content = self.get_url()
        self.parse_content(content)

if __name__ == '__main__':
    apl = AnpelSpider()
    apl.run()
