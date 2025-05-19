from  django.urls import path
from .views import (ListPageView, DetailPageVieaw,
                    HomePageView, ContactPageView,
                    LocalNewsView, XorijNewsView,
                    SportNewsView, TechnologyNewsView,
                    UpdateNewsView, DeleteNewsView,
                    CreateNewsView, SearchListView, EditCommentView, DeleteCommentView, NewsLikeView)


app_name = 'newsapp'


urlpatterns = [
    path('search/',SearchListView.as_view(),name='search'),
    path('', HomePageView.as_view(),name='home_page'),
    path('create/',CreateNewsView.as_view(),name='create_news'),
    path('contact-us/',ContactPageView.as_view(),name='contact_page'),
    path('all-news/',ListPageView.as_view(),name='list_page'),
    path('local/',LocalNewsView.as_view(),name='local_news'),
    path('xorij/',XorijNewsView.as_view(),name='xorij_news'),
    path('sport/',SportNewsView.as_view(),name='sport_news'),
    path('technology/',TechnologyNewsView.as_view(),name='tech_news'),
    path('<slug:slug>/update/', UpdateNewsView.as_view(), name='update_news'),
    path('<slug:slug>/delete/', DeleteNewsView.as_view(), name='delete_news'),
    path('<slug:slug>/', DetailPageVieaw.as_view(), name='detail_page'),

    path('comment/<int:pk>/edit/',EditCommentView.as_view(),name='edit_comment'),
    path('comment/<int:pk>/delete/',DeleteCommentView.as_view(),name='delete_comment'),


    path("like/<slug:slug>/",NewsLikeView.as_view(),name='like'),
]