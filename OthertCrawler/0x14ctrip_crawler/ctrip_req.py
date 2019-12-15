#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/12/9 0009'

"""
import random
from time import sleep

from sqlalchemy.orm import sessionmaker

from models import Comment
from models import engine

Session = sessionmaker(bind=engine)
session = Session()

import requests


def fetchCmts(hotel, page):
    url = "https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031074110034723384"
    headers = {
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://m.ctrip.com',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }

    formData = {
        'groupTypeBitMap': '2',
        'hotelId': str(hotel),
        'pageIndex': str(page),
        'pageSize': '10',
        'travelType': '-1',  # -1 表示全部，家庭亲子为 30
    }
    try:
        r = requests.post(url, data=formData, headers=headers)  # formData,
        r.raise_for_status()
        r.encoding = "utf-8"

        return r.json()
    except:
        pass


def do_work(id):
    page = 0
    while True:
        page = page + 1
        if page % 10 == 0:
            print('【页数】', page)
            sleep(random.randint(3, 5))
        result = (fetchCmts(id, page=page))
        print(result)
        hotelName = result.get('hotelName')
        if hotelName:

            print(hotelName)
            count = result.get('travelTypeFitlerList')[0].get('count')
            othersCommentList = result.get('othersCommentList')

            if not othersCommentList:
                break
            for i in othersCommentList:
                # print('第个',i)
                baseRoomId = i.get('baseRoomId')
                baseRoomName = i.get('baseRoomName')
                checkInDate = i.get('checkInDate')
                content = i.get('content')
                feedbackList = i.get('feedbackList')
                # print('【店家评论】',feedbackList)
                feedcontent = ''
                if feedbackList:
                    feedcontent = feedbackList[0].get('content')
                imageList = i.get('imageList')
                postDate = i.get('postDate')
                ratingPoint = i.get('ratingPoint')
                ratingPointDesc = i.get('ratingPointDesc')
                travelType = i.get('travelType')
                userNickName = i.get('userNickName')
                userCommentCount = i.get('userCommentCount')
                hotelId = id
                print('【信息】', hotelName, hotelId, count, page, content, postDate)
                comment = Comment(
                    hotelName=hotelName,
                    hotelId=hotelId,
                    count=count,
                    page=page,
                    baseRoomId=baseRoomId,
                    baseRoomName=baseRoomName,
                    checkInDate=checkInDate,
                    content=content,
                    imageList=str(imageList),
                    feedcontent=feedcontent,
                    postDate=postDate,
                    ratingPoint=ratingPoint,
                    ratingPointDesc=ratingPointDesc,
                    travelType=travelType,
                    userNickName=userNickName,
                    userCommentCount=userCommentCount,

                )
                session.add(comment)
            session.commit()
            print('【一页采集完成】')
        else:
            break


if __name__ == '__main__':

    with open('doworkbak.txt', 'r+')as f:
        hosts = f.read().split('\n')
    for i in hosts:
        print(i)
        do_work(i)
