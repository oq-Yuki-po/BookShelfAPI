class AppRoles:
    """
    Class to define roles in the application.
    Each role can be used to control access to different parts of the application.
    """
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class AppRoutePermissions:
    """
    Class to define permissions for different routes in the application.
    Each route can have multiple roles that are allowed to access it.
    """
    class Users:

        GET_ME = [AppRoles.USER, AppRoles.ADMIN]

    class Books:
        POST_GOOGLE_BOOKS = [AppRoles.ADMIN]

