import json
from math import ceil

from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pure_pagination import Paginator
from pure_pagination.paginator import Page
from rest_framework.views import APIView
from elasticsearch import Elasticsearch

from home.models import Article

from rest_framework.authentication import BasicAuthentication


# es = Elasticsearch(["111.229.61.201:9200"])
#
#
# # Create your views here.
# class ESPaginator:
#     def __init__(self, request, per_page, count):
#         self.request = request
#         self.per_page = per_page
#         self.count = count
#         hits = max(1, self.count)
#         self.num_pages = int(ceil(hits / float(self.per_page)))


class HomeView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        page = request.GET.get('page', 1)
        per_page = 8
        if keyword:
            # articles = Article.objects.filter(title__icontains=keyword).order_by('title').values(
            #     'id', 'title', 'platform')
            # body = {
            #     "query": {
            #         "match_phrase": {
            #             "content_html": {
            #                 "query": keyword
            #             }
            #         }
            #     },
            #     "_source": ["id", "title", "platform", "status"],
            #     "size": per_page,
            #     "from": (int(page)-1)*per_page
            # }
            # results = es.search(index='haolearticle', body=body)
            # articles = [result.get('_source') for result in results.get('hits').get('hits')]
            # curr_page = Page(articles, page, ESPaginator(request, per_page, count=results.get('hits').get('total')))
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
        # query = {'query': {'match': {'id': id}}}
        # es.delete_by_query(index='haolearticle', body=query)
        article = Article.objects.get(id=id)
        article.status = 0
        article.save()
        return HttpResponse(json.dumps({"scu": False}))
