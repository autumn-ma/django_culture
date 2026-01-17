from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class HTTPSLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url and next_url.startswith("http://"):
            next_url = next_url.replace("http://", "https://", 1)
        if previous_url and previous_url.startswith("http://"):
            previous_url = previous_url.replace("http://", "https://", 1)

        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", next_url),
                    ("previous", previous_url),
                    ("results", data),
                ]
            )
        )
