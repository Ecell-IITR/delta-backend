from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination, _positive_int
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class CustomLimitOffsetPagination(LimitOffsetPagination):

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)


class AllListsPagination(CustomLimitOffsetPagination):
    default_limit = 10
    max_limit = 100