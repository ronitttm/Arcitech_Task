# auth.py
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class QueryParameterTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            return None

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)
