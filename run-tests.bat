@echo off
chcp 65001 > nul

echo === Шаг 1: Создание виртуального окружения ===
python -m venv venv
call venv\Scripts\activate

echo === Шаг 2: Установка зависимостей ===
pip install --upgrade pip
pip install -r requirements.txt

echo === Шаг 3: Установка браузеров Playwright ===
playwright install chromium

echo === Шаг 4: Запуск тестов ===
pytest tests/ -v

rem Сохраняем код выхода pytest
set TEST_EXIT_CODE=%ERRORLEVEL%

if %TEST_EXIT_CODE% equ 0 (
    echo === ИТОГ: PASSED ===
    exit /b 0
) else (
    echo === ИТОГ: FAILED ===
    exit /b %TEST_EXIT_CODE%
)

