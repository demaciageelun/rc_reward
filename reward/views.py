import json
from base64 import decode
from urllib import parse

import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import Dept, Position, Emp


# from functions import insertdata

# Create your views here.
# 从接口获取数据，并写入系统中，包含岗位，部门，人员。
def getdatafrominter(request):
    url = "http://127.0.0.1:36002/mssqlinterface"
    # d = {"table": "T_HR_Department", "param": "id,DepartmentCode,DepartmentName,D_glgs"}
    # d = {"table": "t_hr_post", "param": "id,PostCode,PostName,IfUse"}
    # d = {"table": "t_hr_employee", "param": "Code,Name,DeptID,PostID,HireDate,DimissionDate,EmployeeStatusID"}
    # 从定时任务中获取任务，从接口取数据
    d = json.loads(request.body.decode('utf8'))
    print(d)
    r = requests.get(url=url, data=json.dumps(d))
    retu_data = r.json()
    print(retu_data['data'])
    # 部门，进dept
    if d['table'] == 'T_HR_Department':
        for datas in retu_data['data']:
            Dept.objects.update_or_create(
                defaults={
                    'id': datas[0],
                    'dept_id': datas[1],
                    'dept_name': datas[2],
                    'dept_base': datas[3]
                },
                id=datas[0]
            )
    # 岗位进position
    if d['table'] == 't_hr_post':
        for datas in retu_data['data']:
            Position.objects.update_or_create(
                defaults={
                    'id': datas[0],
                    'p_id': datas[1],
                    'p_name': datas[2],
                },
                id=datas[0]
            )
    # emp进员工信息表
    if d['table'] == 't_hr_employee':
        for datas in retu_data['data']:
            print(datas[1])
            try:
                dept = Dept.objects.get(id=datas[2])
            except Exception as e:
                dept = Dept.objects.get(id=23333)
                print(dept)
                print(e)

            try:
                p = Position.objects.get(id=datas[3])
            except Exception as e:
                print(e)
                p = Position.objects.get(id=1)
            Emp.objects.update_or_create(
                defaults={
                    'emp_id': datas[0],
                    'emp_name': datas[1],
                    'dept': dept,
                    'p': p,
                    'emp_in_date': datas[4],
                    'emp_out_date': datas[5],
                    'emp_is_work': datas[6]
                },
                emp_id=datas[0]
            )
    return HttpResponse({"success": "true"})
