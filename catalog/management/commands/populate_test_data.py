from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Добавляет тестовые категории и продукты в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить все существующие данные перед добавлением новых',
        )
        parser.add_argument(
            '--categories-only',
            action='store_true',
            help='Добавить только категории',
        )
        parser.add_argument(
            '--products-only',
            action='store_true',
            help='Добавить только продукты (требует существующих категорий)',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['clear']:
                self.stdout.write('Очистка существующих данных...')
                Product.objects.all().delete()
                Category.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS('Все данные успешно удалены')
                )

            if not options['products_only']:
                self.create_categories()

            if not options['categories_only']:
                self.create_products()

            self.stdout.write(
                self.style.SUCCESS('Тестовые данные успешно добавлены!')
            )

    def create_categories(self):
        """Создание тестовых категорий"""
        self.stdout.write('Создание категорий...')
        
        categories_data = [
            {
                'name': 'Электроника',
                'description': 'Товары электронной техники и гаджеты'
            },
            {
                'name': 'Одежда',
                'description': 'Мужская и женская одежда, обувь, аксессуары'
            },
            {
                'name': 'Книги',
                'description': 'Художественная и техническая литература'
            },
            {
                'name': 'Спорт',
                'description': 'Спортивные товары, инвентарь и экипировка'
            },
            {
                'name': 'Дом и сад',
                'description': 'Товары для дома, сада и ремонта'
            },
            {
                'name': 'Красота и здоровье',
                'description': 'Косметика, парфюмерия, товары для здоровья'
            },
            {
                'name': 'Автотовары',
                'description': 'Автозапчасти, аксессуары и товары для автомобилей'
            },
            {
                'name': 'Игрушки и хобби',
                'description': 'Детские игрушки, настольные игры, товары для хобби'
            },
            {
                'name': 'Продукты питания',
                'description': 'Продукты питания, напитки, консервы'
            },
            {
                'name': 'Мебель',
                'description': 'Мебель для дома и офиса'
            }
        ]

        created_categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'  ✅ Создана категория: {category.name}')
            else:
                self.stdout.write(f'  ℹ️  Категория уже существует: {category.name}')
            created_categories.append(category)

        self.stdout.write(
            self.style.SUCCESS(f'Создано категорий: {len(created_categories)}')
        )
        return created_categories

    def create_products(self):
        """Создание тестовых продуктов"""
        self.stdout.write('Создание продуктов...')
        
        products_data = [
            # Электроника
            {
                'name': 'Смартфон iPhone 15 Pro',
                'description': 'Новейший смартфон Apple с титановым корпусом и камерой 48 МП',
                'category_name': 'Электроника',
                'price': Decimal('99999.99')
            },
            {
                'name': 'Ноутбук Dell XPS 13',
                'description': 'Ультратонкий ноутбук с дисплеем InfinityEdge и процессором Intel Core i7',
                'category_name': 'Электроника',
                'price': Decimal('129999.99')
            },
            {
                'name': 'Беспроводные наушники Sony WH-1000XM5',
                'description': 'Шумоподавляющие наушники с превосходным качеством звука',
                'category_name': 'Электроника',
                'price': Decimal('29999.99')
            },
            {
                'name': 'Планшет iPad Pro 12.9',
                'description': 'Мощный планшет для профессионалов с дисплеем Liquid Retina XDR',
                'category_name': 'Электроника',
                'price': Decimal('89999.99')
            },
            
            # Одежда
            {
                'name': 'Футболка мужская хлопковая',
                'description': 'Комфортная хлопковая футболка для повседневной носки',
                'category_name': 'Одежда',
                'price': Decimal('1999.99')
            },
            {
                'name': 'Джинсы женские Levi\'s 501',
                'description': 'Классические джинсы прямого кроя из качественного денима',
                'category_name': 'Одежда',
                'price': Decimal('5999.99')
            },
            {
                'name': 'Кроссовки Nike Air Max',
                'description': 'Спортивные кроссовки с технологией Air Max для максимального комфорта',
                'category_name': 'Одежда',
                'price': Decimal('8999.99')
            },
            {
                'name': 'Куртка зимняя Columbia',
                'description': 'Теплая зимняя куртка с технологией Omni-Heat',
                'category_name': 'Одежда',
                'price': Decimal('15999.99')
            },
            
            # Книги
            {
                'name': 'Книга "Война и мир" Л.Н. Толстой',
                'description': 'Великий роман-эпопея о русском обществе в эпоху наполеоновских войн',
                'category_name': 'Книги',
                'price': Decimal('899.99')
            },
            {
                'name': 'Книга "Мастер и Маргарита" М.А. Булгаков',
                'description': 'Философский роман о добре и зле, любви и предательстве',
                'category_name': 'Книги',
                'price': Decimal('799.99')
            },
            {
                'name': 'Книга "Преступление и наказание" Ф.М. Достоевский',
                'description': 'Психологический роман о преступлении и его последствиях',
                'category_name': 'Книги',
                'price': Decimal('699.99')
            },
            
            # Спорт
            {
                'name': 'Футбольный мяч Adidas Champions League',
                'description': 'Официальный мяч Лиги Чемпионов для профессиональной игры',
                'category_name': 'Спорт',
                'price': Decimal('3999.99')
            },
            {
                'name': 'Велосипед горный Trek Marlin 7',
                'description': 'Горный велосипед для активного отдыха и спорта',
                'category_name': 'Спорт',
                'price': Decimal('45999.99')
            },
            {
                'name': 'Беговая дорожка NordicTrack',
                'description': 'Электрическая беговая дорожка для домашних тренировок',
                'category_name': 'Спорт',
                'price': Decimal('89999.99')
            },
            
            # Дом и сад
            {
                'name': 'Горшок для цветов керамический',
                'description': 'Красивый керамический горшок для комнатных растений',
                'category_name': 'Дом и сад',
                'price': Decimal('599.99')
            },
            {
                'name': 'Набор инструментов Bosch',
                'description': 'Профессиональный набор инструментов для ремонта и строительства',
                'category_name': 'Дом и сад',
                'price': Decimal('15999.99')
            },
            {
                'name': 'Газонокосилка электрическая',
                'description': 'Электрическая газонокосилка для ухода за газоном',
                'category_name': 'Дом и сад',
                'price': Decimal('12999.99')
            },
            
            # Красота и здоровье
            {
                'name': 'Крем для лица La Roche-Posay',
                'description': 'Увлажняющий крем для чувствительной кожи',
                'category_name': 'Красота и здоровье',
                'price': Decimal('1299.99')
            },
            {
                'name': 'Витамины Centrum',
                'description': 'Комплекс витаминов и минералов для поддержания здоровья',
                'category_name': 'Красота и здоровье',
                'price': Decimal('899.99')
            },
            {
                'name': 'Электрическая зубная щетка Oral-B',
                'description': 'Электрическая зубная щетка с технологией 3D очистки',
                'category_name': 'Красота и здоровье',
                'price': Decimal('3999.99')
            },
            
            # Автотовары
            {
                'name': 'Автомобильное масло Mobil 1',
                'description': 'Синтетическое моторное масло для современных двигателей',
                'category_name': 'Автотовары',
                'price': Decimal('2499.99')
            },
            {
                'name': 'Автомобильный коврик',
                'description': 'Резиновый коврик для салона автомобиля',
                'category_name': 'Автотовары',
                'price': Decimal('799.99')
            },
            {
                'name': 'Автомобильный компрессор',
                'description': 'Портативный компрессор для подкачки шин',
                'category_name': 'Автотовары',
                'price': Decimal('1999.99')
            },
            
            # Игрушки и хобби
            {
                'name': 'Настольная игра "Монополия"',
                'description': 'Классическая экономическая настольная игра',
                'category_name': 'Игрушки и хобби',
                'price': Decimal('1999.99')
            },
            {
                'name': 'Конструктор LEGO Technic',
                'description': 'Сложный конструктор для детей и взрослых',
                'category_name': 'Игрушки и хобби',
                'price': Decimal('5999.99')
            },
            {
                'name': 'Модель самолета для сборки',
                'description': 'Детализированная модель самолета для сборки',
                'category_name': 'Игрушки и хобби',
                'price': Decimal('1499.99')
            },
            
            # Продукты питания
            {
                'name': 'Кофе в зернах Lavazza',
                'description': 'Итальянский кофе в зернах премиум качества',
                'category_name': 'Продукты питания',
                'price': Decimal('899.99')
            },
            {
                'name': 'Чай зеленый листовой',
                'description': 'Натуральный зеленый чай высшего сорта',
                'category_name': 'Продукты питания',
                'price': Decimal('399.99')
            },
            {
                'name': 'Мед натуральный липовый',
                'description': 'Натуральный мед с пасеки, 1 кг',
                'category_name': 'Продукты питания',
                'price': Decimal('599.99')
            },
            
            # Мебель
            {
                'name': 'Диван угловой',
                'description': 'Комфортный угловой диван для гостиной',
                'category_name': 'Мебель',
                'price': Decimal('45999.99')
            },
            {
                'name': 'Стол обеденный деревянный',
                'description': 'Классический обеденный стол из массива дерева',
                'category_name': 'Мебель',
                'price': Decimal('25999.99')
            },
            {
                'name': 'Кровать двуспальная',
                'description': 'Двуспальная кровать с мягким изголовьем',
                'category_name': 'Мебель',
                'price': Decimal('35999.99')
            }
        ]

        created_products = []
        for prod_data in products_data:
            try:
                category = Category.objects.get(name=prod_data['category_name'])
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'description': prod_data['description'],
                        'category': category,
                        'price': prod_data['price']
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Создан продукт: {product.name} - {product.price} руб.')
                else:
                    self.stdout.write(f'  ℹ️  Продукт уже существует: {product.name}')
                created_products.append(product)
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️  Категория "{prod_data["category_name"]}" не найдена для продукта "{prod_data["name"]}"')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Создано продуктов: {len(created_products)}')
        )
        return created_products 