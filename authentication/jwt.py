from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from authentication.models import User

class  JWTAuthentication(BaseAuthentication):
# https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
    def authenticate(self, request):
        #get the header
        auth_header= get_authorization_header(request)
        #decode as string
        auth_data = auth_header.decode('utf-8')
        #separate bearer and token in a list
        auth_token = auth_data.split(" ")
        if len(auth_token)!=2:
            raise exceptions.AuthenticationFailed('Token not valid')

        token = auth_token[1]

        #get the user. In models.py we encoded the username, email and exp in the jwt token
        ## decode the token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            username = payload['username']
            user=User.objects.get(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is expired, login again'
            )
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is invalid'
            )
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'No such user'
            )

        return super().authenticate(request)