from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает фикстуры с возможностью очистки базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить все существующие данные перед загрузкой фикстур',
        )
        parser.add_argument(
            '--fixture',
            type=str,
            default='initial_data',
            help='Название фикстуры для загрузки (по умолчанию: initial_data)',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='Показать список доступных фикстур',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_fixtures()
            return

        with transaction.atomic():
            if options['clear']:
                self.clear_database()

            self.load_fixture(options['fixture'])

    def clear_database(self):
        """Очистка базы данных"""
        self.stdout.write('Очистка базы данных...')
        
        # Подсчет существующих данных
        products_count = Product.objects.count()
        categories_count = Category.objects.count()
        
        # Удаление данных
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Удалено {products_count} продуктов и {categories_count} категорий'
            )
        )

    def load_fixture(self, fixture_name):
        """Загрузка фикстуры"""
        self.stdout.write(f'Загрузка фикстуры: {fixture_name}')
        
        try:
            call_command('loaddata', fixture_name, verbosity=0)
            self.stdout.write(
                self.style.SUCCESS(f'Фикстура {fixture_name} успешно загружена')
            )
            
            # Показываем статистику
            self.show_statistics()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке фикстуры: {e}')
            )

    def list_fixtures(self):
        """Показать список доступных фикстур"""
        self.stdout.write('Доступные фикстуры:')
        self.stdout.write('  - initial_data (категории + продукты)')
        self.stdout.write('  - categories (только категории)')
        self.stdout.write('  - products (только продукты)')
        self.stdout.write('')
        self.stdout.write('Использование:')
        self.stdout.write('  python manage.py load_fixtures --fixture initial_data')
        self.stdout.write('  python manage.py load_fixtures --clear --fixture categories')

    def show_statistics(self):
        """Показать статистику загруженных данных"""
        categories_count = Category.objects.count()
        products_count = Product.objects.count()
        
        self.stdout.write('')
        self.stdout.write('Статистика:')
        self.stdout.write(f'  Категорий: {categories_count}')
        self.stdout.write(f'  Продуктов: {products_count}')
        
        if categories_count > 0:
            self.stdout.write('')
            self.stdout.write('Категории:')
            for category in Category.objects.all():
                products_in_category = category.products.count()
                self.stdout.write(f'  - {category.name} ({products_in_category} продуктов)') 