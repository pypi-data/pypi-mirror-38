#coding: utf-8
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： TestMapSearchIdDetail.py
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


class TestMapSearchIdDetail(unittest.TestCase):
    u"""测试接口：POI详情信息"""
    
    def setUp(self):
        self.um = UnitMain()
        
    def tearDown(self):
        self.um.dispose()
        self.um = None
    
    def test_iddetail_1(self):
        u"""字段输入异常 poi_id 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/iddetail"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "", "timestamp": 1515377061.875, "location": "121.1928650000,31.2794500000"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21026))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21026)

    def test_iddetail_2(self):
        u"""字段异常 poi_id 字段丢失"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/iddetail"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"timestamp": 1515377061.875, "location": "121.1928650000,31.2794500000"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21020))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21020)

    def test_iddetail_3(self):
        u"""字段输入正确"""
        ip = "http://47.100.220.189:8888"
        url = "/map/search/iddetail"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "B00156G7QT", "timestamp": 1515377061.875, "location": "121.1928650000,31.2794500000"}
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

    def test_iddetail_4(self):
        u"""字段输入异常 经纬度 未输入  """
        ip = "http://47.100.220.189:8888"
        url = "/map/search/iddetail"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "B00156G7QT", "timestamp": 1515377061.875, "location":""}
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
