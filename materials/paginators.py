from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    # Установим размер страницы
    page_size = 10
    # Разрешим пользователям изменять это значение через параметры запроса
    page_size_query_param = 'page_size'
    # Максимальное количество элементов на странице
    max_page_size = 100
