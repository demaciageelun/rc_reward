from django.contrib import admin
from .models import Position, Dept, Emp, Record, Reward
from openpyxl import Workbook
from django.http import HttpResponse, FileResponse
import datetime


# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    list_display = ['p_name']


class DeptAdmin(admin.ModelAdmin):
    list_display = ['dept_name']

    def has_delete_permission(self, request, obj=None):
        if str(request.user) != 'saduck':
            return False
        else:
            return True


class EmpAdmin(admin.ModelAdmin):
    list_display = ['emp_name', 'dept', 'p', 'emp_in_date', 'emp_out_date', 'emp_is_work', 'emp_rank', 'emp_base']


class RecordAdmin(admin.ModelAdmin):
    list_display = ['rc', 'rc_b', 'pp', 'dept', 'rc_cdate',
                    'leavedate', 'rc_fdate', 'rc_fmoney', 'rc_bfmoney', 'rc_sdate', 'rc_smoney', 'rc_bsmoney',
                    'rc_tdate',
                    'rc_tmoney', 'rc_btmoney', 'rc_4date', 'rc_4money', 'rc_b4money']
    list_filter = ['rc__emp_name', 'p', 'rc_b__emp_is_work']
    raw_id_fields = ['rc', 'rc_b']
    # 添加按钮
    actions = ['custom_button']

    def custom_button(self, request, queryset):
        pass

    # 显示的文本，与django admin一致
    custom_button.short_description = '导出数据'
    # icon，参考element-ui icon与https://fontawesome.com
    # custom_button.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'primary'

    # 给按钮追加自定义的颜色
    # custom_button.style = 'color:black;'

    def dept(self, obj):
        return obj.rc_b.dept

    dept.short_description = "被推荐人部门"

    def leavedate(self, obj):
        return obj.rc_b.emp_out_date

    leavedate.short_description = "离职日期"

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
        if obj.id is not None:
            Record.objects.filter(id=obj.id).update(rc=obj.rc.emp_id,
                                                    rc_b=obj.rc_b.emp_id,
                                                    p=obj.p.id,
                                                    rc_fdate=obj.rc_fdate,
                                                    rc_fmoney=obj.rc_fmoney,
                                                    rc_sdate=obj.rc_sdate,
                                                    rc_smoney=obj.rc_smoney,
                                                    rc_tdate=obj.rc_tdate,
                                                    rc_tmoney=obj.rc_tmoney,
                                                    rc_4date=obj.rc_4date,
                                                    rc_4money=obj.rc_4money)
        else:
            # 是none，表示新增。新增的时候自动计算发奖金日期。
            # 根据今天日期，计算后续日期
            Record.objects.create(rc=obj.rc,
                                  rc_b=obj.rc_b,
                                  p=obj.p,
                                  rc_cdate=obj.rc_cdate,
                                  rc_fdate=obj.rc_fdate,
                                  rc_fmoney=obj.rc_fmoney,
                                  rc_sdate=obj.rc_sdate,
                                  rc_smoney=obj.rc_smoney,
                                  rc_tdate=obj.rc_tdate,
                                  rc_tmoney=obj.rc_tmoney,
                                  rc_4date=obj.rc_4date,
                                  rc_4money=obj.rc_4money)


class RewardAdmin(admin.ModelAdmin):
    list_display = ['re_bdate', 're_edate', 'p', 're_money', 're_bmoney', 're_times', 're_desc']
    raw_id_fields = ['p']


admin.site.site_header = '润阳人事推荐奖励系统'
admin.site.site_title = '润阳人事推荐奖励系统'
admin.site.index_title = '欢迎使用润阳人事推荐奖励系统'
admin.site.register(Position, PositionAdmin)
admin.site.register(Dept, DeptAdmin)
admin.site.register(Emp, EmpAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Reward, RewardAdmin)
