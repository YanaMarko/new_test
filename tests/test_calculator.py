import os
import pytest
from playwright.sync_api import sync_playwright, expect
import openpyxl

BASE_URL = os.getenv("BASE_URL", "https://pryaniki.com")

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        yield page
        browser.close()

# --- БЛОК 1: UI И СТРУКТУРА (Спроектировано ИИ) ---

def test_01_ui_elements_visibility(page):
    """Кейс 1: Проверка видимости основных элементов управления калькулятора."""
    # Проверяем вкладки переключения блоков под калькулятором
    expect(page.locator("button:has-text('Модули')")).to_be_visible()
    expect(page.locator("button:has-text('Внедрение')")).to_be_visible()
    expect(page.locator("button:has-text('T&M')")).to_be_visible()
    # Проверяем кнопку выгрузки сметы
    expect(page.locator("button:has-text('Выгрузить смету в Excel')")).to_be_visible()

def test_02_tariff_selection(page):
    """Кейс 2: Проверка переключения тарифов (Облако / Коробка)."""
    # Ищем кнопки переключения тарифа по тексту, как на скриншоте
    btn_cloud = page.locator("button:has-text('TestQuest Облако')")
    btn_box = page.locator("button:has-text('TestQuest Коробка')")
    
    btn_box.click()
    # При переключении в синем блоке сметы должен поменяться заголовок или текст тарифа
    expect(page.locator(".selected-modules-box")).to_contain_text("TESTQUEST КОРОБКА")
    
    btn_cloud.click()
    expect(page.locator(".selected-modules-box")).to_contain_text("TESTQUEST ОБЛАКО")

# --- БЛОК 2: ВАЛИДАЦИЯ ВВОДА (Спроектировано ИИ) ---

def test_03_validation_negative_users(page):
    """Кейс 3: Валидация — ввод отрицательного количества пользователей."""
    # На скриншоте есть подпись "Число лицензий"
    input_users = page.locator("label:has-text('Число лицензий') + input, input[placeholder='100']")
    input_users.fill("-5")
    input_users.press("Enter")
    
    # Ищем появление сообщения об ошибке или сброс к минимальному значению 1
    assert input_users.input_value() != "-5"

def test_04_validation_max_license_term(page):
    """Кейс 4: Валидация — ограничение максимального срока лицензии."""
    # На скриншоте поле "Срок, мес." находится рядом с числом лицензий
    input_term = page.locator("label:has-text('Срок, мес.') + input")
    input_term.fill("999")
    input_term.press("Enter")
    
    # Система должна либо скорректировать значение, либо вывести ошибку валидации
    expect(page.locator("body")).to_contain_text("Неверное значение")

# --- БЛОК 3: ЛОГИКА И МОДУЛИ (Спроектировано ИИ) ---

def test_05_modules_activation_recalc(page):
    """Кейс 5: Активация дополнительных модулей влияет на блок ИТОГО."""
    # На скриншоте в ключевых модулях есть "Конструктор процессов"
    checkbox_process = page.locator("label:has-text('Конструктор процессов') input[type='checkbox']")
    
    # Запоминаем начальную сумму из синего блока (на скрине там 200 429 ₽)
    initial_total = page.locator("text=Всего").locator("xpath=..").text_content()
    
    checkbox_process.check()
    
    # Проверяем, что сумма изменилась после выбора модуля
    new_total = page.locator("text=Всего").locator("xpath=..").text_content()
    assert initial_total != new_total

def test_06_tm_hours_calculation(page):
    """Кейс 6: Расчет стоимости работ по модели T&M (Time and Materials)."""
    # Переходим на вкладку T&M
    page.locator("button:has-text('T&M')").click()
    
    # Находим инпут для ввода часов T&M
    input_hours = page.locator("input[name*='hours'], input[type='number']").last
    input_hours.fill("100")
    input_hours.press("Enter")
    
    # На скриншоте фиолетовый блок отображает "TIME&MATERIAL Всего 585 000 ₽"
    expect(page.locator("text=TIME&MATERIAL")).to_be_visible()
    expect(page.locator("text=585 000")).to_be_visible()

def test_07_meta_kp_toggle(page):
    """Кейс 7: Ввод названия компании и проверка заполнения мета-данных КП."""
    input_company = page.locator("label:has-text('Название компании') + input, input[placeholder='Название компании']")
    input_company.fill("ООО Ромашка")
    
    # Проверяем, что введенный текст отображается в поле
    expect(input_company).to_have_value("ООО Ромашка")

# --- БЛОК 4: СКВОЗНЫЕ СЦЕНАРИИ И ВЫГРУЗКА EXCEL ---

def test_08_full_cycle_calculation(page):
    """Кейс 8: Сквозной расчет: Облако + 100 пользователей + 12 месяцев."""
    page.locator("button:has-text('TestQuest Облако')").click()
    
    input_users = page.locator("label:has-text('Число лицензий') + input")
    input_users.fill("100")
    
    input_term = page.locator("label:has-text('Срок, мес.') + input")
    input_term.fill("12")
    input_term.press("Enter")
    
    # Итоговый блок сметы должен успешно пересчитаться и показать сумму
    expect(page.locator("text=200 429")).to_be_visible()

def test_09_excel_export_download(page):
    """Кейс 9: Проверка успешного скачивания файла Excel при клике на 'Выгрузить смету в Excel'."""
    # Перехватываем событие скачивания файла при клике на синюю кнопку
    with page.expect_download() as download_info:
        page.locator("button:has-text('Выгрузить смету в Excel')").click()
    
    download = download_info.value
    path = download.path()
    
    # Проверяем физическое существование файла на диске песочницы
    assert os.path.exists(path)
    assert download.suggested_filename.endswith(".xlsx")

def test_10_excel_content_validation(page):
    """Кейс 10: Валидация структуры скачанного Excel (проверка наличия данных через openpyxl)."""
    with page.expect_download() as download_info:
        page.locator("button:has-text('Выгрузить смету в Excel')").click()
        
    download = download_info.value
    path = download.path()
    
    # Открываем скачанную смету библиотекой openpyxl
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    
    # Проверяем, что файл не пустой и содержит данные (например, название тарифа или заголовки)
    assert sheet.max_row > 1
    wb.close()
