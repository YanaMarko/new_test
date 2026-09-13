# Пытаемся определить доступную команду python (python3 или python)
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Ошибка: Python не найден в системе песочницы!"
    echo "=== ИТОГ: FAILED ==="
    exit 127
fi

echo "=== Шаг 1: Создание виртуального окружения ==="
$PYTHON_CMD -m venv venv
source venv/bin/activate

echo "=== Шаг 2: Установка зависимостей ==="
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

echo "=== Шаг 3: Установка браузеров Playwright ==="
$PYTHON_CMD -m playwright install chromium

echo "=== Шаг 4: Запуск тестов ==="
$PYTHON_CMD -m pytest tests/ -v
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=== ИТОГ: PASSED ==="
    exit 0
else
    echo "=== ИТОГ: FAILED ==="
    exit $TEST_EXIT_CODE
fi

