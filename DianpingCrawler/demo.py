#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/3/21 0021'

"""

from dazhong import DianpingComment

COOKIES = '_lxsdk_cuid=1699b152d90c8-04b0ee8b481697-541f3415-1fa400-1699b152d91c8; _lxsdk=1699b152d90c8-04b0ee8b481697-541f3415-1fa400-1699b152d91c8; _hc.v=992d8c67-a9b0-ee61-c6cf-ed9b42cfe11f.1553085051; _thirdu.c=136cbfec8b174105c45f6628ce431df6; ctu=cc29f77c02b4556c6a1db1c67c5c10e084f7f63d00208c59788c11a4845348aa; cy=160; cye=zhengzhou; thirdtoken=e0dfd5bf-3cc9-482c-a559-ecb5a5408581; dper=13f0e16d38f4829e80270687b88c4ce8d36d333a6f525bc6be3dec9bbc60b1d7f44f8b47a413dc1c18f3ef5fed921594f3c5161e72d50fed52f3006625babe559507c56bb8b77d1f9dd95d104ffb3cdba1c49805e34df17c99e3ba781183b850; ll=7fd06e815b796be3df069dec7836c3df; ua=aJay13; ctu=a5f067d1428ce75e417e53634b352a7767a63503c85b2d59c0c70ae996add3e701d656899061b0eddfa568430b723553; _lxsdk_s=1699df6ef73-4f6-781-d9c%7C%7C719'


class Customer(DianpingComment):

    def _data_pipeline(self, data):
        print(data)
        with open('code_dict.txt','a+',encoding='utf-8')as f:
            f.write(str(data)+'\n')


if __name__ == "__main__":
    dianping = Customer('1726435', cookies=COOKIES)
    dianping.run()