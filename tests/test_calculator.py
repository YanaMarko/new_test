import os
import pytest
from playwright.sync_api import sync_playwright, expect
import openpyxl

BASE_URL = os.getenv("BASE_URL", "https://pryaniki.com")
CALC_URL = f"{BASE_URL.rstrip('/')}/" # Скорректируйте путь, если калькулятор на подстранице

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(CALC_URL)
        yield page
        browser.close()

# --- БЛОК 1: UI И СТРУКТУРА (Шаблоны ИИ) ---

def test_01_ui_elements_visibility(page):
    """Кейс 1: Проверка видимости основных элементов управления калькулятора."""
    expect(page.locator("text=Мета-КП")).to_be_visible()
    expect(page.locator("select[name='tariff']")).to_be_visible()
    expect(page.locator("input[name='users_count']")).to_be_visible()
    expect(page.locator("input[name='license_term']")).to_be_visible()

def test_02_tariff_selection(page):
    """Кейс 2: Проверка переключения тарифов (Облако / Коробка)."""
    select = page.locator("select[name='tariff']")
    
    select.select_option("cloud")
    expect(page.locator(".tariff-type-label")).to_contain_text("Облако")
    
    select.select_option("box")
    expect(page.locator(".tariff-type-label")).to_contain_text("Коробка")

# --- БЛОК 2: ВАЛИДАЦИЯ ВВОДА (Шаблоны ИИ) ---

def test_03_validation_negative_users(page):
    """Кейс 3: Валидация — ввод отрицательного количества пользователей."""
    input_users = page.locator("input[name='users_count']")
    input_users.fill("-5")
    page.keyboard.press("Enter")
    
    # Предполагается наличие сообщения об ошибке или сброс в мин. значение
    expect(page.locator(".error-message")).to_be_visible()

def test_04_validation_max_license_term(page):
    """Кейс 4: Валидация — ограничение максимального срока лицензии."""
    input_term = page.locator("input[name='license_term']")
    input_term.fill("999") 
    page.keyboard.press("Enter")
    
    # Проверяем, что значение скорректировалось или появилась ошибка
    expect(page.locator(".error-message")).to_be_visible()

# --- БЛОК 3: ЛОГИКА И МОДУЛИ (Шаблоны ИИ) ---

def test_05_modules_activation_recalc(page):
    """Кейс 5: Активация дополнительных модулей влияет на блок ИТОГО."""
    initial_total = page.locator("#total_price").text_content()
    
    # Включаем чекбокс модуля (селектор примерный)
    page.locator("input[type='checkbox'][value='vnedrenie']").check()
    
    new_total = page.locator("#total_price").text_content()
    assert initial_total != new_total

def test_06_tm_hours_calculation(page):
    """Кейс 6: Расчет стоимости работ по модели T&M (Time and Materials)."""
    page.locator("input[name='tm_hours']").fill("10")
    page.keyboard.press("Enter")
    
    # Проверяем, что блок стоимости T&M обновился
    expect(page.locator("#tm_total_price")).not_to_contain_text("0")

def test_07_meta_kp_toggle(page):
    """Кейс 7: Включение опции 'Мета-КП' меняет структуру отображения сметы."""
    toggle = page.locator("input[name='meta_kp']")
    toggle.check()
    expect(page.locator("#meta_kp_section")).to_be_visible()

# --- БЛОК 4: СКВОЗНЫЕ СЦЕНАРИИ И ВЫГРУЗКА EXCEL ---

def test_08_full_cycle_calculation(page):
    """Кейс 8: Сквозной расчет: Облако + 50 пользователей + 12 месяцев + Внедрение."""
    page.locator("select[name='tariff']").select_option("cloud")
    page.locator("input[name='users_count']").fill("50")
    page.locator("input[name='license_term']").fill("12")
    page.locator("input[type='checkbox'][value='vnedrenie']").check()
    
    expect(page.locator("#total_price")).not_to_contain_text("0")
    expect(page.locator("#total_price")).not_to_contain_text("Ошибка")

def test_09_excel_export_download(page):
    """Кейс 9: Проверка успешного скачивания файла Excel при клике на 'Выгрузить'."""
    page.locator("select[name='tariff']").select_option("cloud")
    page.locator("input[name='users_count']").fill("10")
    
    # Ожидаем событие скачивания файла
    with page.expect_download() as download_info:
        page.locator("button#download_excel").click()
    
    download = download_info.value
    path = download.path()
    
    assert os.path.exists(path)
    assert download.suggested_filename.endswith(".xlsx")

def test_10_excel_content_validation(page):
    """Кейс 10: Валидация структуры скачанного Excel (проверка формул/данных)."""
    page.locator("select[name='tariff']").select_option("box")
    page.locator("input[name='users_count']").fill("25")
    
    with page.expect_download() as download_info:
        page.locator("button#download_excel").click()
        
    download = download_info.value
    path = download.path()
    
    # Читаем Excel файл парсером openpyxl
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    
    # Проверяем, что в файле есть данные (например, заголовок или ячейка с тарифом)
    cell_value = sheet["A1"].value
    assert cell_value is not None
    assert len(sheet.title) > 0
