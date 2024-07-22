import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCase3:
    def __init__(self, download_link, expected_size, file_name, download_directory):
        self.download_link = download_link
        self.expected_size = expected_size
        self.file_name = file_name
        self.download_directory = download_directory
        self.full_path = os.path.join(download_directory, file_name)

        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def download_file(self):
        self.driver.get(self.download_link)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//a[@download]'))
        )
        download_button = self.driver.find_element(By.XPATH, '//a[@download]')
        download_button.click()

    def get_file_size_on_disk(self):
        return os.path.getsize(self.full_path)

    def run(self):
        self.download_file()
        print(f"файл скачивается {self.full_path}")

        actual_size = self.get_file_size_on_disk()
        print(f"реальный размер файла: {actual_size} bytes")

        if self.expected_size == actual_size:
            print("Размер одинаковый.")
        else:
            print("Ошибка: разный размер.")

        self.driver.quit()

if __name__ == "__main__":
    download_link = 'https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe'
    expected_size = 11 * 1024 * 1024
    file_name = 'sbisplugin-setup-web.exe'
    download_directory = '/Users/eg/Desktop/Tensor-Tests/downloads'

    test_case3 = TestCase3(download_link, expected_size, file_name, download_directory)
    test_case3.run()