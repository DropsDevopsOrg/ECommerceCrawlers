import config
from  sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,TEXT,Text,DateTime,Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(engine)


class WeiboInfo(Base):
    '''
        爬取的微博信息
    '''
    __tablename__ = 't_weibo_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_url = Column(String(255), comment='微博页面链接')
    name = Column(String(255), comment='微博人名称')
    name_link = Column(String(255),  comment='微博人链接')
    weibo_from = Column(String(255), comment='微博来自')
    txt = Column(TEXT, comment='微博内容')
    feed_list_forward = Column(String(255), default='0',comment='转发量')
    feed_list_comment = Column(String(255), default='0',comment='评论量')
    feed_list_like = Column(String(255), default='0',comment='点赞量')
    search_time = Column(String(255),  comment='搜索时间')
    is_V = Column(String(255),  comment='是否大v')
    sex = Column(String(255),  comment='性别')
    area = Column(String(255),  comment='省份')
    fans = Column(String(255),  comment='粉丝数')
    flows = Column(String(255),  comment='关注数')
    page_frame = Column(String(255),  comment='总发帖数')
    des = Column(String(2550),  comment='个性描述')
    flag = Column(String(255),  comment='标志')
    spider_time = Column(DateTime,default=datetime.now, comment='上次爬取时间')

class WeiboTask(Base):
    '''
        爬取的任务信息
    '''
    __tablename__ = 't_weibo_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    between = Column(String(255), comment='时间范围')
    url = Column(String(255), comment='爬取连接')
    flag = Column(String(255), comment='是否爬取 0 没爬取 1 正在爬取、2爬取成功、3爬取失败 4没有数据')
    time = Column(String(255), comment='时间')
if __name__ == '__main__':

    Base.metadata.drop_all()
    Base.metadata.create_all()
