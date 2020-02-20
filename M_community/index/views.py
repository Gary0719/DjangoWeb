import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from essay.models import Essay
# Create your views here.



def index_view(request):
    if request.method == 'GET':
        classify = request.GET.get('classify','hot')
        page_number = request.GET.get('page',1)
        if classify == 'hot' :
            essay_list = Essay.objects.filter(click_rate__gte=0)
        elif classify == 'music':
            essay_list = Essay.objects.filter(classify='0')
        elif classify == 'film':
            essay_list = Essay.objects.filter(classify='1')
        elif classify == 'tv':
            essay_list = Essay.objects.filter(classify='2')
        elif classify == 'pet':
            essay_list = Essay.objects.filter(classify='3')
        elif classify == 'game':
            essay_list = Essay.objects.filter(classify='4')
        elif classify == 'read':
            essay_list = Essay.objects.filter(classify='5')
        elif classify == 'travel':
            essay_list = Essay.objects.filter(classify='6')

        paginator = Paginator(essay_list, 10)
        # print(paginator.count)      # 需要分页的总数
        # print(paginator.num_pages)  # 分页后总页数
        the_page = paginator.page(page_number)
        return render(request, 'index/index.html', locals())