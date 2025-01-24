from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'size'  # 指定分页大小参数名
    page_size = 4  # 每页显示4个
    max_page_size = 8  # 对page_size进行限制
