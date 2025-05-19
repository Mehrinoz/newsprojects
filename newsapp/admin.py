from django.contrib import admin
from django.utils.translation.trans_null import activate

from .models import Category, News, ContactModel, Comment, NewsLike


# admin.site.register(Category)
# admin.site.register(News)
# @admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('id','title','status','category','created_time','updated_time')
    list_filter = ['status','category', 'updated_time', 'status']
    search_fields = ['title','status','category__name','created_time','updated_time']

    prepopulated_fields =   { 'slug':('title',)}
    date_hierarchy = 'published_time'
    ordering = ['status','published_time']

# @admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['name']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email']

# @admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user','body','active','created_time']
    list_filter = ['active','created_time']
    search_fields = ['user','body']
    actions = ['disabled_actived','enabled_actived']

    def disabled_actived(self,request,queryset):
        queryset.update(active=False)

    def enabled_actived(self,request,queryset):
        queryset.update(active=True)
@admin.register(NewsLike)
class NewsLikeAdmin(admin.ModelAdmin):
    list_display = ['user','news']






admin.site.register(Comment,AdminComment)
admin.site.register(News,AdminNews)
admin.site.register(Category,AdminCategory)
admin.site.register(ContactModel,ContactAdmin)