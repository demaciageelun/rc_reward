# 返回供应商列表信息，用于新供应商申请物料价格
# 获取到请求后，发送原始数据给云之家互联控件
import time
import datetime

import flask, json
from flask import request
from functions import interfaces

'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
登录接口，需要传url、username、passwd
'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)

# 接收请求，获取数据库数据
'''
创建hr系统的接口。因为原系统只提供了视图，没有接口，操作很不方便。
接口分3个；
1、部门接口
2、岗位接口
3、人员接口
接口样式：{"table"："emp/position/dept","param":"字段名,字段名","filter":"过滤条件"}，分别代表员工、岗位、部门
返回参数样式：{"code":0/1,"data":[数据],"mes":"成功为空，不成功写明错误原因"} 0失败/1成功
'''


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


@server.route('/mssqlinterface', methods=['get', 'post'])
def mssqlinterface():
    print(request)
    data = request.get_data()
    print(data)
    datas = data.decode('utf8')
    jsondata = json.loads(datas)
    resu = interfaces.getdatafrommssql(jsondata['table'], jsondata['param'])
    print(json.dumps(resu, cls=DateEncoder))
    # resu = interfaces.getdatafrommssql(jsondata['table'], "Code,Name,DeptID,PostID,HireDate,DimissionDate,EmployeeStatusID")
    return json.dumps(resu, cls=DateEncoder)


if __name__ == '__main__':
    server.run(debug=True, port=36002, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
