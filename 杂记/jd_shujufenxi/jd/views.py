from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Comment, Commodity
from .get_jd_comments import JdComment
from .image_jd_comments import JdShow


def index(request):
    commodity_list = Commodity.objects.filter()
    print(commodity_list)
    return render(request, 'html/index.html', {'commodity_list': commodity_list})


def detail(request, s_id):
    # s_id = request.GET.get("id")
    print("sndasndas,", s_id)
    content_list = Comment.objects.filter(p_id=s_id)
    print(content_list)
    if not content_list:
        print('数据库无此商品信息，信息采集中，请稍后')
        s_id = int(s_id)
        JdComment().run(s_id=s_id)
        content_list = Comment.objects.filter(p_id=s_id)
    return render(request, 'html/detail.html', {'content_list': content_list, 'h1': s_id})


def show_svg(request, s_id):
    print("sndasndas,", s_id)
    JdShow().run(s_id)
    with open('JD数据可视化(条形图).svg', 'r', encoding='UTF-8') as f:
        a = f.read()

    return HttpResponse(a)

