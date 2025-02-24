from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest

# Фикстура для инициализации браузера
@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome(executable_path='./drivers/chromedriver')
    yield driver
    driver.quit()


# Тест 1: Успешная регистрация с email и паролем
def test_successful_registration_with_email(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    name_field = browser.find_element(By.NAME, 'Имя')
    name_field.send_keys("Иван")

    surname_field = browser.find_element(By.NAME, 'Фамилия')
    surname_field.send_keys("Иванов")

    # Кликаем по кнопке, чтобы открыть выпадающий список "Регион"
    region_dropdown_button = browser.find_element(By.XPATH, '//*[text()="Регион"]/following-sibling::div')
    region_dropdown_button.click()

    # После открытия списка, выбираем нужный элемент
    region_option = browser.find_element(By.XPATH, '//*[text()="Алтай Респ"]')
    region_option.click()

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("ivan.ivanov2025@mail.ru")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(5)
    assert "Введите код" in browser.page_source


# Тест 2: Успешная регистрация с номером телефона
def test_successful_registration_with_phone(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    name_field = browser.find_element(By.NAME, 'Имя')
    name_field.send_keys("Иван")

    surname_field = browser.find_element(By.NAME, 'Фамилия')
    surname_field.send_keys("Иванов")

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("+79161234567")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(5)
    assert "Введите код" in browser.page_source


# Тест 3: Ввод некорректного email
def test_invalid_email(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("invalid-email")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Некорректный email" in browser.page_source


# Тест 4: Ввод пароля, который не соответствует политике безопасности
def test_invalid_password(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("short")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("short")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Пароль должен содержать хотя бы одну заглавную букву" in browser.page_source


# Тест 5: Несовпадение пароля и подтверждения пароля
def test_password_mismatch(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("NoValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Пароли не совпадают" in browser.page_source


# Тест 6: Ввод номера телефона, который уже привязан к учетной записи
def test_phone_already_registered(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("+79161234567")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Телефон уже зарегистрирован" in browser.page_source


# Тест 7: Повторная отправка кода на телефон
def test_resend_sms_code(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("+79161234567")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(120)
    resend_button = browser.find_element(By.XPATH, '//*[text()="Получить код повторно"]')
    resend_button.click()

    time.sleep(2)
    assert "Код отправлен" in browser.page_source


# Тест 8: Некорректный код при регистрации
def test_invalid_code(browser):
    browser.get("https://b2c.passport.rt.ru/")
    register_button = browser.find_element(By.XPATH, '//*[text()="Зарегистрироваться"]')
    register_button.click()

    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("+79161234567")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'Подтверждение пароля')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(5)
    code_field = browser.find_element(By.NAME, 'code')
    code_field.send_keys("12345")

    submit_button = browser.find_element(By.XPATH, '//button[text()="Подтвердить"]')
    submit_button.click()

    time.sleep(2)
    assert "Неверный код" in browser.page_source