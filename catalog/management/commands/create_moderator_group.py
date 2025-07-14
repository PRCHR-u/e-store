from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с нужными правами.'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        can_unpublish = Permission.objects.get(codename='can_unpublish_product')
        can_delete = Permission.objects.get(codename='delete_product')
        group.permissions.set([can_unpublish, can_delete])
        group.save()
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены.')) 