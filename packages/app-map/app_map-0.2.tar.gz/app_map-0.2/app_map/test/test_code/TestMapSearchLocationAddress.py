#coding: utf-8
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： TestMapSearchLocationAddress.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018-09-06 13:47:24
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------
import unittest
import datetime
import time
from test.requests_code.unittest_Interface import UnitMain


class TestMapSearchLocationAddress(unittest.TestCase):
    u"""测试接口：GPS周边搜索"""
    
    def setUp(self):
        self.um = UnitMain()
        
    def tearDown(self):
        self.um.dispose()
        self.um = None
    
    def test_locationaddress_1(self):
        u"""字段输入异常 location 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/locationaddress"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"timestamp": 1515377061.875, "location": ""}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21025))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21025)

    def test_locationaddress_2(self):
        u"""字段异常 location 字段丢失"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/locationaddress"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"page": "1", "timestamp": 1515377061.875}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21019))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21019)

    def test_locationaddress_3(self):
        u"""字段输入正确"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/locationaddress"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"page": "1", "timestamp": 1515377061.875, "location": "121.1928650000,31.2794500000"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (0))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 0)

    def test_locationaddress_4(self):
        u"""字段输入异常 page 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/locationaddress"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"page": "", "timestamp": 1515377061.875, "location": "121.1928650000,31.2794500000"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (0))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 0)

    
if __name__ == "__main__":
    unittest.main()
