from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        MERCHANT = "MERCHANT", _("تاجر")
        AFFILIATE = "AFFILIATE", _("مسوّق بالعمولة")
        ADMIN = "ADMIN", _("مدير")

    role = models.CharField(
        verbose_name=_("الدور"),
        max_length=16,
        choices=Role.choices,
        default=Role.MERCHANT,
    )
    email = models.EmailField(unique=True)

    class Meta(AbstractUser.Meta):
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمون")

    def __str__(self) -> str:
        return self.email or self.username

    @property
    def is_merchant(self) -> bool:
        return self.role == self.Role.MERCHANT and not self.is_admin

    @property
    def is_affiliate(self) -> bool:
        return self.role == self.Role.AFFILIATE and not self.is_admin

    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN or self.is_staff or self.is_superuser
