from django.db import models


# Create your models here.
# 岗位表
class Position(models.Model):
    p_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位名称')

    # re = models.ForeignKey('Reward', models.DO_NOTHING, verbose_name="奖金信息")

    def __str__(self):
        return str(self.p_name)

    class Meta:
        managed = False
        db_table = 'position'
        verbose_name = '岗位列表'


# 部门表
class Dept(models.Model):
    dept_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='部门名称')

    def __str__(self):
        return str(self.dept_name)

    class Meta:
        managed = False
        db_table = 'dept'
        verbose_name = '部门列表'


is_work_choice = (
    (1, '在职'),
    (2, '离职'),
)
base_choice = (
    (1, '润阳新能源'),
    (2, '润阳悦达'),
    (3, '建湖润阳'),
    (4, '润阳世纪'),
    (5, '泰国润阳'),
)


# 员工表
class Emp(models.Model):
    emp_id = models.IntegerField(primary_key=True, verbose_name='员工工号')
    emp_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工姓名')
    dept = models.ForeignKey('Dept', models.DO_NOTHING, verbose_name="部门")
    p = models.ForeignKey('Position', models.DO_NOTHING, verbose_name="岗位")
    emp_in_date = models.DateField(blank=True, null=True, verbose_name="入职日期")
    emp_out_date = models.DateField(blank=True, null=True, verbose_name="离职日期")
    emp_is_work = models.IntegerField(blank=True, null=True, verbose_name='是否在职', choices=is_work_choice)
    emp_rank = models.CharField(max_length=255, blank=True, null=True, verbose_name='职级')
    emp_base = models.IntegerField(blank=True, null=True, verbose_name='基地', choices=base_choice)

    def __str__(self):
        return str(self.emp_name)

    class Meta:
        managed = False
        db_table = 'emp'
        verbose_name = '员工列表'


# 奖金发放记录表
class Record(models.Model):
    rc = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="推荐人", related_name='rc')
    rc_b = models.ForeignKey('Emp', models.DO_NOTHING, verbose_name="被推荐人", related_name='rc_b')
    p = models.ForeignKey('Reward', models.DO_NOTHING, verbose_name="奖金类型")
    rc_fdate = models.DateField(blank=True, null=True, verbose_name="发放日期1")
    rc_fmoney = models.FloatField(blank=True, null=True, verbose_name="发放金额1")
    rc_sdate = models.DateField(blank=True, null=True, verbose_name="发放日期2")
    rc_smoney = models.FloatField(blank=True, null=True, verbose_name="发放金额2")
    rc_tdate = models.DateField(blank=True, null=True, verbose_name="发放日期3")
    rc_tmoney = models.FloatField(blank=True, null=True, verbose_name="发放金额3")
    rc_4date = models.DateField(blank=True, null=True, verbose_name="发放日期4")
    rc_4money = models.FloatField(blank=True, null=True, verbose_name="发放金额4")

    def pp(self):
        if len(str(self.p)) > 10:
            return '{}···'.format(str(self.p)[0:10])
        else:
            return str(self.p)

    pp.allow_tags = True
    pp.short_description = "奖金类型"

    class Meta:
        managed = False
        db_table = 'record'
        verbose_name = '奖金发放记录表'


# 奖金类型表
class Reward(models.Model):
    re_bdate = models.DateField(blank=True, null=True, verbose_name="生效日期")
    re_edate = models.DateField(blank=True, null=True, verbose_name="失效日期")
    p = models.ForeignKey('Position', models.DO_NOTHING, verbose_name="岗位信息")
    re_money = models.FloatField(blank=True, null=True, verbose_name="推荐人奖金金额")
    re_bmoney = models.FloatField(blank=True, null=True, verbose_name="被推荐人奖金金额")
    re_times = models.IntegerField(blank=True, null=True, verbose_name='分期发放次数')
    re_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='规则描述')

    def __str__(self):
        if self.re_bmoney is None:
            bmoney = "0"
        else:
            bmoney = self.re_bmoney
        return str(self.p.p_name) + "," + str(self.re_bdate) + "到" + str(self.re_edate) + ",分" + str(
            self.re_times) + "期发，推荐人奖金为" + str(
            self.re_money) + ",被推荐人奖金为" + str(bmoney)

    class Meta:
        managed = False
        db_table = 'reward'
        verbose_name = '奖金标准'
