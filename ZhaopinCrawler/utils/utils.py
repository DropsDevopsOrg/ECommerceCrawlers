# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from faker import Faker
user_agent = Faker('zh-CN').user_agent()

import time

def get_header():
    return {
        'User-Agent': user_agent
    }

def get_time():
    return int(time.time())