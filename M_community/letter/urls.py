from django.conf.urls import url

from . import views

urlpatterns = [
    # 127.0.0.1:8000/letter/friend
    url(r'^friend$',views.add_friend_view),

    # 127.0.0.1:8000/letter/newfriends
    url(r'^newfriend$',views.deal_addfriend_request_view),

    url(r'^myletter$',views.process_message_view),

    url(r'^myletter_1$',views.get_friend_letter_view),

    url(r'^newfriends/(?P<username>\w+)',views.deal_newfriend_request_view),

    url(r'^myfriends/(?P<username>\w+)',views.deal_myfriend_request_view),

    # "/letter/with/+friend_name"
    url(r'^with/(?P<friendname>\w+)',views.deal_withfriend_url_view),

    # '/letter/PATCH/news/'+username
    url(r'^PATCH/news/(?P<username>\w+)',views.update_letter_is_read_view),

    url(r'^(?P<username>\w+)/with/(?P<friendname>\w+)',views.deal_withfriend_letter_view),

    url(r'^record/(?P<username>\w+)/with/(?P<friendname>\w+)',views.get_letter_record_view),

    url(r'^news$',views.get_news_view),

    url(r'^news/data$',views.get_data_news_view),
]