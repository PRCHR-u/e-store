from catalog.models import Category, Product

def get_all_categories():
    """Получить все категории"""
    categories = Category.objects.all()
    print("\nВсе категории:")
    for category in categories:
        print(f"- {category.name}")
    return categories

def get_all_products():
    """Получить все продукты"""
    products = Product.objects.all()
    print("\nВсе продукты:")
    for product in products:
        print(f"- {product.name} (Цена: {product.price})")
    return products

def get_products_by_category(category_name):
    """Найти все продукты в определенной категории"""
    try:
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        print(f"\nПродукты в категории '{category_name}':")
        for product in products:
            print(f"- {product.name} (Цена: {product.price})")
        return products
    except Category.DoesNotExist:
        print(f"Категория '{category_name}' не найдена")
        return None

def update_product_price(product_name, new_price):
    """Обновить цену определенного продукта"""
    try:
        product = Product.objects.get(name=product_name)
        old_price = product.price
        product.price = new_price
        product.save()
        print(f"\nЦена продукта '{product_name}' обновлена:")
        print(f"Старая цена: {old_price}")
        print(f"Новая цена: {new_price}")
        return product
    except Product.DoesNotExist:
        print(f"Продукт '{product_name}' не найден")
        return None

def delete_product(product_name):
    """Удалить продукт"""
    try:
        product = Product.objects.get(name=product_name)
        product.delete()
        print(f"\nПродукт '{product_name}' успешно удален")
        return True
    except Product.DoesNotExist:
        print(f"Продукт '{product_name}' не найден")
        return False

if __name__ == "__main__":
    # Примеры использования:
    
    # Получить все категории
    categories = get_all_categories()
    
    # Получить все продукты
    products = get_all_products()
    
    # Найти продукты в категории
    category_products = get_products_by_category("Электроника")
    
    # Обновить цену продукта
    updated_product = update_product_price("Смартфон", 999.99)
    
    # Удалить продукт
    deleted = delete_product("Старый продукт") 