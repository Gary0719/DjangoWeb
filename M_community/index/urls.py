from django.conf.urls import url

from . import views

urlpatterns = [
    # 127.0.0.1:8000/index/
    # 127.0.0.1:8000/index?classify=hot&page=1
    url(r'^$',views.index_view),
]