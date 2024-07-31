# chat/middleware.py

from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

User = get_user_model()

class JwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Get the token
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if token:
            try:
                # This will automatically validate the token and raise an error if token is invalid
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                # Token is invalid
                print(f"Invalid token: {e}")
                return None
            else:
                #  Then token is valid, decode it
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                # Get the user using ID
                user = await self.get_user(decoded_data['user_id'])
                if user is not None:
                    scope['user'] = user
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))