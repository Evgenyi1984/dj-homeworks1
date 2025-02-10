import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Укажите путь к файлу CSV (по умолчанию: phones.csv)",
            default="phones.csv",
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        with open(file_path, "r", encoding="utf-8") as file:
            phones = list(csv.DictReader(file, delimiter=";"))

        for phone in phones:
            Phone.objects.get_or_create(
                id=int(phone["id"]),
                defaults={
                    "name": phone["name"],
                    "image": phone["image"],
                    "price": int(phone["price"]),
                    "release_date": phone["release_date"],
                    "lte_exists": phone["lte_exists"].lower() == "true",
                    "slug": slugify(phone["name"]),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported phones from {file_path}")
        )
