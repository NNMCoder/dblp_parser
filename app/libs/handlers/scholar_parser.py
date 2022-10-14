import time
from fastapi import HTTPException, status
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class ScholarParser:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-infobars')
        self.chrome_options.add_argument('--remote-debugging-port=9222')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.driver = self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(
            5)  # нормально работает только на 102 версии драйвера (https://github.com/SeleniumHQ/selenium/issues/10799)
        self.link = 'https://scholar.google.ru/citations?view_op=search_authors'

    async def search_author_link(self, query):
        try:
            h_index, cited_count = None, None
            self.driver.get(self.link)
            search = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/form/div/input")
            search.send_keys(f'{query}')
            search.send_keys(Keys.ENTER)
            result = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[2]/div/div/div/div/h3/a").click()
            h_index = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[12]/div[2]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]").text
            cited_count = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[12]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]").text
            return h_index, cited_count


        except NoSuchElementException:
            return h_index, cited_count
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        except Exception as exc:
            return h_index, cited_count
            # raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

        finally:
            self.driver.close()
            self.driver.quit()


