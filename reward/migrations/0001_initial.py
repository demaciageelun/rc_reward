# Generated by Django 2.2 on 2022-01-11 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='部门id')),
                ('dept_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='部门名称')),
                ('dept_base', models.CharField(blank=True, max_length=255, null=True, verbose_name='基地名称')),
            ],
            options={
                'verbose_name_plural': '部门列表',
                'db_table': 'dept',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Emp',
            fields=[
                ('emp_id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='员工工号')),
                ('emp_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='员工姓名')),
                ('emp_in_date', models.DateField(blank=True, null=True, verbose_name='入职日期')),
                ('emp_out_date', models.DateField(blank=True, null=True, verbose_name='离职日期')),
                ('emp_is_work', models.IntegerField(blank=True, choices=[(1, '在职'), (2, '离职')], null=True, verbose_name='是否在职')),
                ('emp_rank', models.CharField(blank=True, max_length=255, null=True, verbose_name='职级')),
            ],
            options={
                'verbose_name_plural': '员工列表',
                'db_table': 'emp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='岗位id')),
                ('p_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='岗位名称')),
            ],
            options={
                'verbose_name_plural': '岗位列表',
                'db_table': 'position',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rc_cdate', models.DateField(blank=True, null=True, verbose_name='创建日期')),
                ('rc_fdate', models.DateField(blank=True, null=True, verbose_name='发放日期1')),
                ('rc_fmoney', models.FloatField(blank=True, null=True, verbose_name='推荐人金额1')),
                ('rc_bfmoney', models.FloatField(blank=True, null=True, verbose_name='被推荐人金额1')),
                ('rc_sdate', models.DateField(blank=True, null=True, verbose_name='发放日期2')),
                ('rc_smoney', models.FloatField(blank=True, null=True, verbose_name='推荐人金额2')),
                ('rc_bsmoney', models.FloatField(blank=True, null=True, verbose_name='被推荐人金额2')),
                ('rc_tdate', models.DateField(blank=True, null=True, verbose_name='发放日期3')),
                ('rc_tmoney', models.FloatField(blank=True, null=True, verbose_name='推荐人金额3')),
                ('rc_btmoney', models.FloatField(blank=True, null=True, verbose_name='被推荐人金额3')),
                ('rc_4date', models.DateField(blank=True, null=True, verbose_name='发放日期4')),
                ('rc_4money', models.FloatField(blank=True, null=True, verbose_name='推荐人金额4')),
                ('rc_b4money', models.FloatField(blank=True, null=True, verbose_name='被推荐人金额4')),
                ('creater', models.CharField(blank=True, max_length=255, null=True, verbose_name='创建人')),
                ('rc_issued', models.FloatField(blank=True, null=True, verbose_name='推荐人已发放金额合计')),
                ('rc_notissued', models.FloatField(blank=True, null=True, verbose_name='推荐人未发放金额合计')),
                ('rc_bissued', models.FloatField(blank=True, null=True, verbose_name='被推荐人已发放金额合计')),
                ('rc_bnotissued', models.FloatField(blank=True, null=True, verbose_name='被推荐人未发放金额合计')),
            ],
            options={
                'verbose_name_plural': '奖金发放记录表',
                'db_table': 'record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('re_bdate', models.DateField(blank=True, null=True, verbose_name='生效日期')),
                ('re_edate', models.DateField(blank=True, null=True, verbose_name='失效日期')),
                ('re_money', models.FloatField(blank=True, null=True, verbose_name='推荐人奖金金额')),
                ('re_bmoney', models.FloatField(blank=True, null=True, verbose_name='被推荐人奖金金额')),
                ('re_time1', models.IntegerField(blank=True, null=True, verbose_name='第一次发放月（入职后）')),
                ('re_time2', models.IntegerField(blank=True, null=True, verbose_name='第二次发放月（入职后）')),
                ('re_time3', models.IntegerField(blank=True, null=True, verbose_name='第三次发放月（入职后）')),
                ('re_time4', models.IntegerField(blank=True, null=True, verbose_name='第四次发放月（入职后）')),
                ('re_desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='规则描述')),
            ],
            options={
                'verbose_name_plural': '奖金标准',
                'db_table': 'reward',
                'managed': False,
            },
        ),
    ]