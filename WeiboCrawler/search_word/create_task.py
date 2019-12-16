from model import WeiboInfo, WeiboTask, engine
from sqlalchemy.orm import sessionmaker

from pyquery import PyQuery as pq
import random

Session = sessionmaker(bind=engine)
session = Session()
import datetime


def getBetweenDay(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list
def run():
    # dateList3 = getBetweenDay("2019-11-16", "2019-12-7")
    dateList3 = getBetweenDay("2009-8-16", "2019-12-7")
    for i in dateList3:
        print(i)
        pingdeng = "https://s.weibo.com/weibo?q=%E5%B9%B3%E7%AD%89&typeall=1&suball=1&timescope=custom:{}&Refer=SWeibo_box&page=indexpage"


        dealtime = i + ":" + i

        weibo_task =WeiboTask(flag='0',url=pingdeng.format(dealtime), between=dealtime,time=i)
        session.add(weibo_task)
    session.commit()


if __name__ == '__main__':
    run()