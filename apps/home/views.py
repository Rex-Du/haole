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

            cursor = connection.cursor()
            sql = f"select id, title, platform from home_article where match(`content_html`) against ('\"{keyword}\"' in boolean mode)"
            cursor.execute(sql)
            results = cursor.fetchall()
            articles = list()
            for result in results:
                article = _Article()
                article.id = result[0]
                article.title = result[1]
                article.content_html = result[2]
                articles.append(article)
        elif fav:
            articles = Article.objects.filter(status=1, fav=fav).order_by('title').values('id', 'title', 'platform')
        else:
            articles = Article.objects.filter(status=1).order_by('title').values('id', 'title', 'platform')
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
