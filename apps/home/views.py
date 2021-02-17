import json

from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pure_pagination import Paginator
from rest_framework.views import APIView

from home.models import Article


class HomeView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        fav = request.GET.get('fav')
        page = request.GET.get('page', 1)
        per_page = 8
        if keyword:
            from django.db import connection
            class _Article:
                id = None
                title = None
                content_html = None
                fav = None

            cursor = connection.cursor()
            sql = f"select id, title, platform,fav from home_article where match(`content_html`) against ('\"{keyword}\"' in boolean mode) order by add_time desc "
            cursor.execute(sql)
            results = cursor.fetchall()
            articles = list()
            for result in results:
                article = _Article()
                article.id = result[0]
                article.title = result[1]
                article.platform = result[2]
                article.fav = result[3]
                articles.append(article)
        elif fav:
            articles = Article.objects.filter(status=1, fav=1).order_by('title').values('id', 'title', 'platform', 'fav')
        else:
            articles = Article.objects.filter(status=1).order_by('title').values('id', 'title', 'platform', 'fav')
        paginator = Paginator(articles, per_page, request=request)
        try:
            curr_page = paginator.page(page)
        except PageNotAnInteger:
            curr_page = paginator.page(1)
        return render(request, 'home.html', locals())


class DeleteView(APIView):
    @csrf_exempt
    def post(self, request):
        id = request.POST.get('id')
        article = Article.objects.get(id=id)
        article.status = 0
        article.save()
        return HttpResponse(json.dumps({"scu": False}))


class FavView(APIView):
    @csrf_exempt
    def post(self, request):
        id = request.POST.get('id')
        article = Article.objects.get(id=id)
        article.fav = 1
        article.save()
        return HttpResponse(json.dumps({"scu": False}))


class CancelFavView(APIView):
    @csrf_exempt
    def post(self, request):
        id = request.POST.get('id')
        article = Article.objects.get(id=id)
        article.fav = 0
        article.save()
        return HttpResponse(json.dumps({"scu": False}))