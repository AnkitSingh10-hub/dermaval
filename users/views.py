import logging
import jwt
import pandas as pd
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

from django.db.models.functions import Coalesce, Lower
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from drf_spectacular.utils import extend_schema, inline_serializer
from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side
from requests.exceptions import HTTPError, RequestException
from rest_framework import filters, generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.utils import aware_utcnow, datetime_from_epoch
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from core.utils import (
    CustomPageNumberPagination,
    get_pclaim,
)
from users.serializers import *


logger = logging.getLogger(__name__)




def refresh_cookie(response):
    args = ["refresh", response.data["refresh"]]
    kwargs = {"httponly": True}
    response.set_cookie(*args, **kwargs)
    return response


class TokenObtainPairViewSet(viewsets.GenericViewSet, TokenObtainPairView):
    """
    Custom TokenObtainPairViewSet class that will send refresh token as an http only cookie.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = TokenObtainPairSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["request"] = self.request
        return context

    @extend_schema(
        responses={
            200: inline_serializer(
                name="TokenObtainPairResponseSerializer",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                },
            )
        }
    )
    def create(self, request, *args, **kwargs):
        """
        API that will return access and refresh token. It will also return refresh token as an http only cookie.
        """
        response = super().post(request=request, *args, **kwargs)
        response = refresh_cookie(response)

        return response


class ClearTokenViewSet(viewsets.GenericViewSet):
    """
    Create ViewSet to clear refresh token in client.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = EmptySerializer

    def create(self, request, *args, **kwargs):
        """
        API that will clear the http only refresh token for client.
        """
        OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()
        if "refresh" in request.COOKIES:
            refresh = request.COOKIES["refresh"]
            jwt_decoded = jwt.decode(refresh, settings.SECRET_KEY, "HS256")
            if (
                "jti" in jwt_decoded
                and "exp" in jwt_decoded
                and "username" in jwt_decoded
            ):
                jti = jwt_decoded["jti"]
                exp = jwt_decoded["exp"]
                username = jwt_decoded["username"]
                token = OutstandingToken.objects.filter(
                    jti=jti,
                    user__username=username,
                    expires_at=datetime_from_epoch(exp),
                )
                token.delete()

        response = Response("Successfully Logged Out")
        response.delete_cookie("refresh")
        return response


class TokenRefreshViewSet(viewsets.GenericViewSet, TokenRefreshView):
    """
    Custom TokenRefreshViewSet class that takes refresh token from cookies when refresh is not present in post data.
    It also returns refresh token if ROTATE_REFRESH_TOKENS is true and it gets 'refresh' in response's data.
    """

    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @extend_schema(
        # tags=['Token'],
        responses=inline_serializer(
            name="TokenRefreshResponseSerializer",
            fields={
                "access": serializers.CharField(),
            },
        )
    )
    def create(self, request, *args, **kwargs):
        """
        API that refreshes access token. This API will try to take refresh token from cookies when refresh is not present in post data.
        """
        key_name = "pclaim"
        if not "refresh" in request.data.keys():
            if "refresh" in request.COOKIES.keys():
                request.data["refresh"] = request.COOKIES["refresh"]
            else:
                response = Response(
                    {"message": "NoError", "error": "No Refresh Token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
                response.delete_cookie("refresh")
                return response
        response = super().post(request=request, *args, **kwargs)
        try:
            if response.status_code == 200 and "access" in response.data:
                # Getting user detail by decoding access token
                jwt_decoded = jwt.decode(
                    response.data["access"], settings.SECRET_KEY, "HS256"
                )
                if "user_id" in jwt_decoded:
                    if key_name in jwt_decoded:
                        user = get_user_model().objects.get(id=jwt_decoded["user_id"])
                        pclaim = get_pclaim(user)
                        if jwt_decoded[key_name] != pclaim:
                            raise InvalidToken
                if "refresh" in response.data.keys():
                    response = refresh_cookie(response)
                    # Uncomment the line below if you don't want to send refresh token as response data
                    # response.data.pop('refresh')
        except Exception as e:
            if isinstance(e, InvalidToken):
                raise e

            response = Response({"message": e}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie("refresh")

        return response

