from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from pure_pagination import Paginator
from rest_framework.views import APIView

from home.models import Article

from rest_framework.authentication import BasicAuthentication


# Create your views here.


class HomeView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        if keyword:
            articles = Article.objects.filter(
                Q(title__icontains=keyword) | Q(content_html__icontains=keyword)).order_by(
                'title').values('id', 'title', 'platform')
        else:
            articles = Article.objects.order_by('title').values('id', 'title', 'platform')
        page = request.GET.get('page', 1)
        paginator = Paginator(articles, 10, request=request)
        try:
            curr_page = paginator.page(page)
        except PageNotAnInteger:
            curr_page = paginator.page(1)
        return render(request, 'home.html', locals())
