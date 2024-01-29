from django.core.management.base import BaseCommand
from faker import Faker
from Cars.models import CarType, Car, Dealership

fake = Faker()

CAR_TYPES = [
    {
        "brand": "Audi",
        "models": ["A1", "A2", "A3", "A4", "A5", "A6", "A7"],
        "dealership": "Audi",
    },
    {
        "brand": "BMW",
        "models": [
            "1 Series",
            "2 Series",
            "3 Series",
            "4 Series",
            "5 Series",
            "6 Series",
            "7 Series",
        ],
        "dealership": "BMW",
    },
    {
        "brand": "Mercedes-Benz",
        "models": ["A-Class", "B-Class", "C-Class", "E-Class", "S-Class", "CLA", "CLS"],
        "dealership": "Mercedes-Benz",
    },
]


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database population..."))

        # Очистка існуючих записів
        Car.objects.all().delete()
        CarType.objects.all().delete()
        Dealership.objects.all().delete()

        for car_type_data in CAR_TYPES:
            brand = car_type_data["brand"]
            dealership_name = car_type_data["dealership"]

            # Створення дилершіпу для бренду, якщо його ще не існує
            dealership, _ = Dealership.objects.get_or_create(name=dealership_name)

            for model in car_type_data["models"]:
                car_type = CarType.objects.create(
                    name=model,
                    brand=brand,
                    price=fake.random_int(min=10000, max=30000),
                )

                # Додавання типу автомобіля до доступних для дилершіпу
                dealership.available_car_types.add(car_type)

                for _ in range(5):
                    Car.objects.create(
                        car_type=car_type,
                        color=fake.color_name(),
                        year=fake.random_int(min=2005, max=2023),
                    )

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
