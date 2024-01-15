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

    class Books:
        TAG: str = "books"
        PREFIX: str = "/books"
        POST_URL: str = "/"
        POST_GOOGLE_BOOKS_URL: str = "/google-books"


class AppRoutePermissions:
    class Users:

        GET_ME = ["admin", "user"]

    class Books:
        POST_GOOGLE_BOOKS = ["admin"]
