
from django.urls import path
from .views import LoginView, ResendOTPView, SignupAndSendOTPView,VerifyOTPAndSignupView, list_employers, list_jobseekers, list_recruiters
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RequestPasswordResetView, PasswordResetConfirmView

from .views import admin_login, admin_dashboard

urlpatterns = [
   
]

urlpatterns = [
     path('admin/login/', admin_login, name='admin_login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('signup/', SignupAndSendOTPView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     #path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAndSignupView.as_view(), name='verify-otp'),
     path('jobseekers/', list_jobseekers, name='list_jobseekers'),
    path('employers/', list_employers, name='list_employers'),
    path('recruiters/', list_recruiters, name='list_recruiters'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),

     path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),


]
