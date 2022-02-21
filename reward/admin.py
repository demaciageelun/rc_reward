import datetime
import arrow
from django.contrib import admin
# from django.forms import TextInput, Textarea
# from django.utils.html import format_html
from .models import Position, Dept, Emp, Record, Reward, InterviewAccount, JobLevel, LeaveReason
from openpyxl import Workbook
from django.http import FileResponse
from import_export.admin import ImportExportModelAdmin
import datetime


# Register your models here.
class DeptAdmin(ImportExportModelAdmin):
    list_display = ['dept_id', 'dept_name', 'dept_base']
    list_filter = ['dept_id', 'dept_name', 'dept_base']

    def has_delete_permission(self, request, obj=None):
        if str(request.user) != 'saduck':
            return False
        else:
            return True


class JobLevelAdmin(ImportExportModelAdmin):
    list_display = ['level_code', 'level_name']

    def has_delete_permission(self, request, obj=None):
        if str(request.user) != 'saduck':
            return False
        else:
            return True


class PositionAdmin(ImportExportModelAdmin):
    list_display = ['p_id',
                    'p_name']
    search_fields = ['p_id',
                     'p_name']

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


class EmpAdmin(ImportExportModelAdmin):
    list_display = ['emp_id', 'emp_name', 'dept', 'emp_base', 'p', 'level', 'emp_in_date', 'emp_out_date',
                    'emp_is_work']
    raw_id_fields = ['dept', 'p', 'level']
    list_filter = ['dept', 'p', 'dept__dept_base', 'emp_is_work']
    search_fields = ['emp_id', 'emp_name']
    list_per_page = 10

    # list_select_related = ['emp_name']
    # show_full_result_count = False

    def emp_base(self, obj):
        return obj.dept.dept_base

    emp_base.short_description = '所属基地'
    # list_max_show_all = 10


class RecordAdmin(ImportExportModelAdmin):
    list_display = ['rc', 'rc_b', 'dept', 'p', 'rc_cdate', 'indate', 'leavedate', 'rc_fdate', 'rc_fmoney',
                    'rc_bfmoney', 'rc_sdate', 'rc_smoney', 'rc_bsmoney', 'rc_tdate', 'rc_tmoney', 'rc_btmoney',
                    'rc_4date', 'rc_4money', 'rc_b4money', 'rc_issued', 'rc_notissued', 'rc_bissued', 'rc_bnotissued']
    search_fields = ['rc__emp_id', 'rc__emp_name', 'rc_b__emp_id', 'rc_b__emp_name']
    list_filter = ['rc_cdate', 'rc_b__emp_is_work']
    raw_id_fields = ['rc', 'rc_b']
    list_per_page = 10
    # 重写显示的数据内容，可根据不同登录用户，显示不同基地的人员信息。
    # def get_queryset(self, request):
    #     qs = super(RecordAdmin, self).get_queryset(request)
    #     if str(request.user) != 'saduck':
    #         return qs.filter(creater=str(request.user))
    #     else:
    #         return qs

    # 添加按钮
    actions = ['download', 'calc']

    def dept(self, obj):
        # return format_html('<span style="width:5px">{}</span>', obj.rc_b.dept)
        return obj.rc_b.dept

    dept.short_description = "被推荐人部门"

    def leavedate(self, obj):
        return obj.rc_b.emp_out_date

    leavedate.short_description = "被推荐人离职日期"

    def indate(self, obj):
        return obj.rc_b.emp_in_date

    indate.short_description = "被推荐人入职日期"

    def download(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        row1 = ['推荐人基地',
                '推荐人工号',
                '推荐人姓名',
                '推荐人部门',
                '推荐人岗位',
                '推荐人入职日期',
                '推荐人离职日期',
                '推荐人在职状态',
                '推荐人应付奖金',
                '第一次发放日期',
                '推荐人第一次奖励金额',
                '第二次发放日期',
                '推荐人第二次奖励金额',
                '第三次发放日期',
                '推荐人第三次奖励金额',
                '第四次发放日期',
                '推荐人第四次奖励金额',
                '推荐人已发放金额合计',
                '推荐人未发放金额合计',
                '被推荐人基地',
                '被推荐人工号',
                '被推荐人姓名',
                '被推荐人部门',
                '被推荐人岗位',
                '被推荐人职级',
                '被推荐人入职日期',
                '被推荐人离职日期',
                '被推荐人在职状态',
                '第一次发放日期',
                '被推荐人第一次奖励金额',
                '第二次发放日期',
                '被推荐人第二次奖励金额',
                '第三次发放日期',
                '被推荐人第三次奖励金额',
                '第四次发放日期',
                '被推荐人第四次奖励金额',
                '被推荐人已发放金额合计',
                '被推荐人未发放金额合计',
                ]
        ws.append(row1)
        for datas in queryset:
            row2 = [
                str(datas.rc.dept.dept_base) if str(datas.rc.dept.dept_base) != "None" else "",  # 推荐人基地
                str(datas.rc.emp_id) if str(datas.rc.emp_id) != "None" else "",  # 推荐人工号
                str(datas.rc) if str(datas.rc) != "None" else "",  # 推荐人姓名
                str(datas.rc.dept) if str(datas.rc.dept) != "None" else "",  # 推荐人部门
                str(datas.rc.p) if str(datas.rc.p) != "None" else "",  # 推荐人岗位
                str(datas.rc.emp_in_date) if str(datas.rc.emp_in_date) != "None" else "",  # 推荐人入职日期
                str(datas.rc.emp_out_date) if str(datas.rc.emp_out_date) != "None" else "",  # 推荐人离职日期
                "在职" if str(datas.rc.emp_is_work) == "1" else "离职",  # 推荐人在职状态
                str(datas.p.re_money) if str(datas.p.re_money) != "None" else "",  # 推荐人应付奖金
                str(datas.rc_fdate) if str(datas.rc_fdate) != "None" else "",  # 第一次发放日期
                str(datas.rc_fmoney) if str(datas.rc_fmoney) != "None" else "",  # 推荐人第一次发放金额
                str(datas.rc_sdate) if str(datas.rc_sdate) != "None" else "",  # 第二次发放日期
                str(datas.rc_smoney) if str(datas.rc_smoney) != "None" else "",  # 推荐人第二次发放金额
                str(datas.rc_tdate) if str(datas.rc_tdate) != "None" else "",  # 第三次发放日期
                str(datas.rc_tmoney) if str(datas.rc_tmoney) != "None" else "",  # 推荐人第三次发放金额
                str(datas.rc_4date) if str(datas.rc_4date) != "None" else "",  # 第四次发放日期
                str(datas.rc_4money) if str(datas.rc_4money) != "None" else "",  # 推荐人第四次发放金额
                str(datas.rc_issued) if str(datas.rc_issued) != "None" else "",  # 推荐人已发放金额合计
                str(datas.rc_notissued) if str(datas.rc_notissued) != "None" else "",  # 推荐人未发放金额合计
                str(datas.rc_b.dept.dept_base) if str(datas.rc_b.dept.dept_base) != "None" else "",  # 被推荐人基地
                str(datas.rc_b.emp_id) if str(datas.rc_b.emp_id) != "None" else "",  # 被推荐人工号
                str(datas.rc_b) if str(datas.rc_b) != "None" else "",  # 被推荐人姓名
                str(datas.rc_b.dept) if str(datas.rc_b.dept) != "None" else "",  # 被推荐人部门
                str(datas.rc_b.p) if str(datas.rc_b.p) != "None" else "",  # 被推荐人岗位
                str(datas.rc_b.emp_rank) if str(datas.rc_b.emp_rank) != "None" else "",  # 被推荐人职级
                str(datas.rc_b.emp_in_date) if str(datas.rc_b.emp_in_date) != "None" else "",  # 被推荐人入职日期
                str(datas.rc_b.emp_out_date) if str(datas.rc_b.emp_out_date) != "None" else "",  # 被推荐人离职日期
                "在职" if str(datas.rc_b.emp_is_work) == "1" else "离职",  # 被推荐人在职状态
                str(datas.rc_fdate) if str(datas.rc_fdate) != "None" else "",  # 第一次发放日期
                str(datas.rc_bfmoney) if str(datas.rc_bfmoney) != "None" else "",  # 推荐人第一次发放金额
                str(datas.rc_sdate) if str(datas.rc_sdate) != "None" else "",  # 第二次发放日期
                str(datas.rc_bsmoney) if str(datas.rc_bsmoney) != "None" else "",  # 推荐人第二次发放金额
                str(datas.rc_tdate) if str(datas.rc_tdate) != "None" else "",  # 第三次发放日期
                str(datas.rc_btmoney) if str(datas.rc_btmoney) != "None" else "",  # 推荐人第三次发放金额
                str(datas.rc_4date) if str(datas.rc_4date) != "None" else "",  # 第四次发放日期
                str(datas.rc_b4money) if str(datas.rc_b4money) != "None" else "",  # 推荐人第四次发放金额
                str(datas.rc_bissued) if str(datas.rc_bissued) != "None" else "",
                str(datas.rc_bnotissued) if str(datas.rc_bnotissued) != "None" else "",
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
    download.short_description = '下载数据'
    # icon，参考element-ui icon与https://fontawesome.com
    # custom_button.icon = 'fas fa-audio-description'
    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    download.type = 'success'
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
        if obj.id is not None:
            Record.objects.filter(id=obj.id).update(rc=obj.rc.emp_id,
                                                    rc_b=obj.rc_b.emp_id,
                                                    p=obj.p,
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
                                                    rc_b4money=obj.rc_b4money,
                                                    rc_issued=obj.rc_issued,
                                                    rc_notissued=obj.rc_notissued,
                                                    rc_bissued=obj.rc_bissued,
                                                    rc_bnotissued=obj.rc_bnotissued,
                                                    )
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
                                  rc_4money=obj.rc_4money,
                                  rc_bfmoney=obj.rc_bfmoney,
                                  rc_bsmoney=obj.rc_bsmoney,
                                  rc_btmoney=obj.rc_btmoney,
                                  rc_b4money=obj.rc_b4money,
                                  rc_issued=obj.rc_issued,
                                  rc_notissued=obj.rc_notissued,
                                  rc_bissued=obj.rc_bissued,
                                  rc_bnotissued=obj.rc_bnotissued,
                                  creater=request.user
                                  )

    # 新增计算按钮，手动计算金额发放情况。
    # 遍历根据入职日期、离职日期、奖金详情，计算当前已发放的月份和金额，并计算已发放合计、未发放合计。
    def calc(self, request, queryset):
        for data in queryset:
            # 依次取出每行的被推荐人入职日期，离职日期，奖金政策
            out_data = data.rc.emp_out_date  # 推荐人离职日期
            bin_date = data.rc_b.emp_in_date  # 被推荐人入职日期
            bout_date = data.rc_b.emp_out_date  # 被推荐人离职日期
            bonus = data.p.re_money  # 推荐人奖金
            bonus_b = data.p.re_bmoney if data.p.re_bmoney is not None else 0  # 被推荐人奖金
            # bonus_b = data.p.re_bmoney  # 被推荐人奖金
            date_1 = data.p.re_time1  # 第一次发放月
            date_2 = data.p.re_time2  # 第二次发放月
            date_3 = data.p.re_time3  # 第三次发放月
            date_4 = data.p.re_time4  # 第四次发放月
            # 如果当前推荐人和被推荐人都没离职，则继续计算
            if out_data is None and bout_date is None:
                # 计算奖金分几次发
                give_times = 0
                if date_1 is not None:
                    give_times += 1
                if date_2 is not None:
                    give_times += 1
                if date_3 is not None:
                    give_times += 1
                if date_4 is not None:
                    give_times += 1
                # 计算发放金额
                indiv_bonus = bonus / give_times  # 推荐人每次发放金额
                bindiv_bonus = 0
                if bonus_b is not None:
                    bindiv_bonus = bonus_b / give_times  # 被推荐人每次发放金额
                # 计算发放日期，根据被推荐人入职日期和每次分发的月计算。距离当前日期在一个月之内的，填写发放金额。
                rc_fdate = None
                rc_sdate = None
                rc_tdate = None
                rc_4date = None
                rc_fmoney = 0
                rc_smoney = 0
                rc_tmoney = 0
                rc_4money = 0
                rc_bfmoney = 0
                rc_bsmoney = 0
                rc_btmoney = 0
                rc_b4money = 0
                bin_date = arrow.get(str(bin_date), 'YYYY-MM-DD')
                if date_1 is not None:
                    rc_fdate = str(bin_date.shift(months=1 + date_1).date())[:8] + "15"  # 发放日期1
                    date1 = arrow.get(rc_fdate, 'YYYY-MM-DD').date()
                    date2 = arrow.now().date()
                    if (date1 - date2).days < 20:
                        rc_fmoney = indiv_bonus  # 推荐人奖金1
                        rc_bfmoney = bindiv_bonus  # 被推荐人奖金1
                if date_2 is not None:
                    rc_sdate = str(bin_date.shift(months=1 + date_2).date())[:8] + "15"  # 发放日期2
                    date1 = arrow.get(rc_sdate, 'YYYY-MM-DD').date()
                    date2 = arrow.now().date()
                    if (date1 - date2).days < 20:
                        rc_smoney = indiv_bonus  # 推荐人奖金2
                        rc_bsmoney = bindiv_bonus  # 被推荐人奖金2
                if date_3 is not None:
                    rc_tdate = str(bin_date.shift(months=1 + date_3).date())[:8] + "15"  # 发放日期3
                    date1 = arrow.get(rc_tdate, 'YYYY-MM-DD').date()
                    date2 = arrow.now().date()
                    if (date1 - date2).days < 20:
                        rc_tmoney = indiv_bonus  # 推荐人奖金3
                        rc_btmoney = bindiv_bonus  # 被推荐人奖金3
                if date_4 is not None:
                    rc_4date = str(bin_date.shift(months=1 + date_4).date())[:8] + "15"  # 发放日期4
                    date1 = arrow.get(rc_4date, 'YYYY-MM-DD').date()
                    date2 = arrow.now().date()
                    if (date1 - date2).days < 20:
                        rc_4money = indiv_bonus  # 推荐人奖金4
                        rc_b4money = bindiv_bonus  # 被推荐人奖金4

                Record.objects.filter(id=data.id).update(
                    rc_fdate=rc_fdate,
                    rc_fmoney=rc_fmoney,
                    rc_sdate=rc_sdate,
                    rc_smoney=rc_smoney,
                    rc_tdate=rc_tdate,
                    rc_tmoney=rc_tmoney,
                    rc_4date=rc_4date,
                    rc_4money=rc_4money,
                    rc_bfmoney=rc_bfmoney,
                    rc_bsmoney=rc_bsmoney,
                    rc_btmoney=rc_btmoney,
                    rc_b4money=rc_b4money,
                    rc_issued=rc_fmoney + rc_smoney + rc_tmoney + rc_4money,
                    rc_notissued=bonus - (rc_fmoney + rc_smoney + rc_tmoney + rc_4money),
                    rc_bissued=rc_bfmoney + rc_bsmoney + rc_btmoney + rc_b4money,
                    rc_bnotissued=bonus_b - (rc_bfmoney + rc_bsmoney + rc_btmoney + rc_b4money),
                )

    calc.short_description = '计算金额'
    calc.type = 'primary'


class RewardAdmin(ImportExportModelAdmin):
    list_display = ['re_bdate', 're_edate', 're_money', 're_bmoney', 're_time1', 're_time2', 're_time3', 're_time4',
                    're_desc', 're_level']
    list_filter = ['re_bdate', 're_edate']


class LeaveReasonAdmin(ImportExportModelAdmin):
    list_display = ['reason_name']
    search_fields = ['reason_name']


class InterviewAccountdmin(ImportExportModelAdmin):
    list_display = ['emp_base', 'dates', 'leading_man', 'empid', 'emp', 'emp_dlidl', 'emp_dept', 'emp_post',
                    'emp_source',
                    'emp_in_date', 'prepare_leave_date', 'reason', 'content', 'is_other', 'is_success', 'remarks',
                    'suggests']
    list_filter = ['dates', 'is_success', 'emp__dept', 'emp__p', 'reason', 'emp__dept__dept_base']
    raw_id_fields = ['emp']
    search_fields = ['emp__emp_id', 'emp__emp_name']
    list_per_page = 10
    actions = ['download']

    def emp_base(self, obj):
        return obj.emp.dept.dept_base

    emp_base.short_description = '所属基地'

    def emp_source(self, obj):
        return obj.emp.emp_source

    emp_source.short_description = '劳务来源'

    def empid(self, obj):
        return obj.emp.emp_id

    empid.short_description = '工号'

    def emp_dlidl(self, obj):
        return obj.emp.emp_dlidl

    emp_dlidl.short_description = '员工类型'

    def emp_dept(self, obj):
        return obj.emp.dept

    emp_dept.short_description = '部门'

    def emp_post(self, obj):
        return obj.emp.p

    emp_post.short_description = '岗位'

    def emp_in_date(self, obj):
        return obj.emp.emp_in_date

    emp_in_date.short_description = '入职日期'

    def reason(self, obj):
        return obj.reason.reason_name

    reason.short_description = '离职原因'

    def get_readonly_fields(self, request, obj=None):
        return ('creater', 'createtime')

    def save_model(self, request, obj, form, change):
        InterviewAccount.objects.update_or_create(
            defaults={
                'emp': obj.emp,
                'dates': obj.dates,
                'leading_man': obj.leading_man,
                'prepare_leave_date': obj.prepare_leave_date,
                'reason': obj.reason,
                'content': obj.content,
                'is_other': obj.is_other,
                'is_success': obj.is_success,
                'remarks': obj.remarks,
                'suggests': obj.suggests,
                'creater': str(request.user),
                'createtime': datetime.datetime.now(),
            },
            id=obj.id
        )

    def download(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        row1 = ['基地归属',
                '面谈日期',
                '负责人',
                '工号',
                '员工姓名',
                '员工类型',
                '部门',
                '岗位',
                '劳务来源',
                '入职日期',
                '预离职日期',
                '面谈原因类型',
                '具体内容',
                '是否愿意去其他基地',
                '是否挽留成功',
                '备注',
                '建议'
                ]
        ws.append(row1)
        for datas in queryset:
            row2 = [
                str(datas.emp.dept.dept_base) if str(datas.emp.dept.dept_base) != "None" else "",  # 基地归属
                str(datas.dates) if str(datas.dates) != "None" else "",  # 面谈日期
                str(datas.leading_man) if str(datas.leading_man) != "None" else "",  # 负责人
                str(datas.emp.emp_id) if str(datas.emp.emp_id) != "None" else "",  # 工号
                str(datas.emp.emp_name) if str(datas.emp.emp_name) != "None" else "",  # 员工姓名
                str(datas.emp.emp_dlidl) if str(datas.emp.emp_dlidl) != "None" else "",  # 员工类型
                str(datas.emp.dept.dept_name) if str(datas.emp.dept.dept_name) != "None" else "",  # 部门
                str(datas.emp.p) if str(datas.emp.p) != "None" else "",  # 岗位
                str(datas.emp.emp_source) if str(datas.emp.emp_source) != "None" else "",  # 劳务来源
                str(datas.emp.emp_in_date) if str(datas.emp.emp_in_date) != "None" else "",  # 入职日期
                str(datas.prepare_leave_date) if str(datas.prepare_leave_date) != "None" else "",  # 入职日期
                str(datas.reason.reason_name) if str(datas.reason.reason_name) != "None" else "",  # 面谈原因
                str(datas.content) if str(datas.content) != "None" else "",  # 具体内容
                '是' if str(datas.is_other) == "Y" else "否",  # 是否愿意去其他基地
                '成功' if str(datas.is_success) == "Y" else "失败",  # 是否挽留成功
                str(datas.remarks) if str(datas.remarks) != "None" else "",  # 备注
                str(datas.suggests) if str(datas.suggests) != "None" else "",  # 建议

            ]
            ws.append(row2)
        wb.save('static/standingbook.xlsx')
        #     下载
        file = open('static/standingbook.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="standingbook.xlsx"'
        return response

    download.short_description = '下载数据'
    download.type = 'success'


class testAdmin(ImportExportModelAdmin):
    pass


admin.site.site_header = '人事推荐奖励系统'
admin.site.site_title = '人事推荐奖励系统'
admin.site.index_title = '欢迎使用润阳人事推荐奖励系统'
admin.site.register(Position, PositionAdmin)
admin.site.register(Dept, DeptAdmin)
admin.site.register(Emp, EmpAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(InterviewAccount, InterviewAccountdmin)
admin.site.register(JobLevel, JobLevelAdmin)
admin.site.register(LeaveReason, LeaveReasonAdmin)
