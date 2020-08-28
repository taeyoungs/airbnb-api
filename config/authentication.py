import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.META.get("HTTP_AUTHORIZATION")
        if token is not None:
            try:
                # ValueError
                xjwt, jwt_token = token.split(" ")
                # jwt.exceptions.DecodeError
                decoded = jwt.decode(
                    jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                pk = decoded.get("pk")
                user = User.objects.get(pk=pk)
                return (user, None)
            except ValueError:
                return None
            except jwt.exceptions.DecodeError:
                raise exceptions.AuthenticationFailed("Token format Invalid")
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed("No such user")
        else:
            return None

