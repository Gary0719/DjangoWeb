import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from essay.models import Essay


def index_view(request):
    if request.method == 'GET':
        classify = request.GET.get('classify','hot')
        page_number = request.GET.get('page',1)
        if classify == 'hot':
            essay_list = Essay.objects.filter(click_rate__gte=0)
            paginator = Paginator(essay_list, 10)
            the_page = paginator.page(page_number)
            return render(request,'index/index.html',locals())


