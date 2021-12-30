import json
from urllib import parse

import requests
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# 从接口获取数据
def getdatafrominter(request):
    url = "http://127.0.0.1:36001/mssqlinterface"
    d = {"table": "T_HR_Department", "param": "DepartmentCode,DepartmentName"}
    r = requests.get(url=url, data=json.dumps(d))
    retu_data = r.json()
    print(retu_data)
    return HttpResponse({"success": "true"})
