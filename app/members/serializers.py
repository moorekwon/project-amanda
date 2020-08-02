from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

Member = get_user_model()


class SingUpSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    gender = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(SingUpSerializer, self).get_cleaned_data()
        return {
            'gender': self.validated_data.get('gender', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        self.is_valid()
        member = Member.objects.create_user(
            gender=self.validated_data['gender'],
            email=self.validated_data['email'],
        )
        member.set_password(self.validated_data.pop('password1'))
        member.save()
        return member
