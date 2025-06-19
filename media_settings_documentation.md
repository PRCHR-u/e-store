# Настройки медиа файлов в Django

## Обзор

В проекте корректно настроены параметры для работы с медиа файлами (изображения, документы и т.д.).

## Настройки в settings.py

### MEDIA_URL и MEDIA_ROOT
```python
# Media files (Uploaded files)
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = BASE_DIR / 'media'
```

### Параметры:
- **MEDIA_URL** = '/media/' - URL для доступа к медиа файлам
- **MEDIA_ROOT** = BASE_DIR / 'media' - физический путь к папке медиа файлов

## Настройки в urls.py

### URL маршруты для медиа файлов
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
]

# Добавляем маршруты для медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Важные моменты:
- Маршруты добавляются только в режиме DEBUG
- Используется функция `static()` из Django
- `document_root` указывает на MEDIA_ROOT

## Структура папок

```
e-store/
├── media/                    # Папка для медиа файлов
│   └── products/            # Подпапка для изображений товаров
├── online_store/
│   ├── settings.py          # Настройки MEDIA_URL и MEDIA_ROOT
│   └── urls.py              # URL маршруты для медиа
└── catalog/
    └── models.py            # Модель Product с ImageField
```

## Модель Product

### Поле для изображений
```python
image = models.ImageField(
    upload_to='products/', 
    blank=True, 
    null=True, 
    verbose_name='Изображение'
)
```

### Параметры ImageField:
- **upload_to='products/'** - файлы сохраняются в media/products/
- **blank=True** - поле необязательное в формах
- **null=True** - поле может быть пустым в базе данных

## Переменные окружения

### В файле .env
```
MEDIA_URL=/media/
```

### В файле .env.example
```
MEDIA_URL=/media/
```

## Как это работает

### 1. Загрузка файла
```python
# При создании товара с изображением
product = Product.objects.create(
    name='iPhone 15',
    image=uploaded_file,  # Файл загружается в media/products/
    price=999.99
)
```

### 2. Доступ к файлу
```python
# В шаблонах
<img src="{{ product.image.url }}" alt="{{ product.name }}">

# В коде
image_url = product.image.url  # /media/products/iphone15.jpg
```

### 3. URL маршрутизация
- Запрос: `http://localhost:8000/media/products/iphone15.jpg`
- Django находит файл в `media/products/iphone15.jpg`
- Возвращает файл клиенту

## Проверка настроек

### 1. Создание тестового файла
```python
from django.core.files.uploadedfile import SimpleUploadedFile

# Создание тестового изображения
image = SimpleUploadedFile(
    "test.jpg",
    b"file_content",
    content_type="image/jpeg"
)

# Создание товара с изображением
product = Product.objects.create(
    name='Тестовый товар',
    image=image,
    price=100.00
)
```

### 2. Проверка URL
```python
# Проверка URL изображения
print(product.image.url)  # /media/products/test.jpg

# Проверка физического пути
print(product.image.path)  # /path/to/media/products/test.jpg
```

## Безопасность

### В продакшене
- Не используйте `static()` для медиа файлов
- Настройте веб-сервер (nginx, Apache) для раздачи медиа файлов
- Используйте CDN для больших файлов

### В разработке
- DEBUG=True включает раздачу медиа файлов через Django
- Файлы доступны по URL /media/

## Примеры использования

### В шаблонах
```html
{% if product.image %}
    <img src="{{ product.image.url }}" alt="{{ product.name }}" class="product-image">
{% else %}
    <img src="/static/images/no-image.png" alt="Нет изображения" class="product-image">
{% endif %}
```

### В формах
```python
# forms.py
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

# views.py
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})
```

### В шаблонах форм
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Сохранить</button>
</form>
```

## Проверка работоспособности

1. Убедитесь, что папка `media/` существует
2. Проверьте, что DEBUG=True в настройках
3. Загрузите тестовое изображение через админ-панель
4. Проверьте доступность файла по URL /media/products/filename.jpg 