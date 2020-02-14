import json
import os

import django_redis
import jwt
from django.conf import settings
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from essay.models import Essay, Comment
from user.models import User
# Create your views here.
from django.views.generic.base import View

r = django_redis.get_redis_connection('essay')

# def login_check(func):
#     def wrapper(request,*args,**kwargs):
#         token = request.META.get('HTTP_AUTHORIZATION')  #获取请求头
#         if not token:
#             return JsonResponse({'code':219,'data':'当前未登录!'})
#         try:
#             res = jwt.decode(token,key=settings.JWT_TOKEN_KEY,algorithms='HS256')
#         except Exception as e:
#             return JsonResponse({'code':220,'error':'当前未登录!!'})
#         username = res['username']
#         user = User.objects.get(username=username)
#         # 将user赋值给request,方便视图函数获取当前登录用户
#         request.myuser = user
#         return func(request,*args,**kwargs)
#     return wrapper


def post_essay(request):
    if request.method == 'GET':
        return render(request,'essay/postEssay.html')
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
            return JsonResponse({'code':224,'data':'未选择图片'})
        filename = os.path.join(user_path,user_file.name)
        with open(filename,'wb') as f:
            data = user_file.file.read()
            f.write(data)
        title = r.hget(username,'title').decode()
        classify = r.hget(username,'classify').decode()
        content = r.hget(username,'content').decode()
        image_url = filename.strip()[36:]
        essay = Essay.objects.create(title=title,classify=classify,content=content,image=image_url,author=user)
        r.delete(username)
        return JsonResponse({'code':200,'data':'ok'})
    elif request.method == 'PUT':
        token = request.META.get('HTTP_AUTHORIZATION')  # 获取请求头
        if not token:
            return JsonResponse({'code': 219, 'data': '当前未登录!'})
        try:
            res = jwt.decode(token, key=settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            return JsonResponse({'code': 220, 'data': '当前未登录!!'})
        username = res['username']
        data = json.loads(request.body.decode())
        title = data.get('title')
        if not title:
            return JsonResponse({'code':221,'data':'标题未填写!'})
        classify = data.get('classify')
        if not classify:
            return JsonResponse({'code':222,'data':'话题未填写!'})
        content = data.get('content_text')
        if not content:
            return JsonResponse({'code':223,'data':'描述未填写!'})
        r.hmset(username,{'title':title,'classify':classify,'content':content})
        return JsonResponse({'code':200,'data':'ok'})


def get_detail(request,username,essay_id):
    Essay.objects.filter(id=essay_id).update(click_rate=F('click_rate')+1)
    essay = Essay.objects.get(id=essay_id)
    user = User.objects.get(username=username)
    comments = Comment.objects.filter(id__lte=15,the_essay=essay)
    # print(essay,user)
    return render(request,'essay/detail.html',locals())


def comment_view(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')  # 获取请求头
        if not token:
            return JsonResponse({'code': 219, 'data': '当前未登录!'})
        try:
            res = jwt.decode(token, key=settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            return JsonResponse({'code': 220, 'data': '当前未登录!!'})
        username = res['username']
        user = User.objects.get(username=username)
        data = json.loads(request.body.decode())
        comment = data.get('comment')
        essay_id = int(data.get('essay_id'))
        new_comment = Comment.objects.create(comment=comment,the_essay_id=essay_id,observer=user)
        data = {'username':username,'comment':comment}
        return JsonResponse({'code': 200, 'data': data})