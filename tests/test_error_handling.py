from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome(executable_path='./drivers/chromedriver')
    yield driver
    driver.quit()


 # Тест 1: Отсутствие обязательных полей при регистрации
def test_missing_required_fields(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    # Пропустить все поля и нажать "Зарегистрироваться"
    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Заполните обязательные поля" in browser.page_source

# Тест 2: Пустое поле пароля
def test_empty_password_field(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    name_field = browser.find_element(By.NAME, 'Имя')
    name_field.send_keys("Иван")

    surname_field = browser.find_element(By.NAME, 'Фамилия')
    surname_field.send_keys("Иванов")

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("ivan.ivanov@mail.ru")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("")

    confirm_password_field = browser.find_element(By.NAME, 'confirmPassword')
    confirm_password_field.send_keys("")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Пароль обязателен" in browser.page_source

# Тест 3: Отсутствие кода подтверждения
def test_missing_confirmation_code(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("+79161234567")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'confirmPassword')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(5)
    code_field = browser.find_element(By.NAME, 'code')
    code_field.send_keys("")

    submit_button = browser.find_element(By.XPATH, '//button[text()="Подтвердить"]')
    submit_button.click()

    time.sleep(2)
    assert "Введите код подтверждения" in browser.page_source

# Тест 4: Блокировка после нескольких неудачных попыток
def test_account_lock_after_multiple_failed_attempts(browser):
    browser.get("https://b2c.passport.rt.ru/")

    login_field = browser.find_element(By.NAME, 'username')
    login_field.send_keys("ivan.ivanov@mail.ru")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("WrongPassword123")

    login_button = browser.find_element(By.XPATH, '//button[text()="Войти"]')
    login_button.click()

    time.sleep(2)
    login_button.click()

    assert "Ваш аккаунт заблокирован" in browser.page_source

# Тест 5: Превышение лимита на количество символов
def test_exceed_max_length(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    name_field = browser.find_element(By.NAME, 'Имя')
    name_field.send_keys("Иван" * 100)  # Превышаем максимальную длину

    surname_field = browser.find_element(By.NAME, 'Фамилия')
    surname_field.send_keys("Иванов" * 100)  # Превышаем максимальную длину

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Длина имени не может превышать 50 символов" in browser.page_source
