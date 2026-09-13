#!/bin/bash

echo "=== Шаг 1: Создание виртуального окружения ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Шаг 2: Установка зависимостей ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Шаг 3: Установка браузеров Playwright ==="
playwright install chromium

echo "=== Шаг 4: Запуск тестов ==="
# Выполняем тесты и сохраняем код ответа pytest в переменную
pytest tests/ -v
TEST_EXIT_CODE=$?

# Проверяем, как завершился pytest
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=== ИТОГ: PASSED ==="
    exit 0
else
    echo "=== ИТОГ: FAILED ==="
    exit $TEST_EXIT_CODE
fi

