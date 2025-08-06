from django.core.management.base import BaseCommand
from catalog.services import invalidate_all_products_cache


class Command(BaseCommand):
    help = 'Очищает весь кеш продуктов и категорий'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=int,
            help='ID категории для очистки кеша только этой категории',
        )

    def handle(self, *args, **options):
        category_id = options.get('category')
        
        if category_id:
            from catalog.services import invalidate_products_cache
            invalidate_products_cache(category_id)
            self.stdout.write(
                self.style.SUCCESS(f'Кеш для категории {category_id} успешно очищен')
            )
        else:
            invalidate_all_products_cache()
            self.stdout.write(
                self.style.SUCCESS('Весь кеш продуктов и категорий успешно очищен')
            ) 