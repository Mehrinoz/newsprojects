from lib2to3.fixes.fix_input import context
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import comment
from django.urls import reverse_lazy
from hitcount.models import HitCount
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from unicodedata import category

from config.custom_mixins import CheckUserLogin_and_Admin
from newsapp.forms import ContactForm, CommentForm
from newsapp.models import News, Category, Comment, NewsLike
from django.http import HttpResponse
from django.utils.translation import get_language
"""class view"""
class ListPageView(View):
    def get(self,request):
        news_list = News.published.all()
        context = {
            'news_list':news_list
        }
        return render(request,'news_list.html',context)
"""funkisya view"""
# def ListPageView(request):
#     news_list = News.published.all()#unversial usulda filtrlash
#     # news_list = News.objects.filter(status=News.Status.Published)
#     cantext = {
#         'news_list':news_list
#     }
#     return render(request,'news_list.html',cantext)
"""class detail view """
class DetailPageVieaw(HitCountDetailView,LoginRequiredMixin,View):
    def get(self, request, slug):
        comment_form = CommentForm()
        news_detail = get_object_or_404(News, slug=slug, status=News.Status.Published)
        # print('news_detail', news_detail)
        comments = news_detail.comments.filter(active=True)
        likes_count = news_detail.likes.count()
        is_liked = news_detail.likes.filter(user=request.user).exists()
        hit_count = HitCount.objects.get_for_object(news_detail)
        hit_count_response = self.hit_count(request,hit_count)
        hit_count.refresh_from_db()
        coment_count =  comments.count()


        context = {
            'news_detail': news_detail,
            'comments':comments,
            'comment_form':comment_form,
            'hit_count_response':hit_count_response,
            'hit_count':hit_count,
            'coment_count':coment_count,
            'likes_count':likes_count,
            'is_liked':is_liked
        }
        return render(request, 'news_detail.html', context)
    def post(self,request,slug):
        news_detail = get_object_or_404(News, slug=slug, status=News.Status.Published)
        comments = news_detail.comments.filter(active=True)
        new_comment = None
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_detail
            new_comment.user = request.user
            new_comment.save()
            return redirect('newsapp:detail_page',slug=news_detail.slug)
        context = {
            'news_detail': news_detail,
            'comments':comments,
            'new_comment':new_comment,
            'comment_form':comment_form,
        }
        return render(request, 'news_detail.html', context)

class TopNewsView(View):
    def get(self, request):
        news_type = ContentType.objects.get_for_model(News)
        hit_counts = HitCount.objects.filter(
            content_type=news_type
        ).order_by('-hits')[:6]
        news_hit = []
        for hit in hit_counts:
            try:
                news = News.objects.get(pk=hit.object_pk, status=News.Status.Published)
                news_hit.append(news)
            except News.DoesNotExist:
                continue

        context = {
            'news_hit': news_hit
        }
        return render(request, 'home.html', context)

class NewsLikeView(View):
    def post(self,request,slug):
        news = get_object_or_404(News,slug=slug)
        try:
            is_liked = news.likes.get(news=news,user=request.user)
            is_liked.delete()

        except NewsLike.DoesNotExist:
            NewsLike.objects.create(news=news,user=request.user)

        return redirect('newsapp:detail_page',slug=news.slug)


def get_category_db(name_uz):
    category = Category.objects.filter(name_uz=name_uz).first()

    if not category:
        return News.objects.none()
    return News.objects.filter(category=category).order_by('-published_time')[:6]


"""funkisya detiel view"""
# def DetailPageVieaw(request,id):
#     news_detail = News.published.get(id=id)
#     context = {
#         'news_detail':news_detail
#     }
#
#     return render(request,'news_detail.html',context)

"""homepage view"""

class HomePageView(View):
    def get(self,request):
        categories = Category.objects.all()
        current_language = get_language()
        # print('current_language',current_language)
        news_list = News.published.all().order_by('-published_time')
        latest_news_list = News.published.all().order_by('-published_time')[:5]
        # most_likes_count = News.objects.all().order_by('-likes')[:5]
        most_likes_count = News.published.annotate(
            like_count=Count('likes')
        ).order_by('-like_count').distinct()[:5]
        print('most_likes_count', most_likes_count)


        # local_news = News.published.filter(category__name="maxalliy").order_by('-published_time')[:6]
        # xorij_news = News.published.filter(category__name="xorij").order_by('-published_time')[:6]
        # texnology_news = News.published.filter(category__name="texnalogiya").order_by('-published_time')[:6]
        # sport_news = News.published.filter(category__name="sport").order_by('-published_time')[:6]#agar nargi usulda bo'lsa [1:6]
        local_news = get_category_db('maxalliy')
        texnology_news = get_category_db('texnalogiya')
        xorij_news = get_category_db('xorij')
        sport_news = get_category_db('sport')

        context = {
            'xorij_news':xorij_news,
            'news_list': news_list,
            'local_news': local_news,
            'latest_news_list': latest_news_list,
            'texnology_news':texnology_news,
            'sport_news':sport_news,
            'categories':categories,
            'most_likes_count':most_likes_count,
        }
        return render(request,'home.html',context)

    """contact view """
# class ContactPageView(View):
#     def get(self,request):
#         return render(request,'contact.html')
class ContactPageView(TemplateView):
    def get(self,request, *args, **kwargs):
        forms_page = ContactForm()
        context = {
            'forms_page':forms_page,
        }
        return render(request,'contact.html',context)
        # return self.render_to_response(request)
    def post(self,request,*args, **kwargs):
        forms_page = ContactForm(request.POST)
        if forms_page.is_valid():
            forms_page.save()
            return HttpResponse("<h1> sizning habaringiz yetib keldi </h1>")
        else:
            context = {
                'forms_page': forms_page,
            }
            return render(request, 'contact.html', context)
""" bu funkisya categoryani turli tilda ishlashi uchun"""
def get_category_db_(name_uz_val):
    category =  Category.objects.filter(name_uz=name_uz_val).first()
    if not category:
        return News.objects.none()
    return News.objects.filter(category=category).order_by('id')

class LocalNewsView(ListView):
    model = News
    template_name = 'local_news.html'
    context_object_name = 'page_obj'


    def get_queryset(self):
        # news = self.model.published.all().filter(category__name="maxalliy")
        news = get_category_db_('maxalliy')
        page_size=self.request.GET.get('page_size',2)
        pagination = Paginator(news,page_size)
        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        # print('page_obj',page_obj)

        return page_obj





class XorijNewsView(ListView):
    model = News
    template_name = 'xorij_news.html'
    context_object_name = 'xorijnews_list'

    def get_queryset(self):
        # news = self.model.published.all().filter(category__name="xorij")
        news = get_category_db_('xorij')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'sport_news.html'
    context_object_name = 'sportnews_list'

    def get_queryset(self):
        # news = self.model.published.all().filter(category__name="sport")
        news = get_category_db_('sport')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'texnalogya_news.html'
    context_object_name = 'texnalogyanews_list'

    def get_queryset(self):
        # news = self.model.published.all().filter(category__name="texnalogiya")
        news = get_category_db_('texnalogiya')
        return news


class UpdateNewsView(CheckUserLogin_and_Admin,UpdateView):
    model = News
    template_name = 'crud/update_news.html'
    fields = [ 'title','body','image','category','status',]

class DeleteNewsView(CheckUserLogin_and_Admin,DeleteView):
    model = News
    template_name = 'crud/delete_news.html'
    success_url = reverse_lazy('newsapp:home_page')

class CreateNewsView(CheckUserLogin_and_Admin,CreateView):
    model = News
    template_name =  'crud/create_news.html'
    fields = ['title','title_uz','title_en','title_ru',
              'body','body_uz','body_en','body_ru',
              'image',
              'category','status']


# class CommentView(View):
#     def get(self,request):
#         return render(request,'comment.html')
#     def post(self,request):
#         pass

class SearchListView(ListView):
    model = News
    template_name = 'searching_list.html'
    context_object_name = 'searching_lists'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.published.all.filter(
            Q(title__icontains=query)|Q(body_icontains=query))

class EditCommentView(LoginRequiredMixin,View):
    def get(self,request,pk):
        comment = get_object_or_404(Comment,pk=pk,user=request.user)
        form = CommentForm(instance=comment)
        context = {
            'comment':comment,
            'form':form,
        }
        return render(request,'edit_comment.html',context)

    def post(self,request,pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        form = CommentForm(instance=comment,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('newsapp:detail_page',slug=comment.news.slug)
        context = {
            'comment':comment,
            'form':form,
        }
        return render(request,'edit_comment.html',context)


class DeleteCommentView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'delete_confirm_comment.html'
    context_object_name = 'delete_comment'


    def dispatch(self, request, *args, **kwargs):
        comment =self.get_object()
        if comment.user != request.user:
            return HttpResponse('Boshqalarni izohlarini o\'chira olmaysiz')
        return super().dispatch( request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('newsapp:detail_page',kwargs={'slug':self.object.news.slug})
