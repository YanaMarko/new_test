#!/bin/bash
# Завершать скрипт при любой ошибке
set -e

echo "=== Шаг 1: Создание виртуального окружения ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Шаг 2: Установка зависимостей ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Шаг 3: Установка браузеров Playwright ==="
playwright install chromium

echo "=== Шаг 4: Запуск тестов ==="
# BASE_URL прокидывается из окружения песочницы
pytest tests/ -v

echo "=== ИТОГ: PASSED ==="
