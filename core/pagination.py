from rest_framework.pagination import CursorPagination, PageNumberPagination

__all__ = [
    "PagePaginator",
    "CursorPaginator",
]


class PagePaginator(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "size"
    page_query_param = "page"


class CursorPaginator(CursorPagination):
    page_size = 10
    cursor_query_param = "cursor"
    ordering = "-id"
