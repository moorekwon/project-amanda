from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from members.models import Member


class JWTSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    gender = serializers.CharField(source='user.gender')
    refresh = serializers.SerializerMethodField('get_refresh')
    access = serializers.SerializerMethodField('get_access')

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def get_refresh(self, obj):
        return self.get_token(obj['user'])

    def get_access(self, obj):
        return self.get_token(obj['user']).access_token


class SignupSerializer(RegisterSerializer):
    gender = serializers.CharField()

    def save(self, request):
        self.is_valid()
        member = Member.objects.create_user(
            email=self.validated_data['email'],
            gender=self.validated_data['gender'],
        )
        member.set_password(self.validated_data.pop('password1'))
        return member
