from .models import News,Category

def latest_news(request):
    latest_news_list = News.published.all().order_by('-published_time')[:5]
    categories = Category.objects.all()
    context ={
        'latest_news_list':latest_news_list,
        'categories':categories
    }
    return context