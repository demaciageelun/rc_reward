# Generated by Django 2.2 on 2022-01-19 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reward', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.CharField(blank=True, max_length=255, null=True, verbose_name='面谈年月')),
                ('reason', models.CharField(blank=True, max_length=255, null=True, verbose_name='面谈原因')),
                ('content', models.CharField(blank=True, max_length=255, null=True, verbose_name='具体内容')),
                ('is_success', models.CharField(blank=True, choices=[('Y', '成功'), ('N', '失败')], max_length=255, null=True, verbose_name='是否挽留成功')),
                ('remarks', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '员工离职面谈台账',
                'db_table': 'interview_account',
                'managed': False,
            },
        ),
    ]
