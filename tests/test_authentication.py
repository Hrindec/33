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


# Тест 1: Успешная авторизация с email и паролем
def test_successful_login_with_email(browser):
    browser.get("https://b2c.passport.rt.ru/")

    # Ввод email и пароля
    # Найти кнопку для выбора email
    address_tab = browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    address_tab.click()  # Кликаем по вкладке, чтобы выбрать тип логина

    # Найти поле для ввода email
    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("ivan.ivanov2025@mail.ru")

    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    # Нажать кнопку "Войти"
    login_button = browser.find_element(By.XPATH, '//button[text()="Войти"]')
    login_button.click()

    time.sleep(5)
    assert "Личный кабинет" in browser.page_source


# Тест 2: Некорректный email при авторизации
def test_invalid_login_email(browser):
    browser.get("https://b2c.passport.rt.ru/")

    # Кликаем по вкладке, чтобы выбрать тип логина (по email)
    address_tab = browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    address_tab.click()

    # Находим поле для ввода email, используя By.NAME
    login_field = browser.find_element(By.NAME, 'Электронная почта')  # Поле для ввода email
    login_field.send_keys("invalid-email@mail.ru")

    # Находим поле для ввода пароля
    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("ValidPassword123")

    # Нажимаем кнопку "Войти"
    login_button = browser.find_element(By.XPATH, '//button[text()="Войти"]')
    login_button.click()

    time.sleep(2)
    assert "Неверный логин или пароль" in browser.page_source


# Тест 3: Некорректный пароль при авторизации
def test_invalid_login_password(browser):
    browser.get("https://b2c.passport.rt.ru/")

    # Кликаем по вкладке, чтобы выбрать тип логина (по email)
    address_tab = browser.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    address_tab.click()

    # Находим поле для ввода email, используя By.NAME
    login_field = browser.find_element(By.NAME, 'Электронная почта')  # Поле для ввода email
    login_field.send_keys("invalid-email@mail.ru")

    # Находим поле для ввода пароля, используя By.NAME
    password_field = browser.find_element(By.NAME, 'Пароль')
    password_field.send_keys("WrongPassword123")

    # Нажимаем кнопку "Войти"
    login_button = browser.find_element(By.XPATH, '//button[text()="Войти"]')
    login_button.click()

    time.sleep(2)
    assert "Неверный логин или пароль" in browser.page_source


# Тест 4: Успешная регистрация с номером телефона
def test_successful_registration_with_email_and_phone(browser):
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
    password_field.send_keys("ValidPassword123")

    confirm_password_field = browser.find_element(By.NAME, 'confirmPassword')
    confirm_password_field.send_keys("ValidPassword123")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(5)
    assert "Введите код" in browser.page_source


# Тест 5: Проверка минимальной длины пароля
def test_password_min_length(browser):
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
    password_field.send_keys("short")

    confirm_password_field = browser.find_element(By.NAME, 'confirmPassword')
    confirm_password_field.send_keys("short")

    continue_button = browser.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    continue_button.click()

    time.sleep(2)
    assert "Пароль должен содержать хотя бы 8 символов" in browser.page_source

# Тест 6: Проверка формы на наличие кнопки "Забыли пароль?"
def test_forgot_password_link(browser):
    browser.get("https://b2c.passport.rt.ru/")

    # Перейти на страницу авторизации
    login_button = browser.find_element(By.XPATH, '//*[text()="Войти"]')
    login_button.click()

    time.sleep(2)

    # Проверка наличия кнопки "Забыли пароль?"
    forgot_password_link = browser.find_element(By.XPATH, '//*[text()="Забыли пароль?"]')
    assert forgot_password_link.is_displayed()

# Тест 7: Проверка успешного восстановления пароля через email
def test_password_reset_with_email(browser):
    browser.get("https://b2c.passport.rt.ru/")

    # Перейти на страницу авторизации
    login_button = browser.find_element(By.XPATH, '//*[text()="Войти"]')
    login_button.click()

    time.sleep(2)

    # Кликнуть по ссылке "Забыли пароль?"
    forgot_password_link = browser.find_element(By.XPATH, '//*[text()="Забыли пароль?"]')
    forgot_password_link.click()

    time.sleep(2)

    # Ввод email для восстановления пароля
    address_field = browser.find_element(By.XPATH, '//*[@id="address"]')
    address_field.send_keys("ivan.ivanov@mail.ru")

    submit_button = browser.find_element(By.XPATH, '//button[text()="Отправить"]')
    submit_button.click()

    time.sleep(5)

    # Проверка успешного восстановления
    assert "Письмо с инструкциями отправлено на вашу почту" in browser.page_source
