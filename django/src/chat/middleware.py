import re

from django.apps import apps
from django.utils.functional import empty

from channels.db import database_sync_to_async
from channels.auth import AuthMiddleware, UserLazyObject


class BaseAuthTokenMiddleware(AuthMiddleware):

    async def resolve_scope(self, scope):
        # Get user instance if it not already in the scope.
        if scope["user"]._wrapped is empty or scope["user"].is_anonymous:
            scope["user"]._wrapped = await self.get_user(scope)

    async def get_user(self, scope):
        # postpone model import to avoid ImproperlyConfigured error before
        # Django setup is complete.
        from django.contrib.auth.models import AnonymousUser

        token_key = self.parse_token_key(scope)
        if not token_key:
            return AnonymousUser()

        user = await self.get_user_instance(token_key)
        return user or AnonymousUser()

    def parse_token_key(self, scope):
        headers = dict(scope['headers'])
        key = headers.get(b'authorization', b'').decode()
        matched = re.fullmatch(rf'{self.keyword} ({self.value_regexp})', key)

        if not matched:
            return None
        return matched.group(1)


class DRFAuthTokenMiddleware(BaseAuthTokenMiddleware):

    keyword = 'Token'
    value_regexp = '[0-9a-f]{40}'

    @database_sync_to_async
    def get_user_instance(self, token_key):
        Token = apps.get_model('authtoken', 'Token')
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None


class JWTAuthTokenMiddleware(BaseAuthTokenMiddleware):

    keyword = 'Bearer'
    value_regexp = '.*'

    @database_sync_to_async
    def get_user_instance(self, token_key):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.exceptions import (
            AuthenticationFailed, InvalidToken, TokenError
        )

        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(token_key)
            return auth.get_user(validated_token)
        except (AuthenticationFailed, InvalidToken, TokenError):
            return None
