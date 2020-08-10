from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from members.models import MemberInfo, MemberImage, MemberPersonality, MemberRibbon
from utils.exceptions import NegativeNumberException

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


class PersonalitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberPersonality
        fields = (
            'personality',
        )

    def create(self, validated_data):
        member_id = self.context['request'].user.id
        member = Member.objects.get(id=member_id)
        personality = MemberPersonality.objects.create(member=member, **validated_data)
        return personality


class MemberImageSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source='member.id', read_only=True)
    image_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = MemberImage
        fields = (
            'member_id',
            'image_id',
            'image',
        )


class MemberInfoSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    profile_percent = serializers.FloatField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    ribbons = serializers.SerializerMethodField('get_ribbons')
    images = serializers.SerializerMethodField('get_images')
    personalities = serializers.SerializerMethodField('get_personalities')

    class Meta:
        model = MemberInfo
        fields = (
            'member',
            'profile_percent',
            'age',
            'ribbons',
            'images',
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
            'personalities',
            'introduce',
        )

    def get_ribbons(self, memberinfo):
        ribbons = memberinfo.member.ribbons.last().current_ribbon
        return ribbons

    def get_images(self, memberinfo):
        images = memberinfo.member.images.values_list('image', flat=True)
        return images

    def get_personalities(self, memberinfo):
        personalities = memberinfo.member.personalities.values_list('personality', flat=True)
        return personalities


class MemberInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberInfo
        fields = (
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

    def create(self, validated_data):
        member_id = self.context['request'].user.id
        member = Member.objects.get(id=member_id)
        memberinfo = MemberInfo.objects.create(member=member, **validated_data)
        return memberinfo

    def to_representation(self, instance):
        return MemberInfoSerializer(instance).data


class MemberRibbonsSerializer(serializers.ModelSerializer):
    ribbon_id = serializers.IntegerField(source='id', read_only=True)
    when = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    current_ribbon = serializers.IntegerField(read_only=True)

    class Meta:
        model = MemberRibbon
        fields = (
            'ribbon_id',
            'paid_ribbon',
            'current_ribbon',
            'when',
        )

    def create(self, validated_data):
        member_id = self.context['request'].user.id
        member = Member.objects.get(id=member_id)
        ribbons = MemberRibbon.objects.filter(member=member)
        ribbons_cnt = ribbons.aggregate(Count('member'))['member__count']
        pre = ribbons[ribbons_cnt - 1]

        try:
            current_ribbon = pre.current_ribbon + validated_data['paid_ribbon']
            assert current_ribbon >= 0
            ribbon = MemberRibbon.objects.create(member=member, current_ribbon=current_ribbon, **validated_data)
            return ribbon
        except AssertionError:
            raise NegativeNumberException()
