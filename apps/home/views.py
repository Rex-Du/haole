from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
from pure_pagination import Paginator
from rest_framework.views import APIView

from home.models import Article


# Create your views here.


class HomeView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        if keyword:
            articles = Article.objects.filter(title__icontains=keyword).order_by('title')
        else:
            articles = Article.objects.order_by('title')
        page = request.GET.get('page', 1)
        paginator = Paginator(articles, 10, request=request)
        try:
            curr_page = paginator.page(page)
        except PageNotAnInteger:
            curr_page = paginator.page(1)
        return render(request, 'home.html', locals())
