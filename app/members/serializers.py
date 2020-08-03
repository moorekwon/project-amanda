import datetime

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from members.models import MemberInfo, MemberPersonality

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


class MemberSerializer(serializers.ModelSerializer):
    average_star = serializers.SerializerMethodField('get_average_star', read_only=True)
    status = serializers.SerializerMethodField('get_status', read_only=True)

    class Meta:
        model = Member
        fields = (
            'pk',
            'email',
            'gender',
            'stars',
            'picks',
            'tag_type_selection',
            'average_star',
            'status',
        )
        read_only_fields = ('email',)

    def get_average_star(self, member):
        try:
            avg_star = member.partner_stars.aggregate(Avg('star'))['star__avg']
            return format(float(avg_star), '.2f')
        except TypeError:
            return format(float(0), '.2f')

    def get_status(self, member):
        len_partners = member.partner_stars.aggregate(Count('partner'))['partner__count']
        if len_partners < 3:
            status = 'on_screening'
        elif len_partners >= 3 and self.get_average_star() >= 3:
            status = 'pass'
        elif len_partners >= 3 and self.get_average_star() < 3:
            status = 'fail'
        return status


class MemberInfoSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)

    class Meta:
        model = MemberInfo
        fields = (
            'member',
            'profile_percent',
            'age',
            'birth',
            'nickname',
            'job',
            'company',
            'school',
            'region',
            'body_shape',
            'major',
            'tall',
            'blood_type',
            'drinking',
            'smoking',
            'religion',
            'introduce',
        )