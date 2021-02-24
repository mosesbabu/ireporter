import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'
    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless whether
        the endpoint requires authentication or not
        `authenticate` has to possible return values:
        1) `None` - We return None if we do not wish to authenticate. Usually, this
                    means we know that authentication will fail. Eg. when a user does
                    not include a token in the headers
        2) `{user, token}` - We return user/token combination when authentication is successful
            If neither of the conditions are met, we do not return anything
            We simply raise the `AuthenticationFailed` exception and let DRF
            handle the rest
        """
        request.user = None
        # collect authentication header and split it into an array
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header:
            return None
        # auth_header should have at least two elements
        if len(auth_header) == 1:
            return None
        # auth_header should have at most 2 elements
        elif len(auth_header) > 2:
            return None
        # decode the prefix and token from bytes to `utf-8`
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        # compare authorization header prefix with the set prefix
        if prefix.lower() != auth_header_prefix:
            return None
        # By now, there is a chance that authentication could be successful
        # We therefore pass the request and token to another method that handles
        # authentication
        return self._authenticate_credentials(request, token)
        
    def _authenticate_credentials(self, request, token):
        """
        Try authenticate the credentials and return `user` and `token` if
        successful
        """
        # decode the provided token using jwt
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = "Authentication failed, Could not decode token"
            raise exceptions.AuthenticationFailed(msg)
        # search if user matching token exists
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = "No user matching this token was found"
            raise exceptions.AuthenticationFailed(msg)
        # raise an exception if user is deactivated
        return (user, token)