import re

from django.apps import apps
from django.utils.functional import empty

from channels.db import database_sync_to_async
from channels.auth import AuthMiddleware, UserLazyObject


class DRFAuthTokenMiddleware(AuthMiddleware):

    keyword = 'Token'
    value_regexp = '[0-9a-f]{40}'

    async def resolve_scope(self, scope):
        if scope["user"]._wrapped is empty or scope["user"].is_anonymous:
            scope["user"]._wrapped = await self._get_user(scope)

    @database_sync_to_async
    def _get_user(self, scope):
        from django.contrib.auth.models import AnonymousUser
        Token = apps.get_model('authtoken', 'Token')

        key = self._parse_token_key(scope)
        if not key:
            return AnonymousUser()

        try:
            token = Token.objects.select_related('user').get(key=key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()

    def _parse_token_key(self, scope):
        headers = dict(scope['headers'])
        key = headers.get(b'authorization', b'').decode()
        matched = re.fullmatch(rf'{self.keyword} ({self.value_regexp})', key)

        if not matched:
            return
        return matched.group(1)
