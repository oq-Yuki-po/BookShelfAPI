from fastapi.security import OAuth2PasswordBearer


class AppRoutes:

    class Users:
        TAG: str = "users"
        PREFIX: str = "/users"
        POST_URL: str = "/"
        POST_TOKEN_URL: str = "/token"
        GET_ME_URL: str = "/me"

    class Login:
        TAG: str = "login"
        PREFIX: str = "/login"
        POST_TOKEN_URL: str = "/token"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=AppRoutes.Login.PREFIX + AppRoutes.Login.POST_TOKEN_URL)
