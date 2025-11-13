from .services import get_all_categories_with_products


def categories_processor(request):
    """
    Контекстный процессор для добавления категорий в глобальный контекст
    """
    return {
        'categories': get_all_categories_with_products()
    } 