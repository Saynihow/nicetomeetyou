from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import News
from .serializers import newsSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.
class Get_news_List(APIView):
    def get(self, request):
        news = News.objects.all()
        serialized = newsSerializer(news, many=True)
        return Response(serialized.data)

def homepage(request):
    object_list = News.objects.all().order_by('-author')
    paginator = Paginator(object_list, 5)  # 10 news in each page
    page = request.GET.get('page')  # indicates the current page number
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        news_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        news_list = paginator.page(paginator.num_pages)
    # 將news_list傳入模板逕行數據渲染，然後返回給瀏覽器

    return render(request, 'index.html', {'page':page ,'news_list': news_list})

class NewsListView(ListView):
    queryset = News.objects.all().order_by('-author')
    context_object_name = 'news_list'
    paginate_by = 5
    template_name = 'index.html'