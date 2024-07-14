
from django.urls import path
from .views import LoginView, SignupAndSendOTPView,VerifyOTPAndSignupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


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

]
