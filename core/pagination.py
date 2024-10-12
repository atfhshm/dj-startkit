from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response

__all__ = [
    "PagePaginator",
    "CursorPaginator",
]


class PagePaginator(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "page_size"
    page_query_param = "page_number"

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": len(data),
                "page_number": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "required": ["count", "page_size", "page_number", "total_pages", "results"],
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "page_size": {
                    "type": "integer",
                    "example": self.page_size,
                },
                "page_number": {
                    "type": "integer",
                    "example": 1,
                },
                "total_pages": {
                    "type": "integer",
                    "example": 5,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=4".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=2".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "results": schema,
            },
        }


class CursorPaginator(CursorPagination):
    page_size = 10
    cursor_query_param = "cursor"
    ordering = "-id"
