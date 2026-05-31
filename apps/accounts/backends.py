from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    """Authenticate using email (as entered in the preserved login form) or username.

    When the credential contains '@', an email lookup is attempted first (case-insensitive).
    If that lookup finds nothing (e.g. a username that happens to contain '@'), the backend
    falls through to a username lookup. This removes the hard '@'-heuristic routing and
    means a user is never silently locked out due to an ambiguous credential string.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get("email")
        if username is None or password is None:
            return None

        user = None
        if "@" in username:
            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                pass

        if user is None:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # Timing-safe: run the hasher so the response time matches a successful lookup.
                UserModel().set_password(password)
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
