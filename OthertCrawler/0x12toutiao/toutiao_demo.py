import requests
import time
from selenium import webdriver


base_url = 'https://www.toutiao.com/api/search/content/'
timestamp = int(time.time()*1000)
article_url_list = []
browser = webdriver.Chrome()


# 获取到一个页面内所有的article url
def get_article_urls():
    for offset in range(0, 120, 20):  # 搜索结果有六个页面，所以只120，有时页面没这么多
        params = {
            'aid': 24,
            'app_name': 'web_search',
            'offset': offset,
            'format': 'json',
            'keyword': '街拍',
            'autoload': 'true',
            'count': 20,
            'en_qc': 1,
            'cur_tab': 1,
            'from': 'search_tab',
            'pd': 'synthesis',
            'timestamp': timestamp
        }
        headers = {
                'cookie': 'tt_webid=6726420735470077454; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6726420735470077454; csrftoken=e826e0c3c32a74555da7ec10112dc449; UM_distinctid=16ca3d7c13388-08bc3bd0b608e-c343162-144000-16ca3d7c1353a0; CNZZDATA1259612802=568057237-1566113713-https%253A%252F%252Fwww.toutiao.com%252F%7C1566113713; _ga=GA1.2.343540482.1566116922; __tasessionId=tiuwzvodh1566809947037; s_v_web_id=3c58c92ef3181a0e355d8348267b5efa',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
            }
        html = requests.get(url=base_url, params=params, headers=headers)
        result = list(html.json().get('data'))
        for item in result:
            article_url = item.get('article_url')   # 提取每篇文章的url
            if article_url and len(article_url) < 100:
                article_url_list.append(article_url)


def request_AND_storage():
    get_article_urls()
    print(article_url_list)
    print(len(article_url_list))
    for url in article_url_list:
        print('我是文章url****************************************************', url)
        with open('result_url_txt', 'a', encoding='utf-8') as f:
            f.write('***********************************************************************'+url+'\n')
        try:
            browser.get(url)
            try:
                # 图片在一个url的情况
                div = browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/div')
                if div:
                    image_divs = div.find_elements_by_css_selector('.pgc-img')
                    for image_div in image_divs:
                        image_url = image_div.find_element_by_xpath('./img').get_attribute('src')
                        print('图片在一个url:', image_url)
                        with open('result_url_txt', 'a', encoding='utf-8') as f:
                            f.write(image_url+'\n')
                    continue  # 结束本次循环
            except:
                try:
                    # 图片不在一个url的情况
                    li_list = browser.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/div/div[1]/div/div/ul').find_elements_by_xpath('./li')
                    if li_list:
                        for li in li_list:
                            photo_url = li.find_element_by_xpath('./div/img').get_attribute('src') or li.find_element_by_xpath('./div/img').get_attribute('data-src')
                            print('图片不在在一个url:', photo_url)
                            with open('result_url_txt', 'a', encoding='utf-8') as f:
                                f.write(photo_url+'\n')
                        continue  # 结束本次循环
                except:
                    # 视频的情况
                    time.sleep(2)
                    # try:
                    video_url = browser.find_element_by_xpath('//*[@id="vs"]/video').get_attribute('src')
                    print('视频:' ,video_url)
                    with open('result_url_txt', 'a', encoding='utf-8') as f:
                        f.write(video_url+'\n')
        except:
            print('此文章url无妨访问' ,browser.current_url)
    browser.close()


if __name__ == '__main__':
    request_AND_storage()

