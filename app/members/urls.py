from dj_rest_auth.views import (
    LoginView, UserDetailsView, PasswordChangeView, LogoutView
)
from django.urls import path

from members.views import SignupView

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/password/change/', PasswordChangeView.as_view()),
    path('auth/user/', UserDetailsView.as_view()),
]
