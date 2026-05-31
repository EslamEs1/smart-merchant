from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    """Authenticate using email (as entered in the preserved login form) or username.

    When the credential contains '@', an email lookup is attempted first (case-insensitive).
    If the email lookup finds a user but the password is wrong, a username lookup is still
    attempted — a username that happens to contain '@' should not be silently locked out.
    Only when no matching user is found at all does the timing-safe dummy hash run.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD) or kwargs.get("email")
        if username is None or password is None:
            return None

        candidates: list = []

        if "@" in username:
            try:
                candidates.append(UserModel.objects.get(email__iexact=username))
            except UserModel.DoesNotExist:
                pass

        try:
            by_username = UserModel.objects.get(username=username)
            # Avoid duplicate if email lookup already found this same user.
            if not candidates or candidates[0].pk != by_username.pk:
                candidates.append(by_username)
        except UserModel.DoesNotExist:
            pass

        for user in candidates:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        # Timing-safe dummy: run the hasher when no candidate matched so the
        # response time is similar to a hit-with-wrong-password.
        UserModel().set_password(password)
        return None
