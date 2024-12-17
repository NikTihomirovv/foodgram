import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Класс для импорта фикстур."""

    def handle(self, *args, **options):
        self.load_fixture()
        print('Загрузка завершена!')

    def load_fixture(self, file='ingredients.csv'):
        file_path = f'./data/{file}'
        with open(file_path, newline='', encoding='utf-8') as i:
            reader = csv.reader(i)

            for row in reader:
                status, created = Ingredient.objects.update_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
