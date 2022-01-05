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
        verbose_name_plural = '部门列表'


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
    emp_in_date = models.DateField(blank=True, null=True, verbose_name="入职日期")
    emp_out_date = models.DateField(blank=True, null=True, verbose_name="离职日期")
    emp_is_work = models.IntegerField(blank=True, null=True, verbose_name='是否在职', choices=is_work_choice)
    emp_rank = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级')

    def __str__(self):
        return str(self.emp_name)

    class Meta:
        managed = False
        db_table = 'emp'
        verbose_name_plural = '员工列表'


# 奖金发放记录表  隔月发放，例如1月入职的，到3月15日发放第一次奖金
class Record(models.Model):
    rc = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="推荐人", related_name='rc')
    rc_b = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="被推荐人", related_name='rc_b')
    rc_cdate = models.DateField(blank=True, null=True, verbose_name="创建日期")
    p = models.ForeignKey('Reward', models.DO_NOTHING, verbose_name="奖金类型")
    rc_fdate = models.DateField(blank=True, null=True, verbose_name="日期1")
    rc_fmoney = models.FloatField(blank=True, null=True, verbose_name="金额1")
    rc_sdate = models.DateField(blank=True, null=True, verbose_name="日期2")
    rc_smoney = models.FloatField(blank=True, null=True, verbose_name="金额2")
    rc_tdate = models.DateField(blank=True, null=True, verbose_name="日期3")
    rc_tmoney = models.FloatField(blank=True, null=True, verbose_name="金额3")
    rc_4date = models.DateField(blank=True, null=True, verbose_name="日期4")
    rc_4money = models.FloatField(blank=True, null=True, verbose_name="金额4")
    rc_bfmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额1")
    rc_bsmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额2")
    rc_btmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额3")
    rc_b4money = models.FloatField(blank=True, null=True, verbose_name="被推荐人金额4")
    creater = models.CharField(max_length=255, blank=True, null=True, verbose_name='创建人')
    rc_issued = models.FloatField(blank=True, null=True, verbose_name="已发放金额合计")
    rc_notissued = models.FloatField(blank=True, null=True, verbose_name="未发放金额合计")

    class Meta:
        managed = False
        db_table = 'record'
        verbose_name_plural = '奖金发放记录表'


# 奖金类型表
class Reward(models.Model):
    re_bdate = models.DateField(blank=True, null=True, verbose_name="生效日期")
    re_edate = models.DateField(blank=True, null=True, verbose_name="失效日期")
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
