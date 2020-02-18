import json
import os

import django_redis
import jwt
from django.conf import settings
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from community_token.views import check_login
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
        try:
            # 由于无法在请求头中设置token, 将token和username加入formdata动态表单中
            # 如果token中的username和username字段的值相等, 再进一步获取数据
            # 如果不相等, 给前端返回当前未登录的消息
            # 若在检验token时发生错误, 则也给前端返回当前未登录的消息
            username = request.POST.get('username')
            token = request.POST.get('token')
            res = jwt.decode(token, key=settings.JWT_TOKEN_KEY, algorithms='HS256')
            username_ = res['username']
            if username_ == username:
                user = User.objects.get(username=username)
                if not os.path.exists(settings.MEDIA_ROOT + '/' + user.username):
                    os.makedirs(settings.MEDIA_ROOT + '/' + user.username)
                user_path = settings.MEDIA_ROOT + '/' + user.username
                image_file = request.FILES['image_file']
                video_file = request.FILES['video_file']
                title = request.POST.get('title')
                select = request.POST.get('select')
                text = request.POST.get('text')
                file_name_1 = os.path.join(user_path,image_file.name)
                with open(file_name_1,'wb') as f:
                    data = image_file.file.read()
                    f.write(data)
                file_name_2 = os.path.join(user_path,video_file.name)
                with open(file_name_2,'wb') as f:
                    data = video_file.file.read()
                    f.write(data)
                essay = Essay.objects.create(
                    title=title,
                    classify=select,
                    content=text,
                    image='/static/files/' + user.username + '/' + image_file.name,
                    video='/static/files/' + user.username + '/' + video_file.name,
                    author=user
                )
                # image, video 保存路径:
                # /static/files/Jingtian/IMG_20200218_093400.jpg
                # /static/files/Jingtian/6155d4730f0dfd933773ad289d56f9fd.mp4
                return JsonResponse({'code': 200, 'data': '发表成功!'})
            else:
                return JsonResponse({'code': 220, 'data': '当前未登录!!'})
        except Exception as e:
            print(e)
            JsonResponse({'code': 220, 'data': '当前未登录!!'})




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