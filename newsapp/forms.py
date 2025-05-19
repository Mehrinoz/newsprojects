from django.forms import Form,ModelForm
from .models import ContactModel, Comment
from django import forms
class ContactForm(ModelForm):
    class Meta:
        model = ContactModel
        # fields = ['name','email','phone','massage']
        fields = '__all__'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

