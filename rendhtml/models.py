from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    username=models.CharField('用户名',max_length=20,unique=True)
    password=models.CharField('密码',max_length=30)
    email=models.EmailField()


class Userext(models.Model):
    parent=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='父分类',null=True)
    tel=models.CharField('手机号',max_length=11,unique=True)
    nick=models.CharField('昵称',max_length=10,unique=True)


class Category(models.Model):
    class Meta:
        verbose_name='商品分类'
        verbose_name_plural=verbose_name
    parent=models.ForeignKey('self',on_delete=models.CASCADE,verbose_name='父分类',null=True,blank=True)
    name=models.CharField('名称',max_length=15,unique=True)
    icon=models.CharField('图标',max_length=100,null=True,blank=True)
    banner=models.ImageField('图片',upload_to='category/',null=True,blank=True)
    desc=models.CharField('简介',max_length=200,null=True,blank=True)
    order=models.IntegerField('排序',default=0)
    show_in_menu=models.BooleanField('菜单显示',default=True)
    show_in_home=models.BooleanField('首页显现',default=True)
    create_data=models.DateField('创建日期',auto_now_add=True)

    def __str__(self):
        return self.name

class Goods(models.Model):
    class Meta:
        verbose_name='商品信息'
        verbose_name_plural=verbose_name
#     关联分类外键
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='商品分类')
    name=models.CharField('标题',max_length=30)
    keyword=models.CharField('关键字',max_length=300,null=True,blank=True)
    brief=models.CharField('简短描述',max_length=100,null=True,blank=True)
    stock=models.IntegerField('库存',default=0)
    market_price=models.DecimalField('市场售价',max_digits=10,decimal_places=2)
    shop_price=models.DecimalField('本店售价',max_digits=10,decimal_places=2)
    thumb=models.ImageField('缩略图',upload_to='goods/')
    is_recommend=models.BooleanField('是否推荐',default=False)
    order=models.IntegerField('排序',default=0)
    create_data=models.DateTimeField('创建日期',auto_now_add=True)

    def __str__(self):
        return self.name


# 购物车模型
class Cart(models.Model):
    class Meta:
        verbose_name='购物车'
        verbose_name_plural=verbose_name
    #     关联User的外键
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    #     关联Good的外键
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品')
    number=models.IntegerField('数量',default=0)
    created_date=models.DateTimeField('添加时间',auto_now_add=True)

# 全部订单模型
class Orderinfo(models.Model):
    class Meta:
        verbose_name='所有订单'
        verbose_name_plural=verbose_name
    created_date=models.DateTimeField('添加时间',auto_now_add=True)
    #     关联User的外键
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    finish_status=models.BooleanField('是否完成',default=False)
    pay_status=models.SmallIntegerField('是否支付', choices=[(0, '未支付'), (1, '已支付')], default=0)
    good_flow_status=models.BooleanField('是否送到',default=False)


# 订单商品模型
class Ordergoods(models.Model):
    class Meta:
        verbose_name='订单商品'
        verbose_name_plural=verbose_name
    #     关联Orderinfo的外键
    order=models.ForeignKey(Orderinfo,on_delete=models.CASCADE,verbose_name='订单')
    #     关联Goods的外键
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品')
    name=models.CharField('商品名字',max_length=30)
    good_price=models.DecimalField('商品价格',max_digits=10,decimal_places=2)
    good_number=models.IntegerField('商品数量',default=0)
    good_thumb=models.ImageField('商品缩略图',upload_to='goods/')
    created_date=models.DateTimeField('添加时间',auto_now_add=True)


