# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=512)),
                ('benefit_type', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('value', models.CharField(default=0, max_length=512)),
                ('related_id', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('icon', models.CharField(max_length=512)),
                ('start_date', models.CharField(default=b'', max_length=128)),
                ('end_date', models.CharField(default=b'', max_length=128)),
                ('merchant_id', models.IntegerField(default=0)),
                ('store_id', models.IntegerField(default=0)),
                ('good_id', models.IntegerField(default=0)),
                ('product_id', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'benefit',
            },
        ),
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('custom_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=512)),
                ('phone', models.CharField(max_length=512)),
                ('wechat', models.CharField(max_length=512)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'custom',
            },
        ),
        migrations.CreateModel(
            name='CustomBenifit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('custom_id', models.IntegerField(default=0)),
                ('good_id', models.IntegerField(default=0)),
                ('product_id', models.IntegerField(default=0)),
                ('benefit_id', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'custom_benefit',
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('item_code', models.CharField(max_length=512)),
                ('product_id', models.IntegerField(default=0)),
                ('merchant_id', models.IntegerField(default=0)),
                ('store_id', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('class_name', models.CharField(max_length=512)),
                ('unit', models.CharField(max_length=512)),
                ('area', models.CharField(max_length=512)),
                ('shelf_day', models.DateTimeField()),
                ('in_price', models.DecimalField(max_digits=19, decimal_places=2)),
                ('sale_price', models.DecimalField(max_digits=19, decimal_places=2)),
                ('whole_sale_price', models.DecimalField(max_digits=19, decimal_places=2)),
                ('vip_price', models.DecimalField(max_digits=19, decimal_places=2)),
                ('remark', models.CharField(max_length=2048)),
                ('extra', models.CharField(max_length=2048)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'good',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('status', models.IntegerField(default=0)),
                ('shop_num', models.IntegerField(default=0)),
                ('contact', models.CharField(max_length=512)),
                ('telephone', models.CharField(max_length=512)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'merchant',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('custom_id', models.IntegerField(default=0)),
                ('trade_no', models.CharField(max_length=512)),
                ('trade_id', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='PayDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('trade_no', models.CharField(max_length=512)),
                ('store_id', models.IntegerField(default=0)),
                ('way', models.IntegerField(default=0)),
                ('pay_time', models.DateTimeField(auto_now_add=True)),
                ('trade_status', models.IntegerField(default=0)),
                ('fee', models.DecimalField(max_digits=19, decimal_places=2)),
                ('refund_status', models.IntegerField(default=0)),
                ('extra', models.CharField(max_length=2048)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pay_detail',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('class_name', models.CharField(max_length=512)),
                ('unit', models.CharField(max_length=512)),
                ('extra', models.CharField(max_length=2048)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('merchant_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=512)),
                ('status', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=2048)),
                ('latitude', models.DecimalField(default=0, max_digits=10, decimal_places=6)),
                ('longitude', models.DecimalField(default=0, max_digits=10, decimal_places=6)),
                ('score', models.DecimalField(max_digits=2, decimal_places=1)),
                ('icon', models.CharField(default=b'', max_length=2048)),
                ('contact', models.CharField(default=b'', max_length=512)),
                ('telephone', models.CharField(default=b'', max_length=512)),
                ('description', models.CharField(default=b'', max_length=2048)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'store',
            },
        ),
        migrations.CreateModel(
            name='TradeInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('trade_id', models.IntegerField(default=0)),
                ('custom_id', models.IntegerField(default=0)),
                ('product_id', models.IntegerField(default=0)),
                ('good_id', models.IntegerField(default=0)),
                ('benefit_id', models.IntegerField(default=0)),
                ('store_id', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'trade_info',
            },
        ),
    ]
