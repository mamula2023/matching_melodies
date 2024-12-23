from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
def user_authenticated(request):
    is_jwt_authenticated = False
    jwt_authenticator = JWTAuthentication()
    
    try:
        # Attempt to authenticate using JWT
        result = jwt_authenticator.authenticate(request)
        if result:
            user, token_payload = result
            is_jwt_authenticated = True
    except AuthenticationFailed:
        pass  # Token is invalid or missing

    return {'is_jwt_authenticated': is_jwt_authenticated}
