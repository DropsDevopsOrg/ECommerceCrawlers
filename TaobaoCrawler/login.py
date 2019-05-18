import time
import requests
from logging import getLogger, basicConfig, INFO
from datetime import date, timedelta


from selenium.common.exceptions import NoSuchElementException


from dbcookie import DbClient


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# config logging level
basicConfig(level=INFO)

TB_LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36',
}

class CookieGetter():

    def __init__(self,logMessage,errMessage):
        self.browser = None
        self.db = DbClient()
        self.cookies = None
        self.search_url = 'https://s.taobao.com'
        self.logMessage = logMessage
        self.errMessage = errMessage
        self._failure_num =0

        self.logger = getLogger(__name__)

    def get_cookie(self):
        """
        Get cookies from db.
        :return: if exist return True, else False
        """
        cookie = self.db.get_cookies(flag=1)
        if cookie:
            return cookie
 

    def init_firefox(self):
        self.option = webdriver.FirefoxOptions()
        HEADLESS=False
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

        self.wait = WebDriverWait(self.browser, 20)  # 超时时长为10
        self.short_wait = WebDriverWait(self.browser, 5)  # 超时时长为10


    def add_cookies(self):
        """
        Add cookies to browser if exist.
        :return:
        """
        if self.cookies:
            for d in self.cookies:
                self.browser.add_cookie(d)

    def switch_to_password_mode(self):
        """
        切换到密码模式
        :return:
        """
        self.errMessage.put('切换至密码登录')
        password_login = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()



    def wait_for_main_page(self,short=False):
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



    def login(self,username,password):
        self.browser.get(TB_LOGIN_URL)
        print("Switch to password input.")
        self.switch_to_password_mode()
        time.sleep(0.5)
        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        time.sleep(0.5)
        weibo_user.clear()
        weibo_user.clear()

        weibo_user.send_keys(username)
        time.sleep(1)
        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.clear()
        time.sleep(0.5)
        weibo_pwd.send_keys(password)
        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()

        self.wait_for_main_page()
        self.browser.get(self.search_url)  # 跳转到搜索页面
        taobao_name = self.wait_for_main_page()

        if taobao_name == "":
            self.errMessage.put('[{}]登陆失败{}次'.format(taobao_name,self._failure_num))
            print('登陆失败%s次' % self._failure_num)
            self._failure_num += 1
            raise TimeoutError('登录失败')
        else:
            self.errMessage.put('[{}]登录成功'.format(taobao_name))
            print('[{}]登录成功'.format(taobao_name))
            self.browser.refresh()
            print("Login success.")
            self.errMessage.put('[{}]保存cookies'.format(taobao_name))
            print("Save cookies")
            self.save_cookies(username)

    def save_cookies(self,username):
        cookies = self.browser.get_cookies()
        t = str(int(time.time()))
        d = {}
        d['user'] = username
        d['flag'] = 1
        d['time'] = t
        d['cookies'] = cookies
        self.db.insert(d)



    def run(self,username,password):
        self.logger.info("Init date.")
        self.init_date()

        self.logger.info('Cookie is Null')
        self.logger.info("Init browser.")
        self.init_firefox()
        self.logger.info('Strart login')
        try:
            self.login(username,password)
            self.logger.info('Get cookies:')
            self.logger.info(self.browser.get_cookies())
            self.browser.quit()
        except Exception as e:
            self.browser.quit()
            self.errMessage.put('登录失败')
            print('登录失败')
            print(e)
            self.run(username,password)


    def init_date(self):
        date_offset = 0
        self.today_date = (date.today() + timedelta(days=-date_offset)).strftime("%Y-%m-%d")
        self.yesterday_date = (date.today() + timedelta(days=-date_offset-1)).strftime("%Y-%m-%d")

if __name__ == "__main__":

    import threading
    from multiprocessing import Process, JoinableQueue
    errMessage = JoinableQueue()
    logMessage = JoinableQueue()
    login = CookieGetter(logMessage,errMessage)

    from settings import USERINFO
    for userinfo in USERINFO:
        username = userinfo.get('username')
        password = userinfo.get('password')
        print(username,password)
        login.run(username=username,password=password)

    print(errMessage.put('账户登录完成'))