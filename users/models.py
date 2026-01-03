from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from core.models import SoftDeleteModal, TimeStampedModel

import random
from core.models import Province, District, Municipality


class User(AbstractUser, SoftDeleteModal):
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(
        _("email address"), validators=[MinLengthValidator(3)], blank=True, null=True
    )
    mobile_number = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^([\s\d]+)$", message="Phone number must contain only number."
            )
        ],
    )
    avatar = models.ImageField(
        "Image",
        upload_to="avatar",
        null=True,
        blank=True,
    )
    is_phone_verified = models.BooleanField(null=True, blank=True)
    is_email_verified = models.BooleanField(null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
    ward = models.CharField(max_length=100, null=True, blank=True)
    
    address = models.CharField(max_length=200, null=True, blank=True)

    def soft_delete(self, *args, **kwargs):
        """
        Soft delete the model instance.
        """
        if not self.is_deleted:
            self.is_deleted = True
            self.is_active = False
            self.username = self.username + "-deleted" + str(self.id)
            self.deleted_date = timezone.now()

            return super().save(*args, **kwargs)

    def get_date_joined_date_only(self):
        return self.date_joined.date() if self.date_joined else None

    def get_roles_name(self):
        return ",".join([x.name for x in self.groups.all()])

    