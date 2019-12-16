
#!/usr/bin/python3
# Author: Conyyon
# Date: 2019.03.10 17:26
# Software: PyCharm

import time
import requests
from pprint import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}

# 配置微博用户的UID（具体方法：PC端打开用户微博个人界面，右键查看源代码，搜索 $CONFIG['oid'] ,后面的数据即为下面的UID）
UID = '1644285801'


def get_url():
    """
    返回请求接口的URL
    :return:URL
    """
    index_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(UID)
    return index_url


def get_user_info():
    """
    获取用户信息
    :return: 用户信息、containerid参数
    """
    index_url = get_url()
    index_ret = requests.get(index_url, headers=headers).json()
    userInfo = index_ret['data']['userInfo']
    # 个人信息
    person_info = {
        # 头像高清
        # 'avatar_hd': userInfo.get('avatar_hd'),
        # 手机微博背景图片
        # 'cover_image_phone': userInfo.get('cover_image_phone'),
        # 个人描述
        'description': userInfo.get('description'),
        # 关注人数
        'follow': userInfo.get('description'),
        # 微博总数
        'statuses_count': userInfo.get('statuses_count'),
        # 是否关注当前登录用户
        # 'follow_me': userInfo.get('follow_me'),
        # 粉丝数量
        'followers_count': userInfo.get('followers_count'),
        'follow_count': userInfo.get('follow_count'),
        # 性别 m：男、f：女、n：未知
        'gender': userInfo.get('gender'),
        # id
        'id': userInfo.get('id'),
        # 用户头像地址（中图），50×50像素
        # 'profile_image_url': userInfo.get('profile_image_url'),
        # 微博统一URL地址
        # 'profile_url': userInfo.get('profile_url'),
        # 用户昵称
        'screen_name': userInfo.get('screen_name'),
        # 是否是微博认证用户，即加V用户
        'verified': userInfo.get('verified'),
        # 认证原因
        'verified_reason': userInfo.get('verified_reason')
    }
    # 在当前页面获取containerid参数，作为下文获取微博信息的必要参数

    return  person_info




if __name__ == '__main__':
    pprint(get_user_info())
