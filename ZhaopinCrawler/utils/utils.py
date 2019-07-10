# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import time

def get_header():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

def get_time():
    return int(time.time())