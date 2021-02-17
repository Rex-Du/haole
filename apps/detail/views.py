from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from home.models import Article


class DetailView(APIView):
    def get(self, request, id):
        article = Article.objects.get(id=int(id))
        article.content_html = article.content_html.replace("。", '<br/>')
        return render(request, 'detail.html', locals())
