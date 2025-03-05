from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from env.settings import getCategoryId


class Uploader:
    def __init__(self, now_account):
        self.title = None
        self.content = None
        self.category_id = None

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('lang=ko_KR')
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

        # 크롬 드라이버 최신 버전 설정
        self.driver = webdriver.Chrome(options=chrome_options)

        # 로그인
        self.driver.get('https://www.tistory.com/')
        self.driver.find_element(By.XPATH, '//*[@id="kakaoHead"]/div/div[3]/div/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/a[2]').click()
        self.driver.find_element(By.XPATH, '//*[@id="loginId--1"]').send_keys(now_account[0])
        self.driver.find_element(By.XPATH, '//*[@id="password--2"]').send_keys(now_account[1])
        self.driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

    def update(self, title, content, category, thumbnail_img):
        self.title = title
        self.content = thumbnail_img + "\n" + content
        self.category_id = getCategoryId(category)

    def customUpload(self):
        # 글쓰기로 이동
        self.driver.get('https://big-think1004.tistory.com/manage/newpost/?type=post&returnURL=%2Fmanage%2Fposts%2F')
        # self.driver.get('https://virus-lab.tistory.com/manage/newpost/?type=post&returnURL=%2Fmanage%2Fposts%2F')
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            # 취소하기(닫기)
            alert.dismiss()
        except:
            print("no alert")

        # 진행 전 체크
        while True:
            if self.driver.current_url == "https://big-think1004.tistory.com/manage/newpost/?type=post&returnURL=%2Fmanage%2Fposts%2F":
                break
            else:
                sleep(1)

        ## 카테고리 설정
        self.driver.find_element(By.XPATH, '//*[@id="category-btn"]').click()
        sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@id="category-item-' + str(self.category_id) + '"]').click()
        ## 제목 입력
        self.driver.find_element(By.XPATH, '//*[@id="post-title-inp"]').send_keys(self.title)
        ## 내용 입력
        content_write_script = """xpath = '//*[@id="editor-tistory_ifr"]'

// iframe 요소를 JavaScript로 선택합니다.
const iframe =  document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;


// iframe 요소가 제대로 선택되었는지 확인합니다.
if (iframe) {
  // iframe 내부의 document 객체를 가져옵니다.
  const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;

  // 편집기의 내용을 변경하려면 다음과 같이 작성합니다.
  iframeDocument.body.innerHTML = arguments[0];

  // 편집기 내용을 가져오려면 다음과 같이 작성합니다.
  const content = iframeDocument.body.innerHTML;
  console.log(content); // 이때, 콘솔에 현재 편집기의 내용이 출력됩니다.
} else {
  console.error('iframe을 찾을 수 없습니다.');
}
"""
        self.driver.execute_script(content_write_script, self.content)
        sleep(0.5)
        ## 글 최적화

        self.driver.find_element(By.XPATH, '//*[@id="editor-mode-layer-btn-open"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="editor-mode-html"]').click()
        sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@id="html-editor-container"]/div[1]/div/div/div/div/div/div[5]/div/div/button').click()
        self.driver.find_element(By.XPATH, '//*[@id="editor-mode-kakao-tistory"]').click()

        # 업로드
        sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="publish-layer-btn"]').click()
        sleep(1)
        ## 홈 주제 설정
        self.driver.find_element(By.XPATH, '//*[@id="editor-root"]/div[6]/div/div/div/form/fieldset/div[2]/div/dl[2]/dd/div/button').click()
        sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="editor-root"]/div[6]/div/div/div/form/fieldset/div[2]/div/dl[2]/dd/div/div/div/div[28]').click()
        ##업로드 진행
        self.driver.find_element(By.XPATH, '//*[@id="publish-btn"]').click()

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            if alert.text == '하루에 새롭게 공개 발행할 수 있는 글은 최대 15 개까지입니다. ':
                return False
        except:
            print("no_alert")
            return True

        return True
