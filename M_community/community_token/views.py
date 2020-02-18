from django.conf import settings
from django.shortcuts import render

# Create your views here.


def make_token(username,exp=60*60*24):
    import time,jwt
    payload = {'username':username,'exp':time.time()+exp}   # token过期时间为一天
    key = settings.JWT_TOKEN_KEY
    return jwt.encode(payload,key,algorithm='HS256')


def check_login(request):
    token = request.META.get('HTTP_AUTHORIZATION')  # 获取请求头
    if not token:
        return None
    try:
        import jwt
        res = jwt.decode(token, key=settings.JWT_TOKEN_KEY, algorithms='HS256')
    except Exception as e:
        return None
    username = res['username']
    return username