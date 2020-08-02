from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model

from members.serializers import SingUpSerializer

Member = get_user_model()


class SignupView(RegisterView):
    serializer_class = SingUpSerializer
