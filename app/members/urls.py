from dj_rest_auth.views import (
    LoginView, PasswordChangeView, LogoutView
)
from django.urls import path

from members.views import (
    SignupView, MemberDeleteView, MemberInfoView, MemberInfoCreateView, MemberImagesView
)

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/password/change/', PasswordChangeView.as_view()),
    path('auth/delete/', MemberDeleteView.as_view()),

    path('member/info/', MemberInfoView.as_view()),
    path('member/info/create/', MemberInfoCreateView.as_view()),

    path('member/images/', MemberImagesView.as_view()),
]
