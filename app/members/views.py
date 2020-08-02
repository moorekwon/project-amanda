from dj_rest_auth.registration.views import RegisterView

from members.serializers import SignupSerializer


class SignupView(RegisterView):
    serializer_class = SignupSerializer
