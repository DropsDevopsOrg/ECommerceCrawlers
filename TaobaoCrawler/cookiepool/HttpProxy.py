TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.6.12/index.js'
INJECT_TEXT = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});'

def response(flow):
    if flow.request.url.startswith(TARGET_URL):
        flow.response.text = INJECT_TEXT + flow.response.text
        print('注入成功')

    if 'um.js' in flow.request.url or '115.js' in flow.request.url:
    # 屏蔽selenium检测
        print(flow.response.text)
        flow.response.text = flow.response.text + 'Object.defineProperties(navigator,{webdriver:{get:() => false}})'
# mitmdump -s HttpProxy.py -p 9000