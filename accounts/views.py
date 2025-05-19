from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth.forms import UserCreationForm

from config.custom_mixins import CheckUserLogin_and_Admin
from .forms import LoginForm, UserRegistrationForm, UserProfileEditForm, ProfileEditForms
from django.http import HttpResponse
from django.contrib.auth import login,authenticate

from .models import UserProfile


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             date = form.cleaned_data
#             user = authenticate(
#                 request,
#                 username = date['username'],
#                 password = date['password']
#             )
#             if user is not None:
#                 if user.is_active:
#                     login(request,user)
#                     return HttpResponse("you have been successfully logged in")
#                 else:
#                     return HttpResponse("your account is not active")
#             else:
#                 return HttpResponse('invalid login credentials')
#
#         else:
#             return HttpResponse('invalid form data')
#     else:
#         form = LoginForm()
#         return render(request,'login.html',{'form':form })

@login_required
def profile_page_view(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    print("prolife",profile)
    context = {
        'user':user,
        'profile':profile
    }
    if user.is_authenticated:
        return render(request,'registration/profile.html',context)




def signup_view(request):
    if request.method == 'POST':

        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'new_user':new_user
            }
            return render(request,'registration/signup_done.html',context)
        else:
            return render(request,'registration/signup.html',{'user_form':user_form})
    else:
        user_form =UserRegistrationForm()
        return render(request,'registration/signup.html',{'user_form':user_form})


class signUpView(View):
    def post(self,request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(user=new_user)
            context = {
                'new_user': new_user,

            }
            return render(request, 'registration/signup_done.html', context)
        else:
            return render(request, 'registration/signup.html', {'user_form': user_form})
    def get(self,request):
        user_form = UserRegistrationForm()

        return render(request, 'registration/signup.html', {'user_form': user_form })


class UserRegisterCreateView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:signup_done')


class ProfileEditView(LoginRequiredMixin,View):
    def get(self,request):
        user_form = UserProfileEditForm(instance=request.user)
        profile_form =ProfileEditForms(instance=request.user.userprofile)
        # print('user_form g', user_form)
        # print('profile_form g', profile_form)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request,'registration/profile_edit.html',context)
    def post(self,request):
        user_form = UserProfileEditForm(instance=request.user,data=request.POST)
        profile_form =ProfileEditForms(instance=request.user.userprofile,data=request.POST,
                                       files=request.FILES)
        # print('user_form p', user_form)
        # print('profile_form p', profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('accounts:profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'profile_edit.html', context)
            # return HttpResponse("Invalid forum data ")


@login_required(login_url='accounts:login')
@user_passes_test(lambda user:user.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)
    context ={
        'admin_user':admin_user
    }
    return render(request,'admin_page.html',context)



