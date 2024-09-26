from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

class CustomLimitOffsetPagtination(LimitOffsetPagination):
    default_limit = 10


class CustomPagePagination(PageNumberPagination):
    page_size = 2

    def get_next_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()
    
    def get_previous_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        return Response({
            'previous': self.get_previous_number(),
            'next': self.get_next_number(),
            'count': self.page.paginator.count,
            'results': data
        })
    

