from rest_framework import status
from rest_framework.exceptions import APIException


class NegativeNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '현재 보유량이 부족합니다.'
    default_code = 'NegativeNumber'
