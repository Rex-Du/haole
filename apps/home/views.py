from math import ceil

from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
from pure_pagination import Paginator
from pure_pagination.paginator import Page
from rest_framework.views import APIView
from elasticsearch import Elasticsearch

from home.models import Article

from rest_framework.authentication import BasicAuthentication


# Create your views here.
class ESPaginator:
    def __init__(self, request, per_page, count):
        self.request = request
        self.per_page = per_page
        self.count = count
        hits = max(1, self.count)
        self.num_pages = int(ceil(hits / float(self.per_page)))


class HomeView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        page = request.GET.get('page', 1)
        per_page = 8
        if keyword:
            # articles = Article.objects.filter(title__icontains=keyword).order_by('title').values(
            #     'id', 'title', 'platform')
            es = Elasticsearch(["111.229.61.201:9200"])
            body = {
                "query": {
                    "match_phrase": {
                        "content_html": {
                            "query": keyword
                        }
                    }
                },
                "_source": ["id", "title", "platform"],
                "size": per_page,
                "from": page
            }
            results = es.search(index='haolearticle', body=body)
            articles = [result.get('_source') for result in results.get('hits').get('hits')]
            curr_page = Page(articles, page, ESPaginator(request, per_page, count=results.get('hits').get('total')))
        else:
            articles = Article.objects.order_by('title').values('id', 'title', 'platform')
            paginator = Paginator(articles, per_page, request=request)
            try:
                curr_page = paginator.page(page)
            except PageNotAnInteger:
                curr_page = paginator.page(1)
        return render(request, 'home.html', locals())
