# Generated by Django 2.1.1 on 2018-10-11 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rendhtml', '0005_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordergoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='商品名字')),
                ('good_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('good_number', models.IntegerField(default=0, verbose_name='商品数量')),
                ('good_thumb', models.ImageField(upload_to='goods/', verbose_name='商品缩略图')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rendhtml.Goods', verbose_name='商品')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
            },
        ),
        migrations.CreateModel(
            name='Orderinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('finish_status', models.BooleanField(default=False, verbose_name='是否完成')),
                ('pay_status', models.BooleanField(default=False, verbose_name='是否支付')),
                ('good_flow_status', models.BooleanField(default=False, verbose_name='是否送到')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '所有订单',
                'verbose_name_plural': '所有订单',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rendhtml.Orderinfo', verbose_name='订单'),
        ),
    ]
