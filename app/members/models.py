import datetime
import random
import string
import unicodedata

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from config.settings._base import AUTH_USER_MODEL

REGION = (
    ('seoul', '서울'),
    ('gyeonggi', '경기'),
    ('incheon', '인천'),
    ('daejeon', '대전'),
    ('chungbuk', '충북'),
    ('chungnam', '충남'),
    ('gangwon', '강원'),
    ('busan', '부산'),
    ('gyeongbuk', '경북'),
    ('gyeongnam', '경남'),
    ('daegu', '대구'),
    ('ulsan', '울산'),
    ('gwangju', '광주'),
    ('jeonbuk', '전북'),
    ('jeonnam', '전남'),
    ('jeju', '제주'),
)
BODY_SHAPE = (
    ('normal', '보통체형'),
    ('plump', '통통한'),
    ('curvy', '살짝볼륨'),
    ('glamor', '글래머'),
    ('thin', '마른'),
    ('slimfirm', '슬림탄탄'),
)
RELIGION = (
    ('none', '종교 없음'),
    ('christian', '기독교'),
    ('catholic', '천주교'),
    ('buddhism', '불교'),
    ('wonbuddhism', '원불교'),
    ('confucian', '유교'),
    ('islam', '이슬람교'),
)
DRINKING = (
    ('sometimes', '가끔 마심'),
    ('pretty', '어느정도 즐기는편'),
    ('very', '술자리를 즐김'),
    ('never', '마시지 않음'),
)
SMOKING = (
    ('yes', '흡연'),
    ('no', '비흡연'),
)


class UserManager(BaseUserManager):
    def create_username(self):
        username = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        username = self.create_username()
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class Member(AbstractUser):
    GENDER = (
        ('female', 'female'),
        ('male', 'male'),
    )

    gender = models.CharField(choices=GENDER, max_length=10)
    stars = models.ManyToManyField('self', through='Star', related_name='star_members', symmetrical=False)
    picks = models.ManyToManyField('self', through='Pick', related_name='pick_members', symmetrical=False)
    tag_type_selection = models.OneToOneField('TagTypeSelection', on_delete=models.CASCADE, blank=True, null=True)

    REQUIRED_FIELDS = ['gender', 'email']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class MemberInfo(models.Model):
    BLOOD_TYPE = (
        ('ab', 'AB형'),
        ('a', 'A형'),
        ('b', 'B형'),
        ('o', 'O형'),
    )

    member = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth = models.DateField(blank=False, null=True)
    nickname = models.CharField(blank=False, max_length=40)
    job = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=60, blank=True)
    school = models.CharField(max_length=50, blank=True)
    region = models.CharField(choices=REGION, max_length=30, blank=True)
    body_shape = models.CharField(choices=BODY_SHAPE, blank=True, max_length=50)
    major = models.CharField(max_length=50, blank=True)
    tall = models.PositiveIntegerField(blank=True, null=True)
    blood_type = models.CharField(choices=BLOOD_TYPE, max_length=30, blank=True)
    drinking = models.CharField(choices=DRINKING, max_length=60, blank=True)
    smoking = models.CharField(choices=SMOKING, max_length=60, blank=True)
    religion = models.CharField(choices=RELIGION, max_length=60, blank=True)
    introduce = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.member}, {self.nickname}'

    def age(self):
        today = datetime.date.today()
        today_year = str(today).split('-')[0]
        birth_year = str(self.birth).split('-')[0]
        return int(today_year) - int(birth_year) + 1

    def profile_percent(self):
        done_infos = 0

        infos = [self.job, self.company, self.school, self.region, self.body_shape, self.major, self.tall,
                 self.blood_type, self.drinking, self.smoking, self.religion, self.introduce,
                 self.member.tag_type_selection, self.member.personalities, self.member.stories]

        for info in infos:
            if not info:
                pass
            else:
                done_infos += 1

        profile_percent = done_infos / len(infos) * 100
        return format(float(profile_percent), '.1f')


class MemberIdealType(models.Model):
    member = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member')
    age_start = models.PositiveIntegerField(blank=True, null=True)
    age_end = models.PositiveIntegerField(blank=True, null=True)
    tall_start = models.PositiveIntegerField(blank=True, null=True)
    tall_end = models.PositiveIntegerField(blank=True, null=True)
    region1 = models.CharField(choices=REGION, blank=True, max_length=60)
    region2 = models.CharField(choices=REGION, blank=True, max_length=60)
    body_shape = models.CharField(choices=BODY_SHAPE, blank=True, max_length=60)
    drinking = models.CharField(choices=DRINKING, blank=True, max_length=60)
    smoking = models.CharField(choices=SMOKING, blank=True, max_length=60)
    religion = models.CharField(choices=RELIGION, blank=True, max_length=60)


class MemberPersonality(models.Model):
    PERSONALITY = (
        ('intelligent', '지적인'),
        ('calm', '차분한'),
        ('humorous', '유머있는'),
        ('optimistic', '낙천적인'),
        ('introvert', '내향적인'),
        ('extrovert', '외향적인'),
        ('emotional', '감성적인'),
        ('kind', '상냥한'),
        ('cute', '귀여운'),
        ('sexy', '섹시한'),
        ('unique', '4차원인'),
        ('cheerful', '발랄한'),
        ('cool', '도도한'),
    )

    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personalities')
    personality = models.CharField(choices=PERSONALITY, max_length=60)


class MemberImage(models.Model):
    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='member_images/')

    def __str__(self):
        return f'{self.member.email}'


# 인스턴스 생성시 S3에서도 파일 삭제
@receiver(post_delete, sender=MemberImage)
def delete_s3_image(sender, instance, *args, **kwargs):
    instance.image.delete(save=False)


class MemberRibbon(models.Model):
    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ribbons')
    paid_ribbon = models.IntegerField()
    current_ribbon = models.PositiveIntegerField()
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.member.email}, paid: {self.paid_ribbon}, current: {self.current_ribbon}'


@receiver(post_save, sender=MemberInfo)
def create_memberribbon(sender, instance, created, **kwargs):
    if created:
        MemberIdealType.objects.create(member=instance.member)
        MemberRibbon.objects.create(member=instance.member, paid_ribbon=10, current_ribbon=10)


class Star(models.Model):
    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_stars')
    partner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_stars')
    star = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.member.email} -> {self.partner.email}, {self.star}'


class Pick(models.Model):
    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_picks')
    partner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_picks')
    pick = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.member.email} -> {self.partner.email}'


class Tag(models.Model):
    name = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f'{self.name}'


class TagTypeSelection(models.Model):
    date_style = models.ManyToManyField('Tag', related_name='date_tag_type_selection', blank=True)
    life_style = models.ManyToManyField('Tag', related_name='life_tag_type_selection', blank=True)
    charm = models.ManyToManyField('Tag', related_name='charm_tag_type_selection', blank=True)
    relationship_style = models.ManyToManyField('Tag', related_name='relationship_tag_type_selection', blank=True)


class Story(models.Model):
    STORY = (
        (1, '이상적인 첫 소개팅 장소'),
        (2, '내 외모중 가장 마음에 드는 곳은'),
        (3, '남들보다 이것 하나는 자신있어요'),
    )

    member = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    story = models.CharField(choices=STORY, max_length=60, blank=True)
    content = models.CharField(max_length=60, blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.member.email}, {self.story}'
