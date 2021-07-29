from rest_framework import pagination

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param='count' #param to set how many items per page
    max_page_size=5
    page_query_param = 'p' #param to set which page to retrieve