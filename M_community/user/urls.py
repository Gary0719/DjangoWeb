from django.conf.urls import url

from user import views

urlpatterns = [
    # 127.0.0.1:8000/user/register
    url(r'^register$',views.register_view),
    # 127.0.0.1:8000/user/email
    url(r'^email$',views.email_view),
    # 127.0.0.1:8000/user/login
    url(r'^login$',views.login_view),

    # 127.0.0.1:8000/user/weibo/authorization  获取微博授权登录页
    url(r'^weibo/authorization$',views.weibo_login),
    # 127.0.0.1:8000/user/callback
    url(r'^callback$',views.callback),

    url(r'^weibo/users$',views.WeiBo.as_view()),

    url(r'^bind$',views.bind),

    url(r'^upload$',views.upload_views)
]