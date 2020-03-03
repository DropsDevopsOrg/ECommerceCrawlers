import requests
import random
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
}

def get_tid():
    """
    获取tid,c,w
    :return:tid
    """
    tid_url = "https://passport.weibo.com/visitor/genvisitor"
    data = {
        "cb": "gen_callback",
        "fp": {
            "os": "3",
            "browser": "Chrome69,0,3497,100",
            "fonts": "undefined",
            "screenInfo": "1920*1080*24",
            "plugins": "Portable Document Format::internal-pdf-viewer::Chrome PDF Plugin|::mhjfbmdgcfjbbpaeojofohoefgiehjai::Chrome PDF Viewer|::internal-nacl-plugin::Native Client"
        }
    }
    req = requests.post(url=tid_url, data=data, headers=headers)

    if req.status_code == 200:
        ret = eval(req.text.replace("window.gen_callback && gen_callback(", "").replace(");", "").replace("true", "1"))
        return ret.get('data').get('tid')
    return None


def get_cookie():
    """
    获取完整的cookie
    :return: cookie
    """
    tid = get_tid()
    if not tid:
        return None

    cookies = {
        "tid": tid + "__095"  # + tid_c_w[1]
    }
    url = "https://passport.weibo.com/visitor/visitor?a=incarnate&t={tid}" \
          "&w=2&c=095&gc=&cb=cross_domain&from=weibo&_rand={rand}"
    req = requests.get(url.format(tid=tid, rand=random.random()),
                       cookies=cookies, headers=headers)
    if req.status_code != 200:
        return None

    ret = eval(req.text.replace("window.cross_domain && cross_domain(", "").replace(");", "").replace("null", "1"))

    try:
        sub = ret['data']['sub']
        if sub == 1:
            return None
        subp = ret['data']['subp']
    except KeyError:
        return None
    return sub, subp

if __name__ == "__main__":
    i=0
    while True:
        try:
            sub, subp = get_cookie()
            print(sub)
            print(subp)
            i += 1
            with open('cookies.csv','a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                L = [i,sub,subp]
                # print(L)
                writer.writerow(L)
                print("\n=====")
                time.sleep(10)
        except:
            time.sleep(0.1)