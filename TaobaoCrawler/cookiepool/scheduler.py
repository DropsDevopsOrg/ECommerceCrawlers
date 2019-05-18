import time
from multiprocessing import Process
from listen import Tester
from login import CookieGetter
from cookiepool.settings import TEST_CYCLE, LOGIN_CYCLE
from cookiepool.settings import TESTER_ENABLE, LOGIN_ENABLE


class Scheduler():

    def schedule_tester(self, cycle=TEST_CYCLE):
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)
 
    def schedule_login(self, cycle=LOGIN_CYCLE):
        login = CookieGetter()
        while True:
            login.run(username='',password='')
            time.sleep(cycle)



    def run(self):
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
            # tester_process.join()
        if LOGIN_ENABLE:
            login_process = Process(target=self.schedule_login)
            login_process.start()
            # login_process.join()

