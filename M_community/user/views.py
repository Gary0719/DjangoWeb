import base64
import hashlib
import json
import os
import random
import re
from urllib.parse import urlencode
import django_redis
import jwt
import requests
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from community_token.views import make_token, check_login
from .tasks import send_active_email
from .models import User, WeiboUser


# Create your views here.


def activate_email(user):
    random_number = random.randint(1000,9999)
    random_str = user.username + '-' + str(random_number)
    random_code = base64.urlsafe_b64encode(random_str.encode())
    activate_url = 'http://127.0.0.1:8000/user/email?code=%s'%(random_code.decode())
    red = django_redis.get_redis_connection('email')
    red.set('email_activate_code_%s'%user.username,random_number)   # 将相应用户的随机码存入redis进行缓存
    red.expire('email_activate_code_%s'%user.username,60*60*24)    # 对缓存设置过期时间:1天
    return activate_url


def register_view(request):
    if request.method == 'GET':
        return render(request,'user/register.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        # 获取用户名,并进行验证,不能为空且只能由数字,字母,下划线组成
        username = data.get('username')
        if not username:
            return JsonResponse({'code':201,'data':'用户名不能为空'})
        pattern = r'[a-zA-Z0-9_]+'
        result = re.findall(pattern,username)[0]
        if result != username:
            return JsonResponse({'code':205,'data':'用户名不合法'})
        # 获取密码,并进行验证,两次密码必须一致,且6~12位
        password_1 = data.get('password_1')
        if not password_1:
            return JsonResponse({'code':202,'data':'密码不能为空'})
        password_2 = data.get('password_2')
        if not password_2:
            return JsonResponse({'code':203,'data':'请确认密码'})
        if password_1 != password_2:
            return JsonResponse({'code':206,'data':'两次密码不一致'})
        if len(password_1)<6 or len(password_1)>12:
            return JsonResponse({'code':207,'data':'密码不符合长度'})
        gender = data.get('gender')
        email = data.get('email')
        if not email:
            return JsonResponse({'code':204,'data':'邮箱不能为空'})
        pattern = r'@\w+.\w+'
        res = re.findall(pattern, email)
        print(res)
        if not res:
            return JsonResponse({'code':208,'data':'邮箱地址不合法'})
        # 进行到此处说明用户信息初步验证通过,尝试数据库中创建用户,若成功则跳转到邮箱激活页面
        md = hashlib.md5()
        md.update(password_1.encode())
        password = md.hexdigest()   # 定长输出 32位
        try:
            user = User.objects.create(username=username,password=password,gender=gender,email=email, head_portrait='/static/image/default_head.jpg')
        except Exception:
            return JsonResponse({'code':209,'data':'该用户名已被占用'})
        print('注册成功')
        activate_url = activate_email(user) # 生链接
        send_active_email.delay(activate_url,user.email)  # 发邮件
        # 需要在终端执行 celery - A M_community worker - -loglevel = info 此命令,启动celery ! ! ! ! ! !
        # 连按两次 Ctrl+C 退出
        token = make_token(username)    # 造token
        return JsonResponse({'code':200,'data':{'username':username, 'head':str(user.head_portrait),'token':token.decode()}})


def email_view(request):
    if request.method != 'GET':
        return JsonResponse({'code':210,'data':'请求方式错误'})
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'code':211,'data':'激活码不能为空'})
    try:
        code_str = base64.urlsafe_b64decode(code.encode())
        username,number = code_str.decode().split('-')
        print(username)
    except Exception:
        return JsonResponse({'code':212,'data':'激活码错误'})
    r = django_redis.get_redis_connection('email')
    random_number = r.get('email_activate_code_'+username)
    if not random_number:
        return JsonResponse({'code':213,'data':'激活码已过期'})
    if random_number.decode() == number:
        try:
            user = User.objects.get(username=username,is_active=False)
            user.is_active = True
            user.save()
            r.delete('email_activate_code_'+username)
            return render(request,'index/index.html')
        except Exception:
            return JsonResponse({'code':214,'data':'激活失败'})
    else:
        return JsonResponse({'code':215,'data':'激活码错误'})


def login_view(request):
    if request.method == 'GET':
        return render(request,'user/login.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # print(username,password)
        if not username:
            return JsonResponse({'code':216,'data':'用户名不能为空'})
        if not password:
            return JsonResponse({'code':217,'data':'密码不能为空'})
        user = User.objects.filter(username=username)
        if not user:
            return JsonResponse({'code':218,'data':'用户名或密码错误'})
        md = hashlib.md5()
        md.update(password.encode())
        password = md.hexdigest()
        if password != user[0].password:
            return JsonResponse({'code':218,'data':'用户名或密码错误'})
        token = make_token(username)
        head_url = str(user[0].head_portrait)
        if not head_url:
            head_url = '/static/image/default_head.jpg'
        return JsonResponse({'code':200,'data':{'username':username,'head':head_url,'token':token.decode()}})

def get_weibo_login_url():
    # 生成微博授权登录页面地址
    # 如果需要高级权限 需要在此声明scope
    params = {
        'response_code': 'code',
        'client_id':settings.WEIBO_CLIENT_ID,
        'redirect_uri':settings.WEIBO_RETURN_URL,
    }
    login_url = 'https://api.weibo.com/oauth2/authorize?'
    url = login_url + urlencode(params)
    return url


def weibo_login(request):
    url = get_weibo_login_url()
    # https://api.weibo.com/oauth2/authorize?response_code=code&client_id=2900349074&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fuser%2Fcallback
    return JsonResponse({'code': 200, 'oauth_url': url})

# http://127.0.0.1:8000/user/callback?code=6b8d2429d82d58e9129a8962364239cd
def get_access_token(code):
    # 向第三方认证服务器发送code,交换token
    token_url = 'https://api.weibo.com/oauth2/access_token'
    post_data = {
        'client_id':settings.WEIBO_CLIENT_ID,
        'client_secret':settings.WEIBO_CLIENT_SECRET,
        'grant_type':'authorization_code',
        'redirect_uri': settings.WEIBO_RETURN_URL,
        'code':code
    }
    try:
        res = requests.post(token_url,data=post_data)
    except Exception as e:
        print('weibo exchange error')
        return None
    if res.status_code == 200:
        return json.loads(res.text)
    return None


class WeiBo(View):
    def get(self, request):
        code = request.GET.get('code')
        # 执行函数,后端最终向第三方获取access_token
        result = get_access_token(code)
        # print(result)
        # {'access_token': '2.00w2kyAI0mFb3g5eb13671401XRPBC', 'remind_in': '157679999', 'expires_in': 157679999, 'uid': '7343540520', 'isRealName': 'true'}
        wuid = result.get('uid')
        access_token = result.get('access_token')
        try:
            weibo_user = WeiboUser.objects.get(wuid=wuid)
        except Exception as e:
            # 第一次用微博登录,在微博用户表中创建数据
            WeiboUser.objects.create(wuid=wuid, access_token=access_token)
            result = {'code': 224, 'uid': wuid}  # 让前端跳转页面,让用户进行本网站账号的绑定
            return JsonResponse(result)
        else:
            # 非第一次登录,weibouser表里有wuid对应的数据
            uid = weibo_user.uid
            if uid:
                # 之前已经绑定注册过我们网站的用户
                username = uid.username
                user = User.objects.get(username=username)
                token = make_token(username)
                # print(username)
                # print(str(user.head_portrait))
                return JsonResponse({'code': 200, 'data':{'username': username, 'head': str(user.head_portrait), 'token': token.decode()}})
            else:
                # 之前用过当前微博账号登陆过,但没有完成后续的绑定注册流程
                result = {'code': 224, 'uid': wuid}
                return JsonResponse(result)  # 让前端跳转页面,让用户进行本网站账号的绑定

    # 跳转至本网站账号绑定的页面后,用post请求提交数据
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username:
            return JsonResponse({'code': 291, 'data': '用户名不能为空!'})
        if not password:
            return JsonResponse({'code': 292, 'data': '密码不能为空!'})
        wuid = data.get('wuid')
        md = hashlib.md5()
        md.update(password.encode())
        password_md = md.hexdigest()
        print(username)
        print(password)
        # 当有多条数据需要更新时 要考虑是否使用事务
        try:
            with transaction.atomic():
                user = User.objects.get(username=username)
                if user.password == password_md:
                    weibo_user = WeiboUser.objects.get(wuid=wuid)
                    weibo_user.uid = user
                    weibo_user.save()
                    token = make_token(username)  # 进行到此处说明用户已完成注册,可以登录,签发token传至前端
                    return JsonResponse({'code': 200, 'data': {'username': username, 'head': str(user.head_portrait), 'token': token.decode()}})
                else:
                    return JsonResponse({'code': 293, 'data': '用户名或密码错误!'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 294, 'data': '登录失败, 请重试!'})



def callback(request):
    return render(request,'user/callback.html')


def bind(request):
    return render(request,'user/bind.html')


def upload_views(request):
    if request.method == 'GET':
        return render(request,'user/upload.html')
    elif request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')  # 获取请求头
        if not token:
            return JsonResponse({'code': 219, 'data': '当前未登录!'})
        try:
            res = jwt.decode(token, key=settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            return JsonResponse({'code': 220, 'data': '当前未登录!!'})
        username = res['username']
        user = User.objects.get(username=username)
        if not os.path.exists(settings.MEDIA_ROOT + '/' + username):
            os.makedirs(settings.MEDIA_ROOT + '/' + username)
        user_path = settings.MEDIA_ROOT + '/' + username
        try:
            user_file = request.FILES['image']
        except Exception as e:
            return JsonResponse({'code': 224, 'data': '未选择图片'})
        filename = os.path.join(user_path, user_file.name)
        with open(filename, 'wb') as f:
            data = user_file.file.read()
            f.write(data)
        # /static/files/Gary/头像_2.jpg
        head_portrait =  '/static/files/' + username + '/' + user_file.name
        user.head_portrait = head_portrait
        user.save()
        return JsonResponse({'code':200,'data':('头像更新成功',head_portrait)})


def modify_views(request):
    if request.method == 'GET':
        return render(request, 'user/modify.html')


# def modify_data_views(request):
#     if request.method == 'GET':
#         username = check_login(request)
#         if username:
#             user = User.objects.get(username=username)
#             username = user.username
#             gender = user.gender
#             head = str(user.head_portrait)
#             return JsonResponse({'code': 200, 'data': {'username': username, 'gender': gender, 'head': head}})
#         else:
#             return JsonResponse({'code': 220, 'data': '当前未登录!!'})
