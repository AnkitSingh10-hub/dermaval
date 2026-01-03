import html
from decimal import ROUND_HALF_EVEN, Decimal
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    IntegerField,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer


from users.models import (
   
    User
)
from core.utils import (
    
    get_camelized_json,
    get_pclaim,
)

class EmptySerializer(serializers.Serializer):
    """
    Empty Seralizer that does not take or return any value
    """

    pass


class AuthUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="userinfo.firstName", read_only=True)
    last_name = serializers.CharField(source="userinfo.lastName", read_only=True)
    company_name = serializers.CharField(source="userinfo.company_name", read_only=True)
    state = serializers.CharField(source="userinfo.company_state", read_only=True)
    district = serializers.CharField(source="userinfo.company_district", read_only=True)
    municipality = serializers.CharField(
        source="userinfo.company_municipality", read_only=True
    )
    wardNo = serializers.CharField(source="userinfo.wardNo", read_only=True)
    tole = serializers.CharField(source="userinfo.tole", read_only=True)
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "company_name",
            "state",
            "district",
            "municipality",
            "wardNo",
            "tole",
            "groups",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_groups(self, obj) -> list:
        return [group.name for group in obj.groups.all()]


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer class that will add username to the token payload
    This can then be decoded by client to use the available data
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fcm_token"] = serializers.CharField(required=False)
        self.fields["fcm_type"] = serializers.CharField(required=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["pclaim"] = get_pclaim(user)
        token["userDetail"] = get_camelized_json(AuthUserSerializer(user).data)
        return token

    def validate(self, attrs):
        password = None
        if "password" in attrs:
            password = attrs["password"]
        data = dict()

        data = super().validate(attrs)
        data["user_detail"] = AuthUserSerializer(self.user).data

        return data
