#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = ''
__mtime__ = ''


from .smtp_send import send

if __name__ == "__main__":
    send('smtp.263.net:465', ['测试员', 'wujh@ebfcn.com.cn'], '19D5B6fDB635Ac3f', ['linyl@ebfcn.com.cn', 'wujh@ebfcn.com.cn'], [], '标题', '内网测试', [])
