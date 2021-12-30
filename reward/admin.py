from django.contrib import admin
from django.forms import TextInput, Textarea
from django.utils.html import format_html

from .models import Position, Dept, Emp, Record, Reward
from openpyxl import Workbook
from django.http import HttpResponse, FileResponse
import datetime
from django.db import models


# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    list_display = ['p_id', 'p_name']
    list_filter = ['p_id', 'p_name']

    def has_delete_permission(self, request, obj=None):
        if str(request.user) != 'saduck':
            return False
        else:
            return True

    # actions = ['updatePosition']
    #
    # def updatePosition(self, request, queryset):
    #     print(request)
    #
    # # 显示的文本，与django admin一致
    # updatePosition.short_description = '更新数据'
    # # icon，参考element-ui icon与https://fontawesome.com
    # # custom_button.icon = 'fas fa-audio-description'
    #
    # # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    # updatePosition.type = 'primary'
    # updatePosition.acts_on_all = True


class DeptAdmin(admin.ModelAdmin):
    list_display = ['dept_id', 'dept_name']
    list_filter = ['dept_id', 'dept_name']

    def has_delete_permission(self, request, obj=None):
        if str(request.user) != 'saduck':
            return False
        else:
            return True


class EmpAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'emp_name', 'dept', 'p', 'emp_in_date', 'emp_out_date', 'emp_is_work', 'emp_rank',
                    'emp_base']
    raw_id_fields = ['dept', 'p']
    list_filter = ['emp_id', 'emp_name', 'dept', 'p']
    list_per_page = 10


class RecordAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size': '30'})},
    #     models.DateField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    # }

    list_display = ['rc', 'rc_b', 'dept', 'rc_cdates',
                    'leavedate', 'reward', 'rc_fdate', 'rc_fmoney', 'rc_bfmoney', 'rc_sdate', 'rc_smoney', 'rc_bsmoney',
                    'rc_tdate',
                    'rc_tmoney', 'rc_btmoney', 'rc_4date', 'rc_4money', 'rc_b4money']
    list_filter = ['rc__emp_name', 'rc_b__emp_is_work']
    raw_id_fields = ['rc', 'rc_b']
    # 添加按钮
    actions = ['download']

    def rc_cdates(self, obj):
        return obj.rc_cdate
        # return format_html('<span style="color:blue">{}</span>', obj.rc_cdate)

    rc_cdates.short_description = '创建日期'

    def dept(self, obj):
        # return format_html('<span style="width:5px">{}</span>', obj.rc_b.dept)
        return obj.rc_b.dept

    dept.short_description = "被推荐人部门"

    def leavedate(self, obj):
        return obj.rc_b.emp_out_date

    leavedate.short_description = "离职日期"

    def reward(self, obj):
        return obj.rc_b.r

    reward.short_description = "被推荐人奖励政策"

    def download(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        row1 = ['推荐人', '被推荐人', '奖励政策', '被推荐人部门', '创建日期', '入职日期', '离职日期', '第一次奖励日期', '第一次奖励金额', '被推荐人第一次奖励金额', '第二次奖励日期',
                '第二次奖励金额',
                '被推荐人第二次奖励金额', '第三次奖励日期', '第三次奖励金额', '被推荐人第三次奖励金额', '第四次奖励日期', '第四次奖励金额', '被推荐人第四次奖励金额']
        ws.append(row1)
        for datas in queryset:
            row2 = [
                str(datas.rc) if str(datas.rc) != "None" else "",
                str(datas.rc_b) if str(datas.rc_b) != "None" else "",
                str(datas.rc_b.r) if str(datas.rc_b.r) != "None" else "",
                str(datas.rc_b.dept) if str(datas.rc_b.dept) != "None" else "",
                str(datas.rc_cdate) if str(datas.rc_cdate) != "None" else "",
                str(datas.rc_b.emp_in_date) if str(datas.rc_b.emp_in_date) != "None" else "",
                str(datas.rc_b.emp_out_date) if str(datas.rc_b.emp_out_date) != "None" else "",
                str(datas.rc_fdate) if str(datas.rc_fdate) != "None" else "",
                str(datas.rc_fmoney) if str(datas.rc_fmoney) != "None" else "",
                str(datas.rc_bfmoney) if str(datas.rc_bfmoney) != "None" else "",
                str(datas.rc_sdate) if str(datas.rc_sdate) != "None" else "",
                str(datas.rc_smoney) if str(datas.rc_smoney) != "None" else "",
                str(datas.rc_bsmoney) if str(datas.rc_bsmoney) != "None" else "",
                str(datas.rc_tdate) if str(datas.rc_tdate) != "None" else "",
                str(datas.rc_tmoney) if str(datas.rc_tmoney) != "None" else "",
                str(datas.rc_btmoney) if str(datas.rc_btmoney) != "None" else "",
                str(datas.rc_4date) if str(datas.rc_4date) != "None" else "",
                str(datas.rc_4money) if str(datas.rc_4money) != "None" else "",
                str(datas.rc_b4money) if str(datas.rc_b4money) != "None" else ""
            ]
            ws.append(row2)
        wb.save('static/data.xlsx')
        #     下载
        file = open('static/data.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="record.xlsx"'
        return response

    # 显示的文本，与django admin一致
    download.short_description = '导出数据'
    # icon，参考element-ui icon与https://fontawesome.com
    # custom_button.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    download.type = 'primary'

    # 给按钮追加自定义的颜色
    # custom_button.style = 'color:black;'

    '''
    重写保存按钮
    1、如果当前有数据，则update
    2、如果没有数据，则insert,根据奖金规则，自动填写发放日期。金额由操作人员自行填写。
    '''

    def save_model(self, request, obj, form, change):
        '''
        :param request:原始网址中的数据就像GET
        :param obj: 根据obj.id判断是否为“None”，如果是“None”则表示insert，需要自动计算发放补贴的时间。如果不是“None”，则不需要计算，直接update
        :param form: 网页版数据，包含div啥的
        :param change:暂时不知道有什么用
        :return:
        '''
        print(type(obj.id))
        if obj.id is not None:
            Record.objects.filter(id=obj.id).update(rc=obj.rc.emp_id,
                                                    rc_b=obj.rc_b.emp_id,
                                                    rc_fdate=obj.rc_fdate,
                                                    rc_fmoney=obj.rc_fmoney,
                                                    rc_sdate=obj.rc_sdate,
                                                    rc_smoney=obj.rc_smoney,
                                                    rc_tdate=obj.rc_tdate,
                                                    rc_tmoney=obj.rc_tmoney,
                                                    rc_4date=obj.rc_4date,
                                                    rc_4money=obj.rc_4money,
                                                    rc_bfmoney=obj.rc_bfmoney,
                                                    rc_bsmoney=obj.rc_bsmoney,
                                                    rc_btmoney=obj.rc_btmoney,
                                                    rc_b4money=obj.rc_b4money
                                                    )
        else:
            # 是none，表示新增。新增的时候自动计算发奖金日期。
            # 根据今天日期，计算后续日期
            Record.objects.create(rc=obj.rc,
                                  rc_b=obj.rc_b,
                                  rc_cdate=obj.rc_cdate,
                                  rc_fdate=obj.rc_fdate,
                                  rc_fmoney=obj.rc_fmoney,
                                  rc_sdate=obj.rc_sdate,
                                  rc_smoney=obj.rc_smoney,
                                  rc_tdate=obj.rc_tdate,
                                  rc_tmoney=obj.rc_tmoney,
                                  rc_4date=obj.rc_4date,
                                  rc_4money=obj.rc_4money,
                                  rc_bfmoney=obj.rc_bfmoney,
                                  rc_bsmoney=obj.rc_bsmoney,
                                  rc_btmoney=obj.rc_btmoney,
                                  rc_b4money=obj.rc_b4money
                                  )


class RewardAdmin(admin.ModelAdmin):
    list_display = ['re_bdate', 're_edate', 're_money', 're_bmoney', 're_times', 're_desc']


admin.site.site_header = '润阳人事推荐奖励系统'
admin.site.site_title = '润阳人事推荐奖励系统'
admin.site.index_title = '欢迎使用润阳人事推荐奖励系统'
admin.site.register(Position, PositionAdmin)
admin.site.register(Dept, DeptAdmin)
admin.site.register(Emp, EmpAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Reward, RewardAdmin)
