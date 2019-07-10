# Generated by Django 2.2.3 on 2019-07-09 15:13

from django.db import migrations, models
import libs.orm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('bj', '北京'), ('sz', '深圳'), ('sh', '上海'), ('gz', '广州'), ('cd', '成都'), ('dl', '大连')], max_length=64)),
                ('min_distance', models.IntegerField(default=1)),
                ('max_distance', models.IntegerField(default=10)),
                ('min_dating_age', models.IntegerField(default=18)),
                ('max_dating_age', models.IntegerField(default=81)),
                ('dating_sex', models.IntegerField(choices=[(0, '全部'), (1, '男'), (2, '女')], default=0)),
                ('vibration', models.BooleanField(default=True)),
                ('only_matche', models.BooleanField(default=True)),
                ('auto_play', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'profiles',
            },
            bases=(models.Model, libs.orm.ModelToDictMixin),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=11, unique=True)),
                ('nickname', models.CharField(max_length=32)),
                ('sex', models.IntegerField(choices=[(0, '全部'), (1, '男'), (2, '女')], default=0)),
                ('birth_year', models.IntegerField(default=2000)),
                ('birth_month', models.IntegerField(default=1)),
                ('birth_day', models.IntegerField(default=1)),
                ('avatar', models.CharField(max_length=256)),
                ('location', models.CharField(choices=[('bj', '北京'), ('sz', '深圳'), ('sh', '上海'), ('gz', '广州'), ('cd', '成都'), ('dl', '大连')], max_length=64)),
                ('vip_id', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
