import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

@pytest.fixture(scope="module")
def driver():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_case1(driver):
    driver.get("https://sbis.ru/")
    wait = WebDriverWait(driver, 10)

    contacts_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Контакты')]")))
    contacts_link.click()

    tensor_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='tensor.ru' and @href='https://tensor.ru/']")))
    tensor_link.click()

    wait.until(lambda d: len(driver.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])

    element1 = (By.XPATH, "//p[@class='tensor_ru-Index__card-title tensor_ru-pb-16' and contains(text(), 'Сила в людях')]")
    try:
        element = wait.until(EC.presence_of_element_located(element1))
        assert element is not None, f"Элемент {element1} найден на странице."
    except NoSuchElementException:
        pytest.fail(f"Элемент {element1} отсутствует.")

    about_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/about']")))
    about_link.click()

    element_xpaths = [
        '//div[@class="tensor_ru-About__block3-image-wrapper"]//img[@alt="Разрабатываем систему СБИС"]',
        '//div[@class="tensor_ru-About__block3-image-wrapper"]//img[@alt="Продвигаем сервисы"]',
        '//div[@class="tensor_ru-About__block3-image-wrapper"]//img[@alt="Создаем инфраструктуру"]',
        '//div[@class="tensor_ru-About__block3-image-wrapper"]//img[@alt="Сопровождаем клиентов"]'
    ]

    element_dimensions = {}
    for xpath in element_xpaths:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element_dimensions[xpath] = (element.size['width'], element.size['height'])

    for xpath, dimensions in element_dimensions.items():
        print(f"Элемент {xpath}: Width = {dimensions[0]}, Height = {dimensions[1]}")

    reference_element = element_xpaths[0]
    reference_dimensions = element_dimensions[reference_element]

    for xpath, dimensions in element_dimensions.items():
        if xpath != reference_element:
            assert dimensions == reference_dimensions, f"Элемент {xpath} такого же размера как {reference_element}."

def test_case2(driver):
    driver.get("https://sbis.ru/contacts/72-tyumenskaya-oblast?tab=clients")

    time.sleep(5)

    #Проверка региона первая
    city = driver.find_element("xpath", "//div[@id='city-id-2']")
    region = driver.find_element("xpath", "//span[(@class='sbis_ru-Region-Chooser__text sbis_ru-link')]")
    expected_region = 'Тюменская обл.'

    city_name = city.text
    region_name = region.text

    if region_name == expected_region:
        print(f"Соответствие верно: {city_name} : {region_name}")
    else:
        driver,quit
        print(f"Ошибка соответствия: {city_name} : {region_name} (ожидалось: {expected_region})")

    driver.find_element("xpath", "//span[(@class='sbis_ru-Region-Chooser__text sbis_ru-link')]").click()
    driver.find_elements("xpath", "//ul[(@class = 'sbis_ru-Region-Panel__list-l')]")
    time.sleep(5)
    driver.find_element("xpath", "//li[@class='sbis_ru-Region-Panel__item']//span[contains(text(), '41 Камчатский край')]").click()
    time.sleep(3)

    #Проверка региона вторая
    region = driver.find_element("xpath", "//span[(@class='sbis_ru-Region-Chooser__text sbis_ru-link')]")
    expected_region = 'Камчатский край'

    region_name = region.text

    if region_name == expected_region:
        print(f"Соответствие верно:{region_name}")
    else:
        driver,quit
        print(f"Ошибка соответствия:{region_name} (ожидалось: {expected_region})")

    time.sleep(2)

    #Проверка изменения списка партнеров
    partners = driver.find_element("xpath", "//div[@class='sbisru-Contacts-List__name sbisru-Contacts-List--ellipsis sbisru-Contacts__text--md pb-4 pb-xm-12 pr-xm-32']")
    partners_title = 'СБИС - Камчатка'

    part = partners.text

    if part == partners_title:
        print("Список партнеров изменился")
    else:
        driver.quit()
        print("Ошибка: список партнеров не изменился")

    #Проверка URL и title
    current_url = driver.current_url
    current_title = driver.title
    title = 'СБИС Контакты — Камчатский край'
    url= "https://sbis.ru/contacts/41-kamchatskij-kraj?tab=clients"
    if current_title == title and current_url == url:
        print('Заголовок и title верный ')
    else:
        driver.quit()
        print('Несоответствие заголовка и title')

if __name__ == "__main__":
    pytest.main()


