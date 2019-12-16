# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
import config
from  sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,TEXT,Text,DateTime,Date
from datetime import datetime

# engine = create_engine('mysql+pymysql://Joynice:liran123/@10.63.2.199:3306/wechat_1118?charset=utf8')
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base(engine)

class Comment(Base):
    '''
        爬取的微信公众号信息
    '''
    __tablename__ = 'ctrip_comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hotelName = Column(String(255), comment='酒店名称')
    hotelId = Column(String(255), comment='酒店ID')
    count = Column(Integer, comment='总页数')
    page = Column(Integer, comment='页数')
    baseRoomId = Column(Integer, comment='房间id')
    baseRoomName = Column(String(255), comment='房间类型名称')
    checkInDate = Column(String(255), comment='复测时间')
    content = Column(Text, comment='评论内容')
    imageList = Column(String(255), comment='图片列表')
    feedcontent = Column(String(255), comment='公众号中文名')

    postDate = Column(String(255), comment='时间')
    ratingPoint = Column(String(255), comment='评分')
    ratingPointDesc = Column(String(255), comment='点评')
    travelType = Column(String(255), comment='旅行方式')
    userNickName = Column(String(255), comment='用户名')
    userCommentCount = Column(String(255), comment='用户评价数量')
    spider_time = Column(DateTime,default=datetime.now, comment='爬取时间')


if __name__ == '__main__':


    Base.metadata.drop_all()
    Base.metadata.create_all()