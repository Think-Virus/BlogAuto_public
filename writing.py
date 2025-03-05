import email
import imaplib
import random
import re
import smtplib
import sys
import urllib
from datetime import datetime
from email.header import make_header, decode_header
from email.mime.text import MIMEText
from time import sleep

import clipboard
import mistune
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs, BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from env.settings import BOOK_ID, FOOD_ID, getCategoryId, CHAT_GPT_ACCOUNT, GMAIL_ACCOUNT

# 카테고리 별 글 형식
FOOD_CONTENT_TEMPLET = """블로그 글 대신 써줘.\nkeyword는 \"{0}\"이고 글 주제는 \"{1} 맛있게 만드는 법\"이야.
아래의 형식 활용해서 마크다운 형식으로 부탁할께
재료의 정확한 양을 알려주면 좋겠고, 독특한 방식이라는 것을 강조해줘.
양념은 keyword에 맞게 부탁해

# 오징어 볶음 맛있게 만드는 법 :: 오늘은 오징오징 오징어다~!
자, 오늘은 오징어 볶음에 대해 알아보겠습니다!
저만의 독특한 레시피 알려드릴께요 >_<

## 오징어 볶음의 첫번째 정보: 오징어 볶음이란?
~~

## 오징어 볶음의 두번째 정보: 오징어 볶음을 준비하는 방법, 레시피

이제 오징어 볶음을 맛있게 만드는 방법에 대해 알려드리겠습니다. 오징어 볶음을 준비하기 위해 필요한 재료와 순서는 다음과 같습니다:
재료 :
순서 :
1.
2.
3.
4.
...

## 오징어 볶음의 세번째 정보: 다양한 오징어 볶음 버전

오징어 볶음은 다양한 변형 버전이 존재합니다. 몇 가지 예시를 들어보면, ~ 또는 ~ 사용하여 특별한 양념맛을 즐길 수도 있습니다. 자신의 취향에 맞게 오징어 볶음을 변형하여 더욱 맛있게 즐겨보세요.


이렇게 오징어 볶음에 대해 간략하게 알아보았습니다. 맛있는 오징어 볶음 요리를 즐겨보세요!
잘 봐주셔서 감사합니다.
"""
BOOK_CONTENT_TEMPLET = """블로그 글 대신 써줘.
keword는 "{0}"이고 글 주제는 "{1} :: 줄거리, 의미 해석, 전문가 평, 나의 감상평"이야.
줄거리와 의미 해석, 나의 감상평, 전문가 평 모두 분량은 좀 길게, 자세하게 적어줬으면 좋겠어.
아래는 keyword가 "데미안"일 때의 내용이야. 아래 내용과 100% 같은 형식으로 작성해줬으면 하고, 마크다운 형식으로 부탁할께.
---------------------------------------------------------

자, 오늘은 데미안에 대해 알아보겠습니다!
# 데미안 :: 줄거리, 의미 해석, 전문가 평, 나의 감상평
## 앞으로의 내용 한 줄 요약
### 데미안 줄거리 한 줄 요약
데미안은 세계의 현실과 정체성 탐색에 대한 내면적인 여정을 그린 헤르만 헤세의 소설입니다.

### 데미안에 담긴 의미 해석 한 줄 요약
데미안에 담긴 의미는 개인적인 자아와 사회적인 기준 사이에서 자아를 발견하고 성장해 나가는 인간의 내면적 탐색을 상징적으로 표현한 것입니다.

### 데미안에 대한 전문가 평 한 줄 요약
데미안은 헤르만 헤세의 대표작으로, 심리적인 성장과 자기탐색을 다루는 독자적인 이야기로 평가받고 있습니다.

### 데미안에 대한 나의 감상평 한 줄 요약
저는 데미안을 읽고 주인공의 내면적인 고뇌와 인생의 의미를 탐구하는 여정에 감명을 받았습니다.

---

## 데미안 심층 분석
###  데미안 줄거리 상세 내용
데미안은 헤르만 헤세의 대표작으로, 주인공인 데미안은 보통 사회적인 규범과 기대에 맞춰 살지만, 그 안에서 내면의 고뇌를 겪고 있습니다.
어린 시절부터 예리한 지성과 예술적인 감수성을 지니고 있던 데미안은 사회의 틀과 자신의 내면 사이에서 갈등을 겪으며 자아를 탐색하기 시작합니다.
그는 정체성을 찾기 위해 사회적 압박과 도전을 받으며, 자신의 진정한 본성과 운명을 발견하기 위한 여정에 나섭니다.
이 과정에서 그는 다양한 인물들과의 만남을 통해 자아의 발견과 성장을 경험하게 됩니다.

### 데미안에 담긴 의미 해석 상세 내용
데미안에는 개인적인 자아의 탐구와 사회적인 기준과의 대립이 주요 의미로 담겨있습니다.
이 작품은 현실 세계와 자아의 충돌, 개인의 내면 성장과정을 그려내는데, 이는 헤르만 헤세의 자기탐색적인 철학과 깊은 연관이 있습니다.
데미안은 주인공인 데미안의 이야기를 통해 사회의 기대와 규범에 맞추려는 욕망과 개인의 본성, 예술적인 감수성을 발현하려는 욕망과의 대립을 다루고 있습니다.
이를 통해 독자는 자아를 발견하고 개인적인 성장을 이루기 위해 사회적인 틀을 벗어남으로써 진정한 자아를 찾아가는 과정을 공감하며 생각해볼 수 있습니다.

### 데미안에 대한 전문가 평 상세 내용
데미안은 헤르만 헤세의 대표작으로 평가받고 있습니다.
이 작품은 정교한 문체와 깊은 내면적 탐구로 독자들에게 깊은 감동과 생각을 안겨주며, 자아와 사회적인 틀 사이의 갈등과 성장을 그린다는 점에서 평단들에게 높은 평가를 받고 있습니다.
헤세는 데미안을 통해 개인의 내면 성장과 현실 세계와의 대립을 다루면서 독자들에게 심오한 철학적 사고를 제시합니다.
그 결과, 데미안은 문학적인 가치와 함께 인간의 존재와 사회적인 기준에 대한 깊은 인식을 독자들에게 전달하고 있습니다.

### 데미안에 대한 나의 감상평 상세 내용
저는 데미안을 읽고 많은 감명을 받았습니다. 
주인공인 데미안의 내면적인 고뇌와 성장 과정이 심오하게 그려져 있어서 이야기에 몰입할 수 있었습니다.
데미안은 현실의 압박과 규범에 맞추려는 욕망과 개인의 본성, 예술적인 감수성을 발현하려는 욕망과의 대립을 다루는데, 이는 나 자신의 삶에서 겪는 고민과 상황과도 연결될 수 있었습니다.
데미안은 자아를 찾고 성장하기 위해 도전하고 끊임없이 탐구하는 모습을 보여줌으로써 독자로 하여금 자아를 발견하고 성장하는 과정에 대해 생각해보게 만들었습니다.
이 소설은 깊은 사색을 요구하지만, 그만큼 높은 만족감을 주는 작품이었습니다.

---

## 데미안에 대한 결론
데미안은 헤르만 헤세의 작품 중에서도 독특하고 깊은 내면적 탐구를 담은 대표작입니다. 
이 소설은 사회의 기준과 개인의 본성 사이의 대립, 자아의 발견과 성장을 다루며 독자들에게 깊은 생각과 감동을 안겨줍니다. 
데미안은 현실과 자아의 충돌을 통해 자아를 탐색하고 성장하는 과정을 그린데, 이는 독자로 하여금 자신의 내면을 돌아보고 성장의 기회를 발견할 수 있도록 함께 합니다.

이 작품은 문학적인 가치와 함께 사회적인 압박과 개인의 내면적 탐구에 관심이 있는 독자들에게 강력히 추천하는 작품입니다.
데미안을 읽으면서 우리 자신의 삶과 성장에 대해 생각해보는 시간을 가져보세요.
이 소설은 우리가 진정한 자아를 발견하고 세상과 조화롭게 존재하기 위해 필요한 내면적인 여정을 다시금 상기시켜줄 것입니다.

마지막으로, 데미안은 현대문학의 걸작 중 하나로서 영원한 가치와 의미를 지니고 있습니다.
그래서 이 소설은 많은 사람들에게 영감과 용기를 주고, 인간의 내면을 탐구하는 고전 중 하나로 끊임없이 읽어져야 할 작품입니다.
데미안의 세계로 떠나 보세요, 그리고 새로운 통찰과 깨달음을 얻을 수 있는 여정에 함께해보시기 바랍니다.
~~"""
BOOK_QUESTION_HEAD = """블로그에 쓸 내용 중 일부인데 마크다운 형식으로 가독성 좋게 글 보강해줘.
그리고 내용도 존댓말로 바꿔줬으면 줘.
다른 추가적인 내용 없이 이에 대해서만 부탁해"""

ANSWER_READ_SCRIPT = """
                        const targetElement = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return targetElement ? targetElement.innerHTML : null;
                    """
ANSWER_READ_XPATH_FORM = '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[1]/div/div/div/div[{0}]/div/div[2]/div[1]/div/div'
ANSWER_CODE_READ_SCRIPT = """
                        const targetElement = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return targetElement ? targetElement.innerText : null;
                    """
ANSWER_CODE_READ_XPATH_FORM = '//*[@id="__next"]/div[1]/div[2]/div/main/div[1]/div/div/div/div/div[{0}]/div/div[2]/div[1]/div/div/pre/div/div[2]/code'

CONTINUE_WRITE_SCRIPT = """
        const targetElement = document.evaluate('//*[@id="__next"]/div[1]/div[2]/div/main/div/div[2]/form/div/div[1]/div/div[2]/div/button', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (targetElement) {
            if (targetElement.innerText == 'Continue generating'){
                targetElement.click();
                return 'True'
            } else {
                return 'False'
            }
        } else {
            return 'False'
        }
"""
ILLEGAL_ALERT_CLICK_SCRIPT = """
        const targetElement = document.evaluate('//*[@id="radix-:r2m:"]/div[2]/div/div/button', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (targetElement) {
            if (targetElement.innerText == 'Continue generating'){
                targetElement.click();
                return 'True'
            } else {
                return 'False'
            }
        } else {
            return 'False'
        }
"""


class Writing:
    def __init__(self):
        self.content = ""
        self.request_content = None
        self.category_id = None
        self.keyword = None
        self.count = 0
        self.image_subjects = []
        self.subtitle_div_class_name = '_6qiGVcoz'
        self.content_div_class_name = "sRKmzCQk"

        # 초기 설정
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = uc.Chrome(use_subprocess=True, options=options)
        driver.maximize_window()

        self.driver = driver
        self.driver.get("https://chat.openai.com/")
        self.driver.implicitly_wait(3)
        try:
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[4]/button[1]').click()
        except:
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div/button[1]').click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '/html/body/div/main/section/div/div/div/div[4]/form[2]/button').click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(CHAT_GPT_ACCOUNT['email'])
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(CHAT_GPT_ACCOUNT['password'])
        sleep(15)
        self.driver.find_element(By.XPATH, '//*[@id="radix-:ri:"]/div[2]/div/div[4]/button').click()
    def setting(self, keyword, category):
        self.keyword = keyword
        self.category_id = getCategoryId(category)

    def _settingNamuwikiClassName(self, namuwiki_url):
        # 이미지들 삽입 전 메일로 확인
        # 설정
        user = GMAIL_ACCOUNT['email']
        password = GMAIL_ACCOUNT['password']
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user, password)

        # 메일 보내기
        send_msg = MIMEText("""{0},\n['subtitle_div_class_name','content_div_class_name']""".format(namuwiki_url))
        send_msg['Subject'] = "나무위키 클래스 이름 또 바뀜"
        smtp.sendmail(user, user, send_msg.as_string())
        smtp.quit()

        # 메일 받을 준비
        # 유저 개인정보 (환경변수 설정)
        load_dotenv()
        # IMAP 서버에 연결하기
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(user, password)
        # 접근하고자 하는 메일함 이름
        imap.select("INBOX")

        # 아예 해당 내용 넘어갈 것인지 확인
        while True:
            print("메일 확인 중")
            sleep(5)
            # status = 이메일 접근 상태
            # messages = 선택한 조건에 해당하는 메일의 id 목록
            # ('OK', [b'00001 00002 .....'])
            try:
                status, messages = imap.uid('search', None, '(FROM ' + user + ')')
            except:
                imap = imaplib.IMAP4_SSL("imap.gmail.com")
                imap.login(user, password)
                # 접근하고자 하는 메일함 이름
                imap.select("INBOX")
                status, messages = imap.uid('search', None, '(FROM ' + user + ')')
            messages = messages[0].split()
            # 0이 가장 마지막 메일, -1이 가장 최신 메일
            recent_email = messages[-1]
            # fetch 명령어로 메일 가져오기
            res, msg = imap.uid('fetch', recent_email, "(RFC822)")
            # 사람이 읽을 수 있는 형태로 변환
            raw_readable = msg[0][1].decode('utf-8')
            # raw_readable에서 원하는 부분만 파싱하기 위해 email 모듈을 이용해 변환
            email_message = email.message_from_string(raw_readable)

            # 메일 제목
            subject = make_header(decode_header(email_message.get('Subject')))
            if str(subject).startswith("나무위키 클래스 이름 또 바뀜") and str(subject).find("@") != -1:
                choice = int(str(subject).split("@")[1])

                if choice == 2:
                    return False
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))
                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            body = part.get_payload(decode=True)  # decode
                            break
                else:
                    body = email_message.get_payload(decode=True)

                body = eval(str(body.decode('utf-8')).strip())
                self.subtitle_div_class_name = body[0].replace("+", "\\+")
                self.content_div_class_name = body[1].replace("+", "\\+")
                return True
            else:
                continue

    def writeContent(self, isAuto=False, namuwiki_url=""):
        self.content = ""
        self.count = 0
        print('글 쓰는 중...')

        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/nav/div[1]/a').click()

        if self.category_id == BOOK_ID:
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--lang=ko_KR')
                # headless임을 숨기기 위해서
                # headless인 경우 Cloudflare 서비스가 동작한다.
                chrome_options.add_argument(
                    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
                driver = webdriver.Chrome(options=chrome_options)
                if not isAuto:
                    keyword_url = urllib.parse.quote(self.keyword)
                    namuwiki_url = 'https://namu.wiki/w/' + keyword_url

                driver.get(url=namuwiki_url)

                # 나무위키는 주기적으로 클래스 명을 바꾸므로 이를 해소하기 위해 반자동 시스템 도입
                while True:
                    try:
                        driver.find_element(By.CLASS_NAME, self.subtitle_div_class_name)
                        driver.find_element(By.CLASS_NAME, self.content_div_class_name)
                        break
                    except:
                        if not self._settingNamuwikiClassName(namuwiki_url):
                            return "", ""

                total_content_html = driver.execute_script('return document.body.innerHTML')
                total_content_soup = bs(total_content_html, "html.parser")

                subtitle_div = driver.find_element(By.CLASS_NAME, self.subtitle_div_class_name)
                subtitle_html = driver.execute_script('return arguments[0].innerHTML', subtitle_div)
                subtitle_soup = bs(subtitle_html, "html.parser")

                # 헤더가 될 항목 추출
                sub_title_elements = subtitle_soup.find_all('span')
                sub_titles = [span.get_text() for span in sub_title_elements]
                # 헤더의 내용들 추출
                contents = []

                for _soup in total_content_soup.find_all('div', class_=self.content_div_class_name):
                    if _soup.find_all('li'):
                        content = _soup.get_text(separator='\n')
                    else:
                        content = _soup.get_text()
                    contents.append(content)
            except:
                return "", ""
            # GPT 질문 내용 정리
            sub_title_list = []
            questions = []
            question = ""
            for i in range(len(sub_titles)):
                sub_title = "#" * sub_titles[i].count(".") + " " + sub_titles[i]
                content = contents[i]
                # 1. 1.1. 1.1.1 등으로 소재목이 나눠져있을 경우
                if sub_title[0] == "#" and sub_title[0:2] != "##" and sub_title[0:3] != "###":
                    sub_title_list.append(sub_titles[i])
                    if question:
                        questions.append(''.join(re.split(r'\s*\[\d+]\s*', question)))
                    question = sub_title + "\n" + content
                else:
                    if sys.getsizeof(question + "\n" + sub_title + "\n" + content) > 12000:
                        questions.append(''.join(re.split(r'\s*\[\d+]\s*', question)))
                        question = sub_title + "\n" + content
                    else:
                        question = question + "\n" + sub_title + "\n" + content
            questions.append(''.join(re.split(r'\s*\[\d+]\s*', question)))
            # 제목 만들기
            title = self.keyword + " :: " + ", ".join([_sub_title.split('. ')[1] for _sub_title in sub_title_list]) + ", 느낀점"
            print(title)
            remove_title_list = []
            # GPT 질문 시작
            for j, question in enumerate(questions):
                if (len(question) > 5000):
                    split_question = []
                    current_question = ""
                    for sentence in question.split("."):
                        if len(current_question) + len(sentence) < 5000:
                            current_question += sentence + ". \n"
                        else:
                            split_question.append(current_question)
                            current_question = ""
                    split_question.append(current_question)

                    for i, real_question in enumerate(split_question):
                        if i == 0:
                            if real_question.find("스포") != -1:
                                self.request_content = BOOK_QUESTION_HEAD + " 스포일러 내용 포함해서 적어줘" + "\n\n" + real_question
                            else:
                                self.request_content = BOOK_QUESTION_HEAD + "\n\n" + real_question
                        else:
                            self.request_content = "위 내용에 이어서 적어줘" + "\n\n" + real_question
                        answer_content = self.executeChatGPT()
                        if answer_content == "":
                            remove_title_list.append(sub_titles[j])
                            break
                        self.content += "\n" + answer_content
                    continue

                if question.find("스포") != -1:
                    self.request_content = BOOK_QUESTION_HEAD + " 스포일러 내용 포함해서 적어줘" + "\n\n" + question
                else:
                    self.request_content = BOOK_QUESTION_HEAD + "\n\n" + question
                answer_content = self.executeChatGPT()
                if answer_content == "":
                    remove_title_list.append(sub_titles[j])
                    continue
                self.content += "\n" + answer_content

            self.request_content = "위 전체 내용 바탕으로 {0}에 대해 #느낀점 마크다운 형식으로 적어줄래?".format(self.keyword)
            answer_content = self.executeChatGPT()
            self.content += "\n" + answer_content
            print(self.content)
            self.request_content = """위 전체 내용 바탕으로 {0}에 대해 이미지를 넣고자 하는데, 그에 알맞을 이미지 주제 를 아래 리스트에서 3개 선택해서 추천해줘.
['노을', '눈물', '바다', '별', '비', '새싹', '숲', '외로움', '웃음', '책', '철학', '하늘']

반환 형태는 ['주제1', '주제2', '주제3'] 이렇게 부탁할께
다른 첨언 없이 그냥 딱 ['주제1', '주제2', '주제3'] 이렇게 하나만 알려줘
뭐 "~에 대해 알려드리겠습니다." 이딴 사족 붙이지 말고 그냥 딱 ['주제1', '주제2', '주제3'] 이렇게 하나만 알려줘""".format(self.keyword)
            answer_content = self.executeChatGPT()
            self.image_subjects = self.checkImageSubject(answer_content)

            self.content.replace(".\n\n", ".<br>\n")

            for r in remove_title_list:
                sub_title_list.remove(r)
            title = self.keyword + " :: " + ", ".join([_sub_title.split('. ')[1] for _sub_title in sub_title_list]) + ", 느낀점"

            return title, self.content
        else:
            if self.category_id == FOOD_ID:
                self.request_content = FOOD_CONTENT_TEMPLET.format(self.keyword, self.keyword)
            elif self.category_id == BOOK_ID:
                self.request_content = BOOK_CONTENT_TEMPLET.format(self.keyword, self.keyword)
            else:
                print("카테고리 설정 오류")
                exit()

            answer_content = self.executeChatGPT()
            self.content = answer_content

            title = self.content.split('\n')[0].replace('# ', '').strip()
            content = self.content.replace('# ' + title + "\n", '', 1)

            self.log(title, content)

            return title, content

    def executeChatGPT(self):
        self.count += 1

        prompt_textarea = self.driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        self.driver.execute_script('arguments[0].value=arguments[1]', prompt_textarea, self.request_content)
        self.driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]').send_keys(Keys.ENTER)
        sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/button').click()
        # self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/form/div/div/button').click()

        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        sleep(2)
        self.driver.execute_script("""// XPath로 엘리먼트를 찾는 함수
function getElementByXPath(xpath) {
  return document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

// 클릭할 엘리먼트의 XPath
var targetXPath = '//*[@id="radix-:r2r:"]/div[2]/div/div/button';

// 엘리먼트를 찾고 클릭
var targetElement = getElementByXPath(targetXPath);
if (targetElement) {
  targetElement.click();
} else {
  console.error("해당 XPath를 가진 엘리먼트를 찾을 수 없습니다.");
}
""")

        pre_content = ""
        time_count = 0
        buffer_check = 0
        for i in range(1200):
            sleep(0.5)
            time_count += 1
            if time_count % 10 == 0:
                ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()

            is_question_changed = eval(self.driver.execute_script(ILLEGAL_ALERT_CLICK_SCRIPT))
            sleep(2)

            if is_question_changed:
                self.count -= 1
                return ""

            # 웹 페이지에서 자바스크립트 코드를 실행하여 targetElement의 값을 가져옵니다.
            answer_read_script = ANSWER_READ_SCRIPT.format(xpath=ANSWER_READ_XPATH_FORM.format(self.count * 2))
            current_content = self.driver.execute_script(answer_read_script)

            if current_content != pre_content:
                buffer_check = 0
                try:
                    if len(current_content) > len(pre_content):  # 글 작성 중인 상황
                        pre_content = current_content
                    else:  # 글 작성이 멈춘 상황( 잘린 상황일 수도 있음)
                        # 계속 쓰기 있는지 확인
                        is_write_continue = eval(self.driver.execute_script(CONTINUE_WRITE_SCRIPT))
                        sleep(2)
                        if is_write_continue:
                            # 계속 쓰기 진행
                            pre_content = current_content
                            continue
                        else:
                            # 결과 반환
                            answer_code_read_script = ANSWER_CODE_READ_SCRIPT.format(xpath=ANSWER_CODE_READ_XPATH_FORM.format(self.count * 2))
                            code_content = self.driver.execute_script(answer_code_read_script)
                            if code_content is None:
                                return self.refineHTML(current_content)
                            else:
                                return mistune.markdown(code_content)
                except Exception as e:
                    print(e)
            else:
                if buffer_check > 9:
                    # 계속 쓰기 있는지 확인
                    is_write_continue = eval(self.driver.execute_script(CONTINUE_WRITE_SCRIPT))
                    sleep(2)
                    if is_write_continue:
                        # 계속 쓰기 진행
                        pre_content = current_content
                        continue

                    # 결과 반환
                    answer_code_read_script = ANSWER_CODE_READ_SCRIPT.format(xpath=ANSWER_CODE_READ_XPATH_FORM.format(self.count * 2))
                    code_content = self.driver.execute_script(answer_code_read_script)
                    if code_content is None:
                        return self.refineHTML(current_content)
                    else:
                        return mistune.markdown(code_content)
                else:
                    buffer_check += 1

    def refineHTML(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')

        h_tags = sorted(set([tag.name for tag in soup.find_all(re.compile(r'^h\d$'))]))
        if h_tags:
            if h_tags[0] == "h1":
                return str(BeautifulSoup(html, 'html.parser').prettify())
            else:
                return_html = html
                for h in h_tags:
                    origin_num = int(h[1])
                    down_grade_num = origin_num - 1
                    return_html = return_html.replace(f"<h{origin_num}>", f"<h{down_grade_num}>").replace(f"</h{origin_num}>",
                                                                                                          f"</h{down_grade_num}>")
                return str(BeautifulSoup(return_html, 'html.parser').prettify())
        else:
            return html

    def checkImageSubject(self, text):
        # 문자열에서 '['와 ']' 사이의 내용만 추출
        start_idx = text.find('[')
        end_idx = text.find(']')
        if start_idx == -1 or end_idx == -1:
            return random.sample(['노을', '눈물', '바다', '별', '비', '새싹', '숲', '외로움', '웃음', '책', '철학', '하늘'], 3)

        target_str = text[start_idx:end_idx + 1]

        # 추출된 문자열을 리스트로 변환
        try:
            subject_list = eval(target_str)

            for subject in subject_list:
                if subject not in ['노을', '눈물', '바다', '별', '비', '새싹', '숲', '외로움', '웃음', '책', '철학', '하늘']:
                    return random.sample(['노을', '눈물', '바다', '별', '비', '새싹', '숲', '외로움', '웃음', '책', '철학', '하늘'], 3)

            return subject_list
        except:
            return random.sample(['노을', '눈물', '바다', '별', '비', '새싹', '숲', '외로움', '웃음', '책', '철학', '하늘'], 3)

    def log(self, title, content):
        log_text = """request_content : \n{0}\n\n\ntitle : \n{1}\n\n\ncontent : \n{2}""".format(self.request_content, title, content)

        file = open(
            "C:\\Users\\user\\PycharmProjects\\BlogAuto_v2\\log\\" + self.keyword + str(
                datetime.now().timestamp()) + ".txt", "w", encoding="UTF-8")
        file.write(log_text)
        file.close()
