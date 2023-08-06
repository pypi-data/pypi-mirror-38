#coding: utf-8
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： TestMapHistoryDeletePoiHistory.py
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


class TestMapHistoryDeletePoiHistory(unittest.TestCase):
    u"""测试接口：删除POI历史记录"""
    
    def setUp(self):
        self.um = UnitMain()
        
    def tearDown(self):
        self.um.dispose()
        self.um = None
    
    def test_deletePoiHistory_1(self):
        u"""字段输入异常 poi_id keywords 输入关键字段过多"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "B00155KSDE", "keywords": "酒店", "timestamp": 1515377061.875, "location": "121.18705063770875, 31.281607023362948"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21027))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21027)

    def test_deletePoiHistory_2(self):
        u"""字段输入异常  poi_id and keywords 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "", "keywords": "", "timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21028))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21028)

    def test_deletePoiHistory_3(self):
        u"""字段输入异常 keywords 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"timestamp": 1515377061.875, "location": "121.842506,31.779192"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21028))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21028)

    def test_deletePoiHistory_4(self):
        u"""字段输入异常 poi_id 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "", "timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21028))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21028)

    def test_deletePoiHistory_5(self):
        u"""字段异常  poi_id and keywords 缺失"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "\n""     %s" % (ip + url))
        print("Headers：" + "\n""     %s" % (headers))
        print("Body：" + "\n""     %s" % (data))
        print("Desired_value：" + "\n""     %s" % (21028))
        print("Response_value：" + "\n""     %s" % (self.um.get_start()[0]))
        print("Time：" + "\n""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "\n""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], 21028)

    def test_deletePoiHistory_6(self):
        u"""字段输入正确 关键字输入，poi_id 未输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "" ,"keywords": "酒店", "timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
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

    def test_deletePoiHistory_7(self):
        u"""字段输入正确 关键字未输入，poi_id 输入"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "B00155KSDE", "keywords": "", "timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
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

    def test_deletePoiHistory_8(self):
        u"""字段输入正确 关键字输入，poi_id 不存在"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"keywords": "酒店", "timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
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

    def test_deletePoiHistory_9(self):
        u"""字段输入正确 poi_id输入，关键字 不存在"""
        ip = "http://47.100.220.189:8888"
        url = "/map/poihistory/delete"
        headers = {'Vin': 'LSJA1234567890118', 'User_id': '123456'}
        data = {"poi_id": "B00155KSDE", "timestamp": 1515377061.875, "location": "121.18705063770875,31.281607023362948"}
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
