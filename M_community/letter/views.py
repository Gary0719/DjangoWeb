import json

import django_redis
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from letter.models import Friend, Letter
from user.models import User
# Create your views here.



# 获取请求头中的token,如果没有token或者token验证失败,返回none,
# 验证成功说明用户处于登录状态,返回当前用户的用户名
def check_login(request):
    token = request.META.get('HTTP_AUTHORIZATION')  # 获取请求头
    if not token:
        return None
    try:
        res = jwt.decode(token, key=settings.JWT_TOKEN_KEY, algorithms='HS256')
    except Exception as e:
        return None
    username = res['username']
    return username


def get_news(user):
    '''
    通过传入一个用户对象,返回该用户的所有未读消息列表
    :param user: 一个用户对象
    :return: 该用户的所有未读消息列表
    '''
    friends_list_1 = Friend.objects.filter(from_id=user.id, is_active=True)
    friends_list_2 = Friend.objects.filter(to_id=user.id, is_active=True)
    letters = []
    if friends_list_1:
        for friend in friends_list_1:
            letters_list = Letter.objects.filter(friend=friend, is_read=False)
            for letter in letters_list:
                if letter.sender != user.username:
                    letters.append(letter)
    if friends_list_2:
        for friend in friends_list_2:
            letters_list = Letter.objects.filter(friend=friend, is_read=False)
            for letter in letters_list:
                if letter.sender != user.username:
                    letters.append(letter)
    return letters


def add_friend_view(request):
    if request.method == 'GET':
        return render(request,'letter/addfriends.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        friend_name = data.get('friend_name')
        if not friend_name:
            return JsonResponse({'code': 270, 'data': '输入好友昵称不能为空'})
        try:
            friend = User.objects.get(username=friend_name)
        except Exception as e:
            return JsonResponse({'code': 271, 'data': '未搜索到该用户'})
        friend_name = friend.username
        friend_head_portrait = str(friend.head_portrait)
        if friend.gender == '0':
            friend_gender = '女生'
            return JsonResponse({'code': 200, 'data': (friend_name, friend_gender, friend_head_portrait)})
        elif friend.gender == '1':
            friend_gender = '男生'
            return JsonResponse({'code': 200, 'data': (friend_name, friend_gender, friend_head_portrait)})


# 处理添加好友的请求
def deal_addfriend_request_view(request):
    if request.method == 'POST':
        the_user = check_login(request)
        if the_user:
            data = json.loads(request.body)
            target_friend = data.get('target_friend')
            if target_friend == the_user:
                return JsonResponse({'code': 273, 'data': '不能添加自己为好友嗷~~!'})
            from_user = User.objects.get(username=the_user)
            to_user = User.objects.get(username=target_friend)
            friend_1 = Friend.objects.filter(from_id=from_user.id,to_id=to_user.id,is_active=True)
            friend_2 = Friend.objects.filter(to_id=from_user.id,from_id=to_user.id,is_active=True)
            friend_3 = Friend.objects.filter(from_id=from_user.id, to_id=to_user.id, is_active=False)
            friend_4 = Friend.objects.filter(to_id=from_user.id, from_id=to_user.id, is_active=False)
            if not friend_1 and not friend_2 :
                if not friend_3 and not friend_4:
                    friend = Friend.objects.create(from_id=from_user.id,to_id=to_user.id)
                    return JsonResponse({'code':200,'data':'好友申请已发送!'})
                else:
                    return JsonResponse({'code': 274, 'data': '您的好友申请已发送,对方还没有同意哦~'})
            elif friend_1 or friend_2:
                return JsonResponse({'code': 272, 'data': '你们当前已是好友啦!'})
        else:
            return JsonResponse({'code': 220, 'data': '当前未登录'})


# 首页获取添加好友的消息状态的函数
def process_message_view(request):
    if request.method == 'GET':
        the_user = check_login(request)
        if the_user:
            the_user = User.objects.get(username=the_user)
            addfriend_message_list = Friend.objects.filter(to_id=the_user.id,is_active=False)
            if addfriend_message_list:
                message_list= []
                for message in addfriend_message_list:
                    user = User.objects.get(id=message.from_id)
                    # print('来自', user.username, '的好友请求')
                    message_list.append(user.username)
                return JsonResponse({'code':283,'data':message_list})
            else:
                return JsonResponse({'code':282,'data':'没有新的好友请求'})
        else:
            return JsonResponse({'code':281,'data':'未获取到当前登录信息'})


def deal_newfriend_request_view(request,username):
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        print(e)
    if request.method == 'GET':
        addfriend_message_list = Friend.objects.filter(to_id=user.id,is_active=False)
        if addfriend_message_list:
            friends_info = []
            for message in addfriend_message_list:
                user = User.objects.get(id=message.from_id)
                friends_info.append({'friend_name':user.username,'friend_gender':user.gender,'friend_head':str(user.head_portrait)})
            return render(request,'letter/newfriends.html',{'data':friends_info})
        else:
            return render(request, 'letter/newfriends.html')

    elif request.method == 'POST':
        the_user = check_login(request)
        if username != the_user:
            return JsonResponse({'code':281,'data':'未获取到当前登录信息'})
        data = json.loads(request.body)
        option = data.get('option')
        print(option)
        if option == '1':
            try:
                agree_friend = data.get('agree_friend')
                the_user = User.objects.get(username=agree_friend)
                one_friend = Friend.objects.get(from_id=the_user.id,to_id=user.id,is_active=False)
                print(one_friend)
                one_friend.is_active = True
                one_friend.save()
                return JsonResponse({'code':200,'data':'你和%s已经成为好友啦~'%agree_friend})
            except Exception as e:
                return JsonResponse({'code': 291, 'data':'系统错误'})
        elif option == '0':
            try:
                ignore_friend = data.get('ignore_friend')
                the_user = User.objects.get(username=ignore_friend)
                one_friend = Friend.objects.get(from_id=the_user.id,to_id=user.id,is_active=False)
                one_friend.delete()
                return JsonResponse({'code':200,'data':'拒绝来自%s的好友请求'%ignore_friend})
            except Exception as e:
                return JsonResponse({'code': 291, 'data':'系统错误'})


def deal_myfriend_request_view(request,username):
    if request.method == 'GET':
        try:
            the_user = User.objects.get(username=username)
            friends_list_1 = Friend.objects.filter(from_id=the_user.id, is_active=True)
            friends_list_2 = Friend.objects.filter(to_id=the_user.id, is_active=True)
            friends_list = []
            if friends_list_1:
                for a in friends_list_1:
                    friend = User.objects.get(id=a.to_id)
                    friends_list.append(
                        {'username': friend.username, 'gender': friend.gender, 'head': str(friend.head_portrait)})
            if friends_list_2:
                for b in friends_list_2:
                    friend = User.objects.get(id=b.from_id)
                    friends_list.append(
                        {'username': friend.username, 'gender': friend.gender, 'head': str(friend.head_portrait)})
            return render(request, 'letter/myfriends.html', {'data': friends_list})
        except Exception as e:
            print(e)


# 生成一个url返回给前端,让前端重定向到该地址
def deal_withfriend_url_view(request,friendname):
    if request.method == 'GET':
        the_user = check_login(request)
        if the_user :

            url = '/letter/'+the_user+'/with/' + friendname

            return JsonResponse({'code':200,'data':url})
        else:
            return JsonResponse({'code':281,'data':'未获取到当前登录信息'})


def deal_withfriend_letter_view(request,username,friendname):
    if request.method == 'GET':
        try:
            friend = User.objects.get(username=friendname)
            head_photo = friend.head_portrait
            # print('当前用户:',username)
            # print('当前好友:',friendname)
            return render(request,'letter/letter.html',{'name':friendname,'image':str(head_photo)})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 276, 'data': '未获取到当前好友'})
    elif request.method == 'POST':
        username = check_login(request)
        if username:
            data = json.loads(request.body)
            letter = data.get('letter')
            print(letter)
            # 验证消息是否合法:
            if len(letter) > 40:
                return JsonResponse({'code':277,'data':'单条消息长度超过最大值'})
            if not letter:
                return JsonResponse({'code': 278, 'data': '消息不能为空'})
            try:
                the_user = User.objects.get(username=username)
                the_friend = User.objects.get(username=friendname)
                friend_1 = Friend.objects.filter(from_id=the_user.id,to_id=the_friend.id,is_active=True)
                friend_2 = Friend.objects.filter(from_id=the_friend.id,to_id=the_user.id,is_active=True)
                if friend_1:
                    one_letter = Letter.objects.create(letter=letter, sender=username, friend=friend_1[0],is_read=False)
                elif friend_2:
                    one_letter = Letter.objects.create(letter=letter, sender=username, friend=friend_2[0],is_read=False)
                else:
                    return JsonResponse({'code':276,'data':'未获取到当前好友'})
                letter = one_letter.letter
                create_time = one_letter.create_time
                return JsonResponse({'code': 200, 'data': [letter,create_time]})
                # return JsonResponse({'code': 200, 'data': 'ok'})
            except Exception as e:
                return JsonResponse({'code':275,'data':'用户名错误'})
        else:
            JsonResponse({'code': 220, 'data': '当前未登录'})


def get_letter_record_view(request,username,friendname):
    if request.method == 'GET':
        the_user = check_login(request)
        if the_user == username:
            the_user = User.objects.get(username=username)
            the_friend = User.objects.get(username=friendname)
            friend_1 = Friend.objects.filter(from_id=the_user.id, to_id=the_friend.id, is_active=True)
            friend_2 = Friend.objects.filter(from_id=the_friend.id, to_id=the_user.id, is_active=True)
            if friend_1:
                letters = Letter.objects.filter(friend=friend_1)
            if friend_2:
                letters = Letter.objects.filter(friend=friend_2)
            letters_list = []
            for letter in letters:
                letter_dict = {}
                letter_dict['letter'] = letter.letter
                letter_dict['sender'] = letter.sender
                letters_list.append(letter_dict)
                # 把留言的阅读状态改为已读
                # letter.is_read = True
                # letter.save()
            return JsonResponse({'code':200,'data':letters_list[-6:]})
        else:
            return JsonResponse({'code': 281, 'data': '未获取到当前登录信息'})


# 首页获取好友留言的函数
def get_friend_letter_view(request):
    if request.method == 'GET':
        the_user = check_login(request)
        if the_user:
            the_user = User.objects.get(username=the_user)
            letters_list = get_news(the_user)
            if letters_list:
                return JsonResponse({'code': 200, 'data': len(letters_list)})
            return JsonResponse({'code': 279, 'data': '没有新消息'})
        return JsonResponse({'code': 281, 'data': '未获取到当前登录信息'})


def get_news_view(request):
    if request.method == 'GET':
        return render(request, 'letter/news.html')


def get_data_news_view(request):
    if request.method == 'GET':
        the_user = check_login(request)
        if the_user :
            the_user = User.objects.get(username=the_user)
            letters_list = get_news(the_user)
            person = set()
            for item in letters_list:
                person.add(item.sender)
            result = {}
            for one in person:
                number = []
                for item in letters_list:
                    if one == item.sender:
                        number.append(item.letter)
                result[one] = [len(number)]
            for item in result:
                user = User.objects.get(username=item)
                head_url = user.head_portrait
                result[item].append(str(head_url))
            person = list(person)
            return JsonResponse({'code':200,'data':[person,result]})
        else:
            return JsonResponse({'code': 281, 'data': '未获取到当前登录信息'})


def update_letter_is_read_view(request,username):
    if request.method == 'PATCH':
        the_user = check_login(request)
        if the_user == username:
            data = json.loads(request.body)
            friend = data.get('friend')
            is_read = data.get('is_read')
            # 当用户点击查看与该好友的新消息时;当用户点击获取与该好友的留言板界面时,
            # 更新数据库,将好友发来的未读消息更新为已读
            the_user = User.objects.get(username=username)
            the_friend = User.objects.get(username=friend)
            friend_1 = Friend.objects.filter(from_id=the_user.id, to_id=the_friend.id, is_active=True)
            friend_2 = Friend.objects.filter(from_id=the_friend.id, to_id=the_user.id, is_active=True)
            if friend_1:
                letters = Letter.objects.filter(friend=friend_1,sender=friend,is_read=False)
            if friend_2:
                letters = Letter.objects.filter(friend=friend_2,sender=friend,is_read=False)
            for letter in letters:
                letter.is_read = True
                letter.save()
            return JsonResponse({'code':200,'data':'ok'})