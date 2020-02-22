from django.conf.urls import url

from essay import views

urlpatterns = [
    url(r'^post$',views.post_essay),

    # 127.0.0.1:8000/essay/detail/username/essayid
    url(r'^detail/(?P<username>\w+)/(?P<essay_id>\d+)', views.get_detail),

    # 127.0.0.1:8000/essay/comment
    url(r'^comment$', views.comment_view),

    url(r'^essay_list$', views.essay_list_views),

    url(r'^essay_data$', views.essay_data_views),

    # /essay/delete
    url(r'^delete$', views.delete_essay_views),


]