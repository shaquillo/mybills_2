from rest_framework import authentication, exceptions
from .models import Platforms


class PlatformsAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        name = request.headers.get('platform_name')
        token = request.headers.get('platform_token')

        if not name:
            raise exceptions.AuthenticationFailed('Did not provide platform name')

        if not token:
            raise exceptions.AuthenticationFailed('Did not provide platform token')

        try:
            pf = Platforms.objects.get(name = name)
            if pf.token == token:
                return (pf, None)
            else:
                raise exceptions.AuthenticationFailed('Token provided is not correct')

        except Platforms.DoesNotExist:
            raise exceptions.AuthenticationFailed('Platform name is not correct')