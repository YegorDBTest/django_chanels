from django.utils.translation import gettext_lazy as _

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework import exceptions as drf_exceptions
from rest_framework.authtoken.models import Token


class DRFAuthTokenMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        scope = dict(scope)

        if not (user := scope.get('user')) or user.is_anonymous:
            scope['user'] = await self._get_user(scope)

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def _get_user(self, scope):
        # postpone model import to avoid ImproperlyConfigured error before Django
        # setup is complete.
        from django.contrib.auth.models import AnonymousUser

        key = self._parse_token_key(scope)

        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise drf_exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            msg = _('User inactive or deleted.')
            raise drf_exceptions.AuthenticationFailed(msg)

        return token.user

    def _parse_token_key(self, scope):
        auth = dict(scope['headers']).get('Authorization', '').split()

        if not auth or auth[0] != 'Token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise drf_exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                'Invalid token header. '
                'Token string should not contain spaces.')
            raise drf_exceptions.AuthenticationFailed(msg)

        return auth[1]
