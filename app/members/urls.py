from dj_rest_auth.views import (
    LoginView, UserDetailsView, PasswordChangeView, LogoutView
)
from django.urls import path

from members.views import SignupView, MemberDeleteView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password/change/', PasswordChangeView.as_view()),
    path('delete/', MemberDeleteView.as_view()),
    path('user/', UserDetailsView.as_view()),
]
