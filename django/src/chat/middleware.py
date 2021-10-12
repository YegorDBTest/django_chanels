from django.utils.translation import gettext_lazy as _

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework.authtoken.models import Token


class DRFAuthTokenMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        scope = dict(scope)

        if not (user := scope.get('user')) or user.is_anonymous:
            scope['user'] = await self._get_user(scope)

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def _get_user(self, scope):
        key = self._parse_token_key(scope)

        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            return None

        if not token.user.is_active:
            return None

        return token.user

    def _parse_token_key(self, scope):
        auth = dict(scope['headers']).get(b'authorization', b'').decode().split()

        if not auth or auth[0] != 'Token' or len(auth) != 2:
            return None

        return auth[1]
