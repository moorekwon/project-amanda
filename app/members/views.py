from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from members.models import MemberInfo
from members.serializers import SingUpSerializer, MemberInfoSerializer

Member = get_user_model()


class SignupView(RegisterView):
    serializer_class = SingUpSerializer


class MemberDeleteView(DestroyAPIView):
    queryset = Member.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class MemberInfoView(RetrieveUpdateAPIView):
    queryset = MemberInfo.objects.all()
    serializer_class = MemberInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            memberinfo = MemberInfo.objects.get(
                member=self.request.user
            )
        except ObjectDoesNotExist:
            raise ValueError('해당 유저의 memberinfo가 존재하지 않습니다.')
        return memberinfo
