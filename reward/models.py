from django.db import models


# Create your models here.
# 岗位表
class Position(models.Model):
    p_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位id')
    p_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位名称')

    # re = models.ForeignKey('Reward', models.DO_NOTHING, verbose_name="奖金信息")

    def __str__(self):
        return str(self.p_name)

    class Meta:
        managed = False
        db_table = 'position'
        verbose_name = '岗位列表'
        verbose_name_plural = '岗位列表'


# 部门表
class Dept(models.Model):
    dept_id = models.CharField(blank=True, null=True, max_length=255, verbose_name='部门id')
    dept_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门名称')
    dept_base = models.CharField(max_length=255, blank=True, null=True, verbose_name='基地名称')

    def __str__(self):
        return str(self.dept_name)

    class Meta:
        managed = False
        db_table = 'dept'
        verbose_name = '部门列表'
        verbose_name_plural = '部门列表'


class JobLevel(models.Model):
    level_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级编码')
    level_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级名称')

    def __str__(self):
        return str(self.level_name)

    class Meta:
        managed = False
        db_table = 'job_level'
        verbose_name_plural = '职级表'
        verbose_name = '职级表'


is_work_choice = (
    (1, '在职'),
    (2, '离职'),
)


# 员工表
class Emp(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=255, verbose_name='员工工号')
    emp_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工姓名')
    dept = models.ForeignKey('Dept', models.DO_NOTHING, verbose_name="部门")
    p = models.ForeignKey('Position', models.DO_NOTHING, verbose_name="岗位")
    emp_source = models.CharField(max_length=255, blank=True, null=True, verbose_name='招聘来源')
    emp_in_date = models.DateField(blank=True, null=True, verbose_name="入职日期")
    emp_out_date = models.DateField(blank=True, null=True, verbose_name="离职日期")
    emp_is_work = models.IntegerField(blank=True, null=True, verbose_name='是否在职', choices=is_work_choice)
    # emp_rank = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级')
    emp_dlidl = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工类型')
    level = models.ForeignKey('JobLevel', models.DO_NOTHING, verbose_name="职级")

    def __str__(self):
        return str(self.emp_name)

    class Meta:
        managed = False
        db_table = 'emp'
        verbose_name_plural = '员工列表'
        verbose_name = '员工列表'


# 奖金发放记录表  隔月发放，例如1月入职的，到3月15日发放第一次奖金
class Record(models.Model):
    rc = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="推荐人", related_name='rc')
    rc_b = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="被推荐人", related_name='rc_b')
    rc_cdate = models.DateField(blank=True, null=True, verbose_name="创建日期")
    p = models.ForeignKey('Reward', models.DO_NOTHING, verbose_name="奖金类型")
    rc_fdate = models.DateField(blank=True, null=True, verbose_name="发放日期1")
    rc_fmoney = models.FloatField(blank=True, null=True, verbose_name="推荐人金额1")
    rc_bfmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额1")
    rc_sdate = models.DateField(blank=True, null=True, verbose_name="发放日期2")
    rc_smoney = models.FloatField(blank=True, null=True, verbose_name="推荐人金额2")
    rc_bsmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额2")
    rc_tdate = models.DateField(blank=True, null=True, verbose_name="发放日期3")
    rc_tmoney = models.FloatField(blank=True, null=True, verbose_name="推荐人金额3")
    rc_btmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额3")
    rc_4date = models.DateField(blank=True, null=True, verbose_name="发放日期4")
    rc_4money = models.FloatField(blank=True, null=True, verbose_name="推荐人金额4")
    rc_b4money = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额4")
    creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    rc_issued = models.FloatField(blank=True, null=True, verbose_name="推荐人已发放金额合计")
    rc_notissued = models.FloatField(blank=True, null=True, verbose_name="推荐人未发放金额合计")
    rc_bissued = models.FloatField(blank=True, null=True, verbose_name="被推荐人已发放金额合计")
    rc_bnotissued = models.FloatField(blank=True, null=True, verbose_name="被推荐人未发放金额合计")

    class Meta:
        managed = False
        db_table = 'record'
        verbose_name_plural = '奖金发放记录表'
        verbose_name = '奖金发放记录表'


# 奖金类型表
class Reward(models.Model):
    re_bdate = models.DateField(blank=True, null=True, verbose_name="生效日期")
    re_edate = models.DateField(blank=True, null=True, verbose_name="失效日期")
    re_level = models.ForeignKey('JobLevel', models.DO_NOTHING, verbose_name="职级")
    re_money = models.FloatField(blank=True, null=True, verbose_name="推荐人奖金金额")
    re_bmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人奖金金额")
    re_time1 = models.IntegerField(blank=True, null=True, verbose_name='第一次发放月（入职后）')
    re_time2 = models.IntegerField(blank=True, null=True, verbose_name='第二次发放月（入职后）')
    re_time3 = models.IntegerField(blank=True, null=True, verbose_name='第三次发放月（入职后）')
    re_time4 = models.IntegerField(blank=True, null=True, verbose_name='第四次发放月（入职后）')
    re_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='规则描述')

    def __str__(self):
        if self.re_bmoney is None:
            bmoney = "0"
        else:
            bmoney = self.re_bmoney
        return str(self.re_bdate) + "到" + str(self.re_edate) + ",推荐人奖金为" + str(
            self.re_money) + ",被推荐人奖金为" + str(bmoney)

    class Meta:
        managed = False
        db_table = 'reward'
        verbose_name_plural = '奖金标准'
        verbose_name = '奖金标准'


# 离职理由
class LeaveReason(models.Model):
    reason_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='离职理由')

    def __str__(self):
        return self.reason_name

    class Meta:
        managed = False
        db_table = 'leave_reason'
        verbose_name_plural = '离职理由表'
        verbose_name = '离职理由表'


success_choice = (
    ('Y', '成功'),
    ('N', '失败'),
)
other_choice = (
    ('Y', '是'),
    ('N', '否'),
)

reason_choice = (
    ('公司原因-薪资福利不满意', '公司原因-薪资福利不满意'),
    ('公司原因-缺少晋升机会/空间', '公司原因-缺少晋升机会/空间'),
    ('公司原因-工作时间长/工作量大', '公司原因-工作时间长/工作量大'),
    ('公司原因-与同事关系不融洽', '公司原因-与同事关系不融洽'),
    ('公司原因-不适应领导管理方式', '公司原因-不适应领导管理方式'),
    ('公司原因-不满意公司的政策制度', '公司原因-不满意公司的政策制度'),
    ('公司原因-工作环境不适应', '公司原因-工作环境不适应'),
    ('个人原因-找到新工作', '个人原因-找到新工作'),
    ('个人原因-自主创业', '个人原因-自主创业'),
    ('个人原因-继续深造学习', '个人原因-继续深造学习'),
    ('个人原因-家庭原因', '个人原因-家庭原因'),
    ('个人原因-身体原因', '个人原因-身体原因'),
    ('个人原因-其他', '个人原因-其他'),
    ('个人原因-不能胜任工作', '个人原因-不能胜任工作'),
    ('中介原因-工期满了', '中介原因-工期满了'),
    ('中介原因-中介扣发费用', '中介原因-中介扣发费用'),
    ('其他原因-劝退', '其他原因-劝退'),
    ('其他原因-实习期满', '其他原因-实习期满'),

)


# 离职台账表
class InterviewAccount(models.Model):
    emp = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="员工", related_name='emp')
    dates = models.DateField(blank=True, null=True, verbose_name="面谈日期")
    leading_man = models.CharField(max_length=255, blank=True, null=True, verbose_name='负责人')
    prepare_leave_date = models.DateField(blank=True, null=True, verbose_name="预离职日期")
    reason = models.ForeignKey('LeaveReason', models.DO_NOTHING, verbose_name="离职原因")
    content = models.CharField(max_length=255, blank=True, null=True, verbose_name='具体内容')
    is_success = models.CharField(max_length=255, blank=True, null=True, verbose_name='是否挽留成功', choices=success_choice)
    is_other = models.CharField(max_length=255, blank=True, null=True, verbose_name='是否愿意去其他基地', choices=other_choice)
    remarks = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    suggests = models.CharField(max_length=255, blank=True, null=True, verbose_name='建议')
    creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='修改人')
    createtime = models.DateTimeField(blank=True, null=True, verbose_name="修改时间")

    class Meta:
        managed = False
        db_table = 'interview_account'
        verbose_name_plural = '员工离职面谈台账'
        verbose_name = '员工离职面谈台账'
