import sys
import django
import os
from django.conf import settings
from django.test.utils import get_runner


# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myugctracker.settings")


def run_tests():
    # Убедитесь, что настройки Django инициализированы
    django.setup()
    TestRunner = get_runner(settings)

    # Создайте список микросервисов для тестирования
    microservices = ['company_service', 'user_profile', 'users']

    for microservice in microservices:
        print(f"Running tests for {microservice}...")
        test_runner = TestRunner()
        failures = test_runner.run_tests([microservice])
        if failures:
            print(f"Tests failed for {microservice}")
        else:
            print(f"All tests passed for {microservice}")

    # Выход с соответствующим кодом завершения
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()

