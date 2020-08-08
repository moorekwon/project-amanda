from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.generics import (
    RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import MemberInfo, MemberImage
from members.serializers import (
    SingUpSerializer, MemberInfoSerializer, MemberInfoCreateSerializer, MemberImageSerializer
)

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


class MemberInfoCreateView(CreateAPIView):
    queryset = MemberInfo.objects.all()
    serializer_class = MemberInfoCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.member = self.request.user
        instance.save()


class MemberImagesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        images = MemberImage.objects.filter(
            member=self.request.user
        )
        serializer = MemberImageSerializer(images, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        # 기존 내 프로필 이미지들
        my_images = MemberImage.objects.filter(
            member=self.request.user
        )

        # 새로 요청온 프로필 이미지들
        create_images = request.data.getlist('create_image')
        delete_images = request.data.getlist('delete_image_id')

        # if my_images.count() + len(create_images) - len(delete_images) < 3:
        #     raise ValueError('프로필 이미지 개수는 3장 이상 있어야 합니다.')

        # 이미지 복수 생성
        if create_images:
            arr = []
            for create_image in create_images:
                data = {
                    'image': create_image,
                }
                serializer = MemberImageSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(member=self.request.user)
                    arr.append(serializer.data)
                else:
                    return Response(serializer.errors)

        # 이미지 복수 삭제
        if delete_images:
            for image_id in delete_images:
                image = MemberImage.objects.get(id=image_id)
                image.delete()

        # 변경된 프로필 이미지들
        changed_images = MemberImage.objects.filter(
            member=self.request.user
        )
        serializer = MemberImageSerializer(changed_images, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        images = request.data.getlist('image')

        if MemberImage.objects.filter(member=self.request.user).count() + len(images) < 3:
            raise ValueError('프로필 이미지가 3개 이상 있어야 합니다.')

        arr = []
        for image in images:
            data = {
                'image': image,
            }
            serializer = MemberImageSerializer(data=data)
            if serializer.is_valid():
                serializer.save(member=self.request.user)
                arr.append(serializer.data)
            else:
                return Response(serializer.errors)
        return Response({'images': arr}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        image_ids = request.data.getlist('image_id')

        if MemberImage.objects.filter(member=self.request.user).count() - len(image_ids) < 3:
            raise ValueError('프로필 이미지가 3개 이상 있어야 합니다.')

        for image_id in image_ids:
            image = MemberImage.objects.get(id=image_id)
            image.delete()
            image.save()
        return Response('이미지가 성공적으로 삭제되었습니다.')
