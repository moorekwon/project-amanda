from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from members.serializers import SingUpSerializer

Member = get_user_model()


class SignupView(RegisterView):
    serializer_class = SingUpSerializer


class MemberDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Member.objects.all()

    def get_object(self):
        return self.request.user
