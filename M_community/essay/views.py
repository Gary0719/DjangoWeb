import json
import os

import django_redis
import jwt
from django.conf import settings
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from community_token.views import check_login
from essay.models import Essay, Comment, FileReference
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
                image_url = '/static/files/' + user.username + '/' + image_file.name
                video_url = '/static/files/' + user.username + '/' + video_file.name
                essay = Essay.objects.create(
                    title=title,
                    classify=select,
                    content=text,
                    image=image_url,
                    video=video_url,
                    author=user
                )

                # 查看该图片之前是否被引用过
                files_1 = FileReference.objects.filter(file_url=image_url)
                # 如果有, 对该图片的引用计数进行+1
                if files_1:
                    files_1[0].reference_number += 1
                    files_1[0].save()
                # 如果没有, 则为该图片创建引用计数对象, 并赋初始值=1
                else:
                    FileReference.objects.create(file_url=image_url,reference_number=1)

                # 查看该视频之前是否被引用过
                files_2 = FileReference.objects.filter(file_url=video_url)
                # 如果有, 对该视频的引用计数进行+1
                if files_2:
                    files_2[0].reference_number += 1
                    files_2[0].save()
                else:
                    # 如果没有, 则为该视频创建引用计数对象, 并赋初始值=1
                    FileReference.objects.create(file_url=video_url, reference_number=1)
                return JsonResponse({'code': 200, 'data': '发表成功!'})
            else:
                return JsonResponse({'code': 220, 'data': '当前未登录!!'})
        except Exception as e:
            print(e)
            JsonResponse({'code': 220, 'data': '当前未登录!!'})




def get_detail(request,username,essay_id):
    Essay.objects.filter(id=essay_id, is_active=True).update(click_rate=F('click_rate')+1)
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


def essay_list_views(request):
    if request.method == 'GET':
        return render(request, 'essay/essay_list.html')


def essay_data_views(request):
    username = check_login(request)
    if username:
        user = User.objects.get(username=username)
        essay_list = Essay.objects.filter(author=user, is_active=True)
        data = []
        for essay in essay_list:
            one_essay = {}
            one_essay['essay_id'] = essay.id
            one_essay['essay_title'] = essay.title
            if essay.classify == '0':
                one_essay['classify'] = '音乐'
            elif essay.classify == '1':
                one_essay['classify'] = '电影'
            elif essay.classify == '2':
                one_essay['classify'] = '电视剧'
            elif essay.classify == '3':
                one_essay['classify'] = '宠物'
            elif essay.classify == '4':
                one_essay['classify'] = '游戏'
            elif essay.classify == '5':
                one_essay['classify'] = '文学'
            elif essay.classify == '6':
                one_essay['classify'] = '旅游'
            one_essay['click_rate'] = essay.click_rate
            one_essay['create_time'] = essay.create_time
            one_essay['image'] = str(essay.image)
            data.append(one_essay)
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 220, 'data': '当前未登录!!'})


def delete_essay_views(request):
    if request.method == 'POST':
        username = check_login(request)
        if username:
            data = json.loads(request.body)
            essay_id = data.get('essay_id')
            essay = Essay.objects.get(id=essay_id)
            image_url = str(essay.image)
            video_url = essay.video
            file_1 = FileReference.objects.get(file_url=image_url)
            file_2 = FileReference.objects.get(file_url=video_url)
            # 如果两个文件的引用计数都为1, 则可以将两个文件删除, 该文章对象删除, 两个引用计数对象删除
            if file_1.reference_number == 1 and file_2.reference_number == 1:
                os.remove(settings.BASE_DIR + image_url)
                os.remove(settings.BASE_DIR + video_url)
                essay.delete()
                file_1.delete()
                file_2.delete()
            # 如果两个文件的引用计数都不为1, 则将两个文件的引用计数-1, 对该文章对象做伪删除
            elif file_1.reference_number != 1 and file_2.reference_number != 1:
                essay.is_active = False
                file_1.reference_number -= 1
                file_2.reference_number -= 1
                essay.save()
                file_1.save()
                file_2.save()
            # 如果图片的引用计数为1, 视频不为1, 则将图片删除, 图片的引用计数对象删除; 视频的引用计数-1, 对该文章对象做伪删除
            elif file_1.reference_number == 1 and file_2.reference_number != 1:
                os.remove(settings.BASE_DIR + image_url)
                file_1.delete()
                essay.is_active = False
                file_2.reference_number -= 1
                essay.save()
                file_2.save()
            # 如果图片的引用计数不为1, 视频为1, 则将视频文件删除, 视频的引用计数对象删除, 图片的引用计数-1, 对该文章做伪删除
            elif file_1.reference_number != 1 and file_2.reference_number == 1:
                os.remove(settings.BASE_DIR + video_url)
                file_2.delete()
                essay.is_active = False
                file_1.reference_number -= 1
                essay.save()
                file_1.save()
            return JsonResponse({'code': 200, 'data': '该文章已删除!'})
        else:
            return JsonResponse({'code': 220, 'data': '当前未登录!!'})
