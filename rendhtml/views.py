from django.shortcuts import render,redirect
from .forms import RegisTer
from .models import Register
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
#注册验证UserCreationForm     登录验证AuthenticationForm
from django.contrib.auth.forms import authenticate,AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Category,Goods,Cart,Ordergoods,Orderinfo
from django.core.paginator import Paginator
from django.db.models import F,Q,Sum


# Create your views here.
def base(request):
    user=request.user
    usercartnumber=Cart.objects.filter(user_id=user.id).aggregate(Sum('number'))
    # cart_number=cart.aggregate(Sum('number'))
    print(usercartnumber)
    context={
        'usercartnumber':usercartnumber
    }
    # return render(request,'D:\Gjango\Fresheveryday\templates\base.html')
    return render(request, 'base.html',context)

def base1(request):
    return render(request,'base1.html')


def index(request):
    category = Category.objects.all()
    user = request.user
    usercartnumber = Cart.objects.filter(user_id=user.id).aggregate(Sum('number'))
    context={
        'category':category,
        'usercartnumber':usercartnumber
        # 'goods':goods
    }
    return render(request,'index.html',context)




@login_required(login_url='login')
def cart(request):
    user=request.user
    car=Cart.objects.filter(user_id=user.id)
    user = request.user
    usercartnumber = Cart.objects.filter(user_id=user.id).aggregate(Sum('number'))
    context={
        'car':car,
        'usercartnumber': usercartnumber
    }
    return render(request,'cart.html',context)


def del_cart(request,foo_id):
    try:
        res = Cart.objects.get(pk=foo_id).delete()
        if res[0]:
            return redirect('cart')
        else:
            return HttpResponse('删除失败')
    except Exception:
        return HttpResponse('删除失败')
# @login_required(login_url='login')
def add_cart(request):
    goods_id=request.POST.get('goods_id')
    number = request.POST.get('number')
    user = request.user
    print(number,goods_id)
    cart=Cart.objects.filter(goods_id=goods_id,user_id=user.id).first()
    # 过滤条件：同一个用户and同一个商品
    if cart is not None:
        cart.number+=int(number)
        cart.save()
        return JsonResponse({'ok':1,'message':'添加成功'})
    else:
        try:
            cart=Cart.objects.create(
                goods_id=goods_id,
                number=number,
                user_id=user.id,
            )
            if cart is not None:
                return JsonResponse({'ok': 1, 'message': '添加成功'})
            return JsonResponse({'ok': 0, 'message': '请先登录'})
        except Exception:
            return JsonResponse({'ok': 0, 'message': '请先登录'})

def add_lcart(request):
    goods_id=request.GET.get('goods_id')
    # good_id=request.POST.get('goods_id')
    number = request.GET.get('number')
    user = request.user
    # print(number,goods_id)
    cart=Cart.objects.filter(goods_id=goods_id,user_id=user.id).first()
    if cart is not None:
        cart.number+=int(number)
        cart.save()
        return JsonResponse({'ok':1,'message':'添加成功'})
    else:
        try:
            cart=Cart.objects.create(
                goods_id=goods_id,
                number=number,
                user_id=user.id,
            )
            if cart is not None:
                return JsonResponse({'ok': 1, 'message': '添加成功'})
            return JsonResponse({'ok': 0, 'message': '请先登录'})
        except Exception:
            return JsonResponse({'ok': 0, 'message': '请先登录'})



def detail(request):
    user=request.user
    usercartnumber=Cart.objects.filter(user_id=user.id).aggregate(Sum('number'))
    category = Category.objects.all()
    goods_id=request.GET.get('goods_id')
    print(goods_id)
    request.session['goods_id']=goods_id
    request.session.set_expiry(600*10)
    cate_id = request.GET.get('cate_id', None)
    goods=Goods.objects.get(id=goods_id)
    recommend=Goods.objects.filter(category_id=cate_id,is_recommend=1)
    print(cate_id)
    # goo=request.COOKIES.get('goods_id','')
    # goo_list=goo.split(',')
    context = {
        'category': category,
        'goods':goods,
        'cate_id':cate_id,
        'recommend':recommend,
        'usercartnumber':usercartnumber
    }
    response = render(request, 'detail.html', context)
    # goods = request.COOKIES.get('goods', '')  # 判断是否有常浏览商品这个COOKIE
    # if goods != '':
    #     goods_list = goods.split(',')
    #     if goods_list.count(number) < 1 and len(goods_list) < 6:  # 判断该商品是否唯一
    #         goods = goods + ',' + str(number)
    #         response.set_cookie('goods', goods, max_age=3600)
    # else:
    #     pro = str(number)
    #     response.set_cookie('goods', pro)
    return response


def list(request):
    user = request.user
    usercartnumber = Cart.objects.filter(user_id=user.id).aggregate(Sum('number'))
    category = Category.objects.all()
    cate_id = request.GET.get('cate_id', '')
    keyword=request.GET.get('keyword','')
    if cate_id:
        cate = Category.objects.get(id=cate_id)
        goods=Goods.objects.filter(category_id=cate_id)
        recommend=Goods.objects.filter(category_id=cate_id,is_recommend=1)
    elif keyword:
        goods=Goods.objects.filter(name__contains=keyword)
        recommend=Goods.objects.filter(name__contains=keyword,is_recommend=1)
        cate = ''
    else:
        goods=Goods.objects.all()
        # goods=Goods.objects.get_queryset().order_by('id')
        recommend=Goods.objects.filter(is_recommend=1)
        cate = ''
    paginator = Paginator(goods,10)
    num = int(request.GET.get('page',1))
    page = paginator.page(num)
    context={
        'goods':goods,
        'category':category,
        'page':page,
        'cate_id':cate_id,
        'keyword':keyword,
        'cate':cate,
        'recommend':recommend,
        'usercartnumber':usercartnumber
    }
    return render(request,'list.html',context)



def ulogin(request):
    if request.method=='POST':
        next_url = request.POST.get('next','')
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            # return redirect(request.POST.get('next'))
            res = {
                'ok': 1,
                # 'error': form.errors
            }
            return JsonResponse(res)
        else:
            res={
                'ok':0,
                'error':form.errors
            }
            return JsonResponse(res)
    else:
        form=AuthenticationForm()
        next_url = request.GET.get('next', '')
    context={
        'form':form,
        'next':next_url
    }
    return render(request, 'login.html',context)

def ulogout(request):
    logout(request)
    return redirect('index')
def place_order(request):
    # ids=10,20,5
    car = request.GET.get('ids')
    value=request.GET.get('value')
    value=value.split(',')
    # print(value)
    # car:'10,20,5'
    # '10,20,5'.split(',')这样计算后返回列表
    # [10,20,5]
    # 筛选Cart中的id在此上列表中的可以匹配到的
    cart = Cart.objects.filter(id__in=car.split(','))
    n=0
    for i in cart:
        i.number=value[n]
        i.save()
        n=n+1
    print(cart)
    context={
        'cart':cart,
    }
    return render(request,'place_order.html',context)
def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'ok':1})
        else:
            res = {
                'ok':0,
                'error': form.errors
            }
            return JsonResponse(res)

    else:
        form=UserCreationForm()
    context={
        'form':form
    }
    return render(request,'register.html',context)


@login_required(login_url='login')
def user_center_info(request):
    goods_id=request.session.get('goods_id')
    goods=Goods.objects.filter(id=goods_id)
    context={
        'goods':goods
    }
    return render(request,'user_center_info.html',context)
    # context = {}
    # good = []
    # uname = request.COOKIES.get('uname')
    # goods = request.COOKIES.get('goods', '')  # 获取goods这个COOKIE
    # if goods != '':  # 判断该COOKIE是否为空
    #     good_list = goods.split(',')
    #     for i in good_list:
    #         good.append(Goods.objects.get(number=int(i)))  # 取出每个number对应的商品
    # context['goods'] = goods
    # context['uname'] = uname
    # user = User.objects.get(username=uname)
    # if user.relate_address:
    #     context['address'] = Address.objects.filter(belong_to=user, tag=True)
    # return render(request, 'user_center_info.html', context)


@login_required(login_url='login')
def user_center_order(request):
    import json
    user=request.user
    car = request.GET.get('ids')
    if car is not  None:
        print(car)
        cart = Cart.objects.filter(id__in=car.split(','))
        print(cart)
        orders=Orderinfo.objects.create(
            user_id=user.id
        )
        orderss=Orderinfo.objects.filter(user_id=user.id)
        for i in cart:
            order_goods=Ordergoods.objects.create(
                order_id=orders.id,
                goods_id=i.goods.id,
                name=i.goods.name,
                good_price=i.goods.shop_price,
                good_number=i.number,
                good_thumb=i.goods.thumb
            )
        delete_cart=Cart.objects.filter(id__in=car.split(',')).delete()
        # car=json.loads(car)#这里这里这里
        print(cart)
    else:
        orderss = Orderinfo.objects.filter(user_id=user.id)
    context = {
        # 'cart': cart,#这里这里
        'orderss':orderss,
        # 'order_goodss':order_goodss
    }
    # print(cart)
    return render(request,'user_center_order.html',context)

def del_order(request):
    order_id=request.GET.get('order_id')
    print(order_id)
    print(Ordergoods.objects.filter(order_id=order_id))
    order_goods=Ordergoods.objects.filter(order_id=order_id).delete()
    print(Orderinfo.objects.get(id=order_id))
    order_info=Orderinfo.objects.get(id=order_id).delete()
    return redirect('user_center_order')



def user_center_site(request):
    return render(request,'user_center_site.html')

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
def repassword(request):
    return render(request,'repassword.html')
def get_code(request):
    import random
    # appid=1400147763
    # appkey='bbe0084c2a88e2f50a2364e83effbc5f'
    tel = request.POST.get('tel')
    code = random.randint(1000, 9999)
    request.session['code'] = code#保存到字典 保存到后台session
    request.session.set_expiry(600)
    # 验证码有效时间10分钟
    print(tel)
    ssender = SmsSingleSender(1400147763, 'bbe0084c2a88e2f50a2364e83effbc5f')
    phone_numbers = [tel]
    # template_id = 205042
    # sms_sign = "阿里优"
    params = [code, '10']  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
    try:
        result = ssender.send_with_param(
            86,
            phone_numbers[0],
            205042,
            params,
            sign="阿里优",
            extend="",
            ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
        print(result)
        if result['result']==0:
            return JsonResponse({'ok':1})
        else:
            return JsonResponse({'ok':0})
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    print(result)
    # return JsonResponse({'ok':0})
def checksms(request):
    if request.method == 'POST':
        smscode = request.POST.get('smscode')
        print(smscode)
        code=request.session.get('code', 0)#在保存的字典拿出来
        print(code)
        if int(smscode) == int(code):
            try:
                uesrname=request.POST.get('username')
                password=request.POST.get('password1')
                user=User.objects.get(username=uesrname)
                user.set_password(password)
                user.save()
                return JsonResponse({'ok':1})
            except Exception as e:
                return JsonResponse({'ok':0})
        else:
            return JsonResponse({'ok':0})
    # return render(request,'repassword.html')