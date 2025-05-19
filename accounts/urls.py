from django.urls import path
from .views import profile_page_view, signup_view, signUpView, UserRegisterCreateView, ProfileEditView, admin_page_view
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
app_name ='accounts'

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('password_change/',PasswordChangeView.as_view(),name='password_change'),
    path('password_change_done/',PasswordChangeDoneView.as_view(),name='password_change_done'),

    path('password-reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset/complete',PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    # path('signup/',signup_view,name='signup')#fuktion view,
    path('signup/',signUpView.as_view(),name='signup'),#oddiy view
    # path('signup/',UserRegisterCreateView.as_view(),name='signup'),#generik view

    path('profile/',profile_page_view,name='profile'),
    path('profile/edit',ProfileEditView.as_view(),name='profile_edit'),


    path('adminpage/',admin_page_view,name='adminpage'),
]