#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： run_test_main.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018/5/19 下午3:43
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------
"""
    生成接口测试报告
"""
import os
import time
import ruamel_yaml
import unittest
from test.interface_test_code import modelClassCreate
from test.utils.HTMLTestRunner_Py3 import HTMLTestRunner


def endWith(s, *endstring):
    array = map(s.endswith, endstring)
    if True in array:
        return True
    else:
        return False


def interface_code():
    path = os.getcwd() + '/test/config/'
    s = os.listdir(path)
    for i in s:
        if endWith(i, '.yaml'):
            file = open(path + i, encoding='utf-8')
            yaml_json_data = ruamel_yaml.safe_load(file)
            modelClassCreate(yaml_json_data)
            print('接口测试代码已生成，配置文件：%s' % (i))


def test_report():
    test_dir = './test/test_code/'
    #   discover 是一个自动化的过程，将目标路径下，自动匹配test*.py文件作为测试用例
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='Test*.py')
    NOW = time.strftime("%Y-%m-%d %H:%M:%S")
    FILENAME = './test/report/' + 'Map_' + 'API_Test_' + NOW + '_result.html'
    FP = open(FILENAME, 'wb')
    RUNNER = HTMLTestRunner(stream=FP,
                            title='后排辅助者(app_map)测试报告',
                            description='用例执行情况：')

    RUNNER.run(discover)


if __name__ == "__main__":
    interface_code()
    test_report()
