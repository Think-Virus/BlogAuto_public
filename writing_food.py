import re
from time import sleep

import mistune
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs, BeautifulSoup
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

from env.settings import getCategoryId, CHAT_GPT_ACCOUNT

# 카테고리 별 글 형식
REQUEST_FROM = """요리 방법에 대해 설명하는 블로그 글 대신 써줘. 띄어쓰기와 들여쓰기, 줄바꿈 제외 2000글자 이상 되도록 최대한 자세하게, 그리고 추가적인 내용 포함해서 적어줘.
이미지는 넣지 말아줘. 내가 나중에 추가할께


요리 정보는 다음과 같아.
- 요리명 : {0}
- 요리 종류 : {1}
- 조리 방법 : {2}
- 재료 :
{3}
- 만드는 법:
{4}
- 저감 요리 TIP : {5}
- 영양 정보 :
  - 열량 : {6}kcal
  - 나트륨 : {7}mg
  - 탄수화물 : {8}g
  - 단백질 : {9}g
  - 지방 : {10}g


아래의 형식 활용해서 마크다운 형식으로 부탁할께. "키워드"는 요리명으로 적어주면 돼! 아래는 키워드가 "새우 두부 계란찜"일 때의 예시야.
# 새우 두부 계란찜 맛있게 만드는 법 :: 새우 두부 계란찜의 매력
오늘은 매우 간단하지만 맛과 영양 가득한 "새우 두부 계란찜"에 대해 알아보겠습니다. 이 요리는 반찬으로 손쉽게 즐길 수 있으며, 특히 초보 요리사들에게 추천합니다. 그럼 시작해봅시다!

## 새우 두부 계란찜의 첫번째 정보: 새우 두부 계란찜이란?
새우 두부 계란찜은 연두부와 칵테일 새우, 신선한 달걀 등을 활용하여 만드는 고소하고 부드러운 반찬입니다. 찌기 방법으로 조리되며, 간단한 재료와 손쉬운 과정으로 훌륭한 맛을 낼 수 있습니다.

## 새우 두부 계란찜의 두번째 정보: 새우 두부 계란찜을 만드는 법
### 재료:
- 연두부 75g(3/4모)
- 칵테일 새우 20g(5마리)
- 달걀 30g(1/2개)
- 생크림 13g(1큰술)
- 설탕 5g(1작은술)
- 무염버터 5g(1작은술)
- 시금치 10g(3줄기)
### 만드는 법:
1. 먼저, 손질된 칵테일 새우를 끓는 물에 데칩니다. 새우를 건져 물기를 제거하세요.
2. 연두부, 달걀, 생크림, 설탕, 무염버터를 믹서에 넣고 곱게 갈아줍니다. 그런 다음, 데친 새우를 함께 넣고 더 섞어주세요.
3. 다음으로, 시금치를 잘게 다져 혼합물 위에 뿌립니다.
4. 마지막으로, 혼합물을 찜기에 담고 중간 불에서 10분 동안 찐니다.
5. 완성된 새우 두부 계란찜을 접시에 담아 서빙하세요.
## 새우 두부 계란찜의 세번째 정보: 건강한 새우 두부 계란찜 만들기! [저감 요리 TIP]
새우 두부 계란찜은 나트륨을 줄이기 위해 소금이나 간장 대신 새우 자체의 감칠맛을 활용하는 것이 좋습니다. 또한, 시금치를 추가하여 칼륨을 공급받아 건강에도 이로운 요리입니다.
## 새우 두부 계란찜의 마지막 정보 : 새우 두부 계란찜의 영양 정보
열량 : 220kcal
나트륨 : 99mg
탄수화물 : 3g
단백질 : 14g
지방 : 17g
---
새우 두부 계란찜은 맛과 영양이 가득한 요리로, 가족과 친구들에게 간단하게 즐길 수 있는 완벽한 반찬입니다. 요리 미숙한 분들도 쉽게 따라 할 수 있으니, 지금 바로 도전해보세요! 마지막으로, 새우 두부 계란찜을 만들 때 건강을 생각하여 조리해보세요. 맛과 건강 모두 챙길 수 있는 훌륭한 요리입니다. 🍤🥚🍽
"""

ANSWER_READ_SCRIPT = """
                        const targetElement = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return targetElement ? targetElement.innerHTML : null;
                    """
ANSWER_READ_XPATH_FORM = '/html/body/div[1]/div[1]/div[2]/div/main/div[1]/div[1]/div/div/div/div[{0}]/div/div/div[2]/div[1]/div/div'
ANSWER_CODE_READ_SCRIPT = """
                        const targetElement = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return targetElement ? targetElement.innerText : null;
                    """
ANSWER_CODE_READ_XPATH_FORM = '//*[@id="__next"]/div[1]/div/div/main/div/div[1]/div/div/div/div[{0}]/div/div[2]/div[1]/div/div/pre/div/div[2]/code'

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
        self.data: dict = None
        self.count = 0
        self.image_subjects = []

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
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div/div/button[1]').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '/html/body/div/main/section/div/div/div/div[4]/form[2]/button').click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(CHAT_GPT_ACCOUNT['email'])
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(CHAT_GPT_ACCOUNT['password'])
        sleep(15)
        self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div[4]/button').click()

    def setting(self, data: dict, category):
        self.data = data
        self.category_id = getCategoryId(category)

    def writeContent(self):
        self.content = ""
        self.count = 0
        print('글 쓰는 중...')

        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/div/div/nav/div[1]/a').click()

        self.request_content = self.makeRequest(self.data)
        sleep(1)
        origin_content = self.executeChatGPT()

        soup = bs(origin_content, 'html.parser')
        # 첫 번째 h1 태그를 찾음
        first_h1_tag = soup.find('h1')
        first_h1_tag.extract()
        # 첫 번째 h1 태그의 텍스트 내용 출력
        if first_h1_tag:
            title = first_h1_tag.text
        else:
            title = ""

        content = str(soup)

        return title, content

    def executeChatGPT(self):
        self.count += 1

        prompt_textarea = self.driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        self.driver.execute_script('arguments[0].value=arguments[1]', prompt_textarea, self.request_content)
        self.driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]').send_keys(Keys.ENTER)
        sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/button').click()
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

    def makeRequest(self, data: dict) -> str:
        food_name = data["요리명"]
        # thumbnail = data["썸네일"]
        food_kind = data["종류"]
        cook_kind = data["조리방법"]
        ingredient = data["재료"]
        recipe = self.makeRecipe(data)
        reduce_sodium_tip = data["저감 조리법 TIP"]
        calorie = data["열량"]
        sodium = data["나트륨"]
        carbohydrate = data["탄수화물"]
        protein = data["단백질"]
        fat = data["지방"]

        return REQUEST_FROM.format(food_name, food_kind, cook_kind, ingredient, recipe, reduce_sodium_tip, calorie, sodium, carbohydrate,
                                   protein, fat)

    def makeRecipe(self, data: dict) -> str:
        recipe = ""
        # "만드는 법"으로 시작하는 키를 가진 항목 중 값이 비어있지 않은 항목을 추출
        recipe_steps = {key: value for key, value in data.items() if key.startswith("만드는 법") and "이미지" not in key and value.strip() != ''}

        # 결과 출력
        for step, description in sorted(recipe_steps.items()):
            recipe += "\t" + step + ":" + description + "\n"
        return recipe
