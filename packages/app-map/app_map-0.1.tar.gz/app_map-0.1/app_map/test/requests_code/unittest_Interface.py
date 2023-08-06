#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： unittest_Interface.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018/8/28 下午2:20
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------

import requests


class UnitMain:

    def __init__(self):
        self.err_no = 0
        self.res = None

    def get_start(self):
        return self.err_no, self.res

    def interface_requests(self, ip, url, headers, body):
        api_url = ip + url
        res = requests.post(url=api_url, json=body, headers=headers)
        self.err_no = int(res.headers._store['status_code'][1])
        self.res = res

    def dispose(self):
        """

        :return:
        """
        pass
