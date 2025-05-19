from modeltranslation.translator import register, TranslationOptions, translator
from .models import News,Category
@register(News)
class NewsTranslation(TranslationOptions):
    fields = ('title','body')
@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name',)

# translator.register(News,NewsTranslation)# hohlagan usulda
