import os
import sys
import urllib.request
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from env.settings import IMAGE_PATH

TYPE_ALL = "TYPE_ALL"
TYPE_SPECIFIC = "TYPE_SPECIFIC"


class ImageCrawler:
    def __init__(self, keyword, search_keyword, maxImages=25):
        self.keyword = keyword
        self.maxImages = maxImages
        self.search_keyword = search_keyword
        self.enable_retry = True

        # 폴더 설정
        self.keyword_path = IMAGE_PATH + "/" + keyword
        try:
            # 중복되는 폴더 명이 없다면 생성
            if not os.path.exists(self.keyword_path):
                os.makedirs(self.keyword_path)
        except OSError:
            print('os error')
            sys.exit(0)

        # 크롬 드라이버 설정
        # (크롤링할 때 웹 페이지 띄우지 않음, gpu 사용 안함, 한글 지원, user-agent 헤더 추가)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('lang=ko_KR')
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

        # 크롬 드라이버 최신 버전 설정
        service = ChromeService(executable_path=ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def crawling(self):
        self.driver.get(
            'https://www.google.com/search?q=' + self.search_keyword + '&tbm=isch&hl=ko&tbs=il:cl&sa=X&ved=0CAAQ1vwEahcKEwjwmsip0P7_AhUAAAAAHQAAAAAQAg&biw=1903&bih=872')
        self.driver.maximize_window()
        sleep(3)

        SCROLL_PAUSE_TIME = 1
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
                except:
                    break
            last_height = new_height

        images = self.driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
        count = 1
        i = 0
        error_count = 0
        while i < len(images):
            image = images[i]
            i += 1

            if count > self.maxImages:
                break

            try:
                # WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, image.id))).click()
                image.click()
                sleep(0.5)
                try :
                    img_url = self.driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]').get_attribute("src")
                except :
                    img_url = self.driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[2]/div/a/img[1]').get_attribute("src")

                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-Agent',
                     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')
                ]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(img_url, f'{self.keyword_path}/{self.search_keyword + str(count)}.jpg')
                count = count + 1
                error_count = 0
            except Exception as e:
                print('e : ', e)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                i -= 1

                error_count += 1
                if error_count == 3:
                    break
                else:
                    continue

        self._scaling()

    def _scaling(self, type=TYPE_SPECIFIC):
        for filename in os.listdir(self.keyword_path):
            if type == TYPE_SPECIFIC and filename.find(self.search_keyword) == -1:
                continue
            file_path = os.path.join(self.keyword_path, filename)
            self._resize(file_path, 100 * 1024)

    def _resize(self, file_path, target_size):
        try:
            image = Image.open(file_path)
            image.save(file_path, optimize=True, quality=85)
            while os.path.getsize(file_path) > target_size:
                width, height = image.size
                width = int(width * 0.9)
                height = int(height * 0.9)
                image = image.resize((width, height))
                image.save(file_path, optimize=True, quality=85)
        except Exception as e:
            print(file_path+"\n fail!")
            print(e)
            os.remove(file_path)

