from logging import getLogger, basicConfig, DEBUG,INFO
from dbcookie import DbClient
from cookiepool.settings import TEST_URL
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from cookiepool.settings import HEADLESS

basicConfig(level=DEBUG)

class Tester():
    def __init__(self,logMessage,errMessage):
        self.test_url = TEST_URL
        self.main_url = 'https://s.taobao.com'
        self.url = 'https://s.taobao.com/search?q=袜子&sort=sale-desc&s=88'
        self.db = DbClient()
        self.logMessage = logMessage
        self.errMessage = errMessage
        self.logger = getLogger(__name__)

    def init_firefox(self):
        self.option = webdriver.FirefoxOptions()
        if HEADLESS:
            self.option.add_argument('--headless')
        self.option.set_preference('network.proxy.type', 1)
        self.option.set_preference('network.proxy.http', '127.0.0.1')  # IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
        self.option.set_preference('network.proxy.http_port', 8888)
        self.option.set_preference('network.proxy.ssl', '127.0.0.1')
        self.option.set_preference('network.proxy.ssl_port', 8888)
        self.option.set_preference('network.proxy.socks', '127.0.0.1')
        self.option.set_preference('network.proxy.socks_port', 8888)
        self.option.set_preference('network.proxy.ftp', '127.0.0.1')
        self.option.set_preference('network.proxy.ftp_port', 8888)
        self.option.set_preference("permissions.default.image", 2)  # 不加载图片,加快访问速度
        self.browser = webdriver.Firefox(executable_path='geckodriver.exe', options=self.option)
        self.browser.get(self.main_url)
        self.wait = WebDriverWait(self.browser, 20)  # 超时时长为10
        self.short_wait = WebDriverWait(self.browser, 5)  # 超时时长为10

    def __get_invcookies(self):
        return self.db.get_cookies(flag=2)
    def __get_nologin(self):
        return self.db.get_cookies(flag=0)
    def __get_newLogin(self,user):
        self.db.delete(user=user)  # 删除此cookie
        from dbuserinfo import Mongo
        userinfo = Mongo().select({"username": user})
        username = userinfo.get('username')
        password = userinfo.get('password')
        print('此账号未登录', user)
        self.errMessage.put('[{}]此账号未登录'.format( user))
        from login import CookieGetter
        login = CookieGetter(self.logMessage,self.errMessage)
        # 启动一个线程去登录
        import threading
        TProcess_taobao = threading.Thread(target=login.run, args=(username, password))
        TProcess_taobao.daemon = True
        TProcess_taobao.start()
        TProcess_taobao.join()
        print('开启线程去登陆')

    def is_username(self, short=False):
        # 简单检测用户是否有用户名登录，不准
        try:
            if short:
                taobao_name = self.short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                    '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
            else:
                taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                              '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
            return taobao_name.text
        except Exception as e:
            return ''
    def err_title(self):
        title = self.browser.title
        if title in ['security-X5', ]:
            return True
        else:
            # self.save_cookie()
            return False
    def _move(self, getcache):
        self.action = ActionChains(self.browser)
        self.action.click_and_hold(getcache).perform()
        self.action.move_to_element_with_offset(to_element=getcache, xoffset=288, yoffset=0).perform()
        time.sleep(7)
        self.action.reset_actions()

    def check_security(self):
        # 测网站的是不是处于安全状态
        move_num = 0
        while self.err_title():
            move_num += 1
            if move_num > 50:
                self.browser.quit()
                raise RuntimeError
            try:
                getcache = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nc_scale  > .nc_iconfont')))
                print('滑动的对象', getcache)
                self._move(getcache=getcache)  # 移动滑块。就是比较慢
                self.errMessage.put('滑块滑动{}次'.format(move_num))
                print('滑动{}次'.format(move_num))
                if self.is_username(short=True):
                    self.save_cookies(self.user)

                else:
                    self.browser.refresh()
            except Exception as e:
                print('滑动重大错误',e)
                # self.close_webdrive()
                # self.login()


    def save_cookies(self,user):
        cookies = self.browser.get_cookies()
        t = str(int(time.time()))
        d = {}
        d['user'] = user
        d['flag'] = 1
        d['time'] = t
        d['cookies'] = cookies
        self.db.update_cookie_flag1(user=user,cookies=cookies,t=t)

    def _check_login_by_cookie(self, url, cookies):
        # 用cookie的方式登录
        try:
            self.browser.delete_all_cookies()

            for cookie in cookies:
                self.browser.add_cookie({k: v for k, v in cookie.items()})
        except Exception as e:
            print('注入cookie错误')
            pass
        self.browser.get(url)

        self.check_security()

    def test(self):
        """
        Test if cookies can work.
        :return: if cookies words, return True, else False
        """
        while True:
            unlogin = self.__get_nologin()
            print('nologin', unlogin)
            if unlogin is None:
                self.errMessage.put('没有无登录的cookie')
                print('没有无登录的cookie')
                time.sleep(5)
            else:
                user =unlogin.get('user')
                self.__get_newLogin(user=user)


            q = self.__get_invcookies()
            print('cookie',q)
            if q is None:
                print('没有无效的cookie')
                self.errMessage.put('没有无效的cookie')
                self.logger.debug('没有无效的cookie')
                time.sleep(5)
                continue
            else:
                cookies =q.get('cookies')
                self.user = q.get('user')
                self.errMessage.put('验证{}的cookie'.format(self.user))
                self._check_login_by_cookie(self.url,cookies=cookies)



    def run(self):
        self.init_firefox()
        self.errMessage.put('开启监听状态')
        self.errMessage.put('开启监听状态……')
        print('检测cookie...')
        self.test()

if __name__ == '__main__':

    from multiprocessing import Process, JoinableQueue
    errMessage = JoinableQueue()
    logMessage = JoinableQueue()
    tester = Tester(logMessage,errMessage)

    tester.run()

