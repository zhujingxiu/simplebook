#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/5/22


def random_str(length=8):
    '''
    随机字符
    :return:
    '''
    import random
    import string
    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))