from django.conf import settings
from django.shortcuts import render

# Create your views here.


def make_token(username,exp=60*60*24):
    import time,jwt
    payload = {'username':username,'exp':time.time()+exp}   # token过期时间为一天
    key = settings.JWT_TOKEN_KEY
    return jwt.encode(payload,key,algorithm='HS256')