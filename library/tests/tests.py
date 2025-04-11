import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.binary_location = 'C:/chrome-win64/chrome.exe'

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    time.sleep(3)
    driver.quit()

BASE_URL = "http://127.0.0.1:8000"

def test_login(driver):
    driver.get(BASE_URL + "/auth/login/")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.send_keys("test")
    password_field.send_keys("password123")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Здравствуйте, test!')]"))
        )
    except Exception as e:
        print("HTML страницы после входа:", driver.page_source)
        raise e
    assert "Здравствуйте, test!" in driver.page_source, "Не удалось войти в систему"

def test_add_to_cart(driver):
    driver.get(BASE_URL + "/")
    book = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul#book-list li"))
    )
    add_to_cart_button = book.find_element(By.XPATH, ".//a[contains(text(), 'Положить в корзину')]")
    book_title = book.text.split(" от ")[0]
    add_to_cart_button.click()
    driver.get(BASE_URL + "/cart/")
    cart_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{book_title}')]"))
    )
    assert book_title in cart_item.text, f"Книга '{book_title}' не была добавлена в корзину"