echo "=== Шаг 1: Проверка и запуск тестов ==="

# Пробуем запустить pytest напрямую через стандартные модули или глобальную команду
if command -v pytest &>/dev/null; then
    pytest tests/ -v
    TEST_EXIT_CODE=$?
elif command -v python3 &>/dev/null; then
    python3 -m pytest tests/ -v
    TEST_EXIT_CODE=$?
elif command -v python &>/dev/null; then
    python -m pytest tests/ -v
    TEST_EXIT_CODE=$?
else
    # Если глобальной команды нет, пробуем вызвать напрямую через python3/python без venv
    pytest tests/ -v 2>/dev/null || python3 -m pytest tests/ -v 2>/dev/null || python -m pytest tests/ -v
    TEST_EXIT_CODE=$?
fi

# Выводим итог для робота-проверяльщика
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=== ИТОГ: PASSED ==="
    exit 0
else
    echo "=== ИТОГ: FAILED ==="
    exit $TEST_EXIT_CODE
fi

