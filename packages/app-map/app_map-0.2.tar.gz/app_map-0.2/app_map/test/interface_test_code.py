#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： interface_test_code.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018/8/29 下午2:18
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------
import time
from string import Template


# 动态生成单个测试用例函数字符串
def singleMethodCreate(MethodList, interfaceNamePara):
    code = Template('''\n    def test_${testcase}(self):
        u"""${testcaseName}"""
        ip = "${ip}"
        url = "${url}"
        headers = ${headers}
        data = ${data}
        start_time = datetime.datetime.now()
        self.um.interface_requests(ip, url, headers=headers, body=data)
        end_time = datetime.datetime.now()
        print()
        print("Path：" + "${line_bareak1}""     %s" % (ip + url))
        print("Headers：" + "${line_bareak1}""     %s" % (headers))
        print("Body：" + "${line_bareak1}""     %s" % (data))
        print("Desired_value：" + "${line_bareak1}""     %s" % ($body_error_num))
        print("Response_value：" + "${line_bareak1}""     %s" % (self.um.get_start()[0]))
        print("Time：" + "${line_bareak1}""     %s" % (str((end_time - start_time).total_seconds()) + "秒"))
        print("Res：" + "${line_bareak1}""     %s" % (self.um.get_start()[1]))
        print("————————————————————————————————————————————————————————————————————")
        print("")
        self.assertEqual(self.um.get_start()[0], $body_error_num)
''')

    string = code.substitute(testcase=MethodList["testcase"], testcaseName=MethodList["testcasename"],
                             method=MethodList['method'], ip=MethodList['ip'], url=MethodList['url'],
                             headers=MethodList['headers'],
                             data=MethodList['body_'],
                             body_error_num=MethodList['body_error_num'],
                             line_bareak1="\\n",
                             line_bareak2='\t',
                             )
    return string


# 拼接单个的测试用例函数字符串为完整字符串并传回主函数
# MethodParaList获取测试用例部分list
def methodCreate(MethodParaList, interfaceNamePara):
    string = ""
    for MethodPara in MethodParaList:
        string2 = singleMethodCreate(MethodPara, interfaceNamePara)
        string = string + string2
    return string


# 构造单个测试集
def singleTestsuitCreate(MethodList, parameters):
    code = Template('''suite.addTest(${className}("test_${testcase}"))''')
    string = code.substitute(testcase=MethodList["testcase"], className=parameters['className'])
    return string


# 添加测试集
def addtestsuit(MethodParaList, interfaceNamePara):
    string = ""
    for MethodPara in MethodParaList:
        string2 = singleTestsuitCreate(MethodPara, interfaceNamePara)
        string = string + string2
    return string


# 生成测试用例类函数字符串
def modelClassCreate(parameters):
    modelCode = methodCreate(parameters['body'], parameters['interfaceName'])
    adtestsuit = addtestsuit(parameters['body'], parameters)
    code = Template('''#coding: utf-8
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： ${className}.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      ${time}
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


class ${className}(unittest.TestCase):
    u"""测试接口：${interfaceName}"""
    
    def setUp(self):
        self.um = UnitMain()
        
    def tearDown(self):
        self.um.dispose()
        self.um = None
    ${model}
    
if __name__ == "__main__":
    unittest.main()
''')
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    fileStr = code.substitute(className=parameters['className'], interfaceName=parameters['interfaceName'],
                              testsuite=adtestsuit,
                              model=modelCode, time=create_time)
    f = open("./test/test_code/" + parameters['className'] + ".py", 'w',encoding='utf-8')
    f.write(fileStr)
    f.close()
