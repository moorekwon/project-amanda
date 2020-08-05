from dj_rest_auth.views import (
    LoginView, PasswordChangeView, LogoutView
)
from django.urls import path

from members.views import SignupView, MemberDeleteView, MemberInfoView, MemberInfoCreateView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password/change/', PasswordChangeView.as_view()),
    path('delete/', MemberDeleteView.as_view()),
    path('member/info/', MemberInfoView.as_view()),
    path('member/info/create/', MemberInfoCreateView.as_view()),
]
