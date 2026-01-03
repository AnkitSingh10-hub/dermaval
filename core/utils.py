import datetime
import json
from collections import OrderedDict
from typing import List

import nepali_datetime
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext as _
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import numpy as np


def convert_normal_nepali_date_to_normal_eng_date(normal_nep_date):
    normal_eng_date = None
    if normal_nep_date:
        # Example date string in "YYYY-MM-DD" format
        date_str = str(
            normal_nep_date
        )  # This can be replaced with a variable or user input

        # Parse the date string into a nepali datetime.date object
        year, month, day = map(int, date_str.split("-"))
        nepali_date = nepali_datetime.date(year, month, day)
        # print("nep date month calendar is:::", nepali_date.calendar())
        # Nepali datetime object to normal date object
        normal_eng_date = nepali_date.to_datetime_date()
    return normal_eng_date


def convert_normal_eng_date_to_normal_nepali_date(normal_eng_date):
    normal_nep_date = None
    if normal_eng_date:
        # Example date string in "YYYY-MM-DD" format
        date_str = str(
            normal_eng_date
        )  # This can be replaced with a variable or user input

        # Parse the nepali date string into a datetime.date object
        year, month, day = map(int, date_str.split("-"))
        eng_date = datetime.date(year, month, day)
        # Normal datetime  object to  Nepali datetime object
        normal_nep_date = nepali_datetime.date.from_datetime_date(eng_date)
    return normal_nep_date


class MaxFileSizeValidator(BaseValidator):
    """
    Max file size validator.
    """

    message = _("The file exceed the maximum size of %(limit_value)s MB.")
    code = "file_max_size"

    def __call__(self, value):
        # Get the file size as cleaned value
        cleaned = self.clean(value.size)
        params = {
            "limit_value": self.limit_value,
            "show_value": cleaned,
            "value": value,
        }
        if self.compare(cleaned, self.limit_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def compare(self, file_size, limit_size):
        """
        Compare file size to limit size.
        :param file_size: In bytes.
        :param limit_size: In Megabytes (MB)
        """
        limit_size_in_bytes = (
            limit_size * 1024 * 1024
        )  # Convert limit_size from MB to Bytes
        return file_size > limit_size_in_bytes


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view):
        actual_page_size = request.query_params.get(self.page_size_query_param, None)
        if actual_page_size and (str(actual_page_size) in ["0", "none"]):
            queryset_count = queryset.count()
            if queryset_count > 0:
                self.page_size = queryset_count
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        actual_page_size = self.request.query_params.get(
            self.page_size_query_param, None
        )
        if actual_page_size and str(actual_page_size).lower() == "none":
            return Response(data)
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("currentPage", self.page.number),
                    (
                        "nextPage",
                        self.page.next_page_number() if self.page.has_next() else None,
                    ),
                    ("pageSize", self.get_page_size(self.request)),
                    ("totalPages", self.page.paginator.num_pages),
                    ("totalObjects", self.page.paginator.count),
                    ("results", data),
                ]
            )
        )


def convert_to_nepali_numbers(number):
    nepali_digits = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]

    # Handle if the number is a float or integer
    str_number = str(number)

    if "." in str_number:
        integer_part, decimal_part = str_number.split(".")
        nepali_integer_part = "".join(
            nepali_digits[int(digit)] for digit in integer_part
        )
        nepali_decimal_part = "".join(
            nepali_digits[int(digit)] for digit in decimal_part
        )
        return nepali_integer_part + "." + nepali_decimal_part
    else:
        return "".join(nepali_digits[int(digit)] for digit in str_number)


def get_camelized_json(data):
    """Utility function that returns CamelizedJSON of snake_cased_json

    Args:
        data (json): Snaked Case data

    Returns:
        json: Camelized data
    """
    camalized_data = json.loads(CamelCaseJSONRenderer().render(data).decode())
    return camalized_data


def get_pclaim(user):
    try:
        claim = user.password[-10:]
        bclaim = claim.encode("utf-8")
        pclaim = str(int.from_bytes(bclaim, "big"))
        return pclaim
    except Exception as e:
        print(e)
        return None



