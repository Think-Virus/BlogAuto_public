import email
import imaplib
import json
import smtplib
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from time import sleep

import pandas as pd
from dotenv import load_dotenv
from tistory import Tistory

import image_uploader_food
import uploader_food
import writing_food
from env.settings import ACCESS_TOKEN, BLOG_URL, IMAGE_HTML_START, IMAGE_HTML_IMG, IMAGE_HTML_END, CATEGORY, \
    T_STORY_ACCOUNT_LIST, JUST_CHECK_GUI, GMAIL_ACCOUNT


class Main():
    def __init__(self):
        # 입력하고 변경하는 속성
        self.keyword = ""
        self.category = CATEGORY[0]
        self.title = ""
        self.content = ""
        self.img_addresses = []
        self.html_code = ""
        self.thumbnail_img = ""
        self.image_subjects = ""

        self.NOW_ACCOUNT_INDEX = 0
        self.ACCOUNT_LIST_KEY = list(T_STORY_ACCOUNT_LIST.keys())
        self.NOW_ACCOUNT = T_STORY_ACCOUNT_LIST[self.ACCOUNT_LIST_KEY[self.NOW_ACCOUNT_INDEX]]
        CLIENT_ID = self.NOW_ACCOUNT[2]
        CLIENT_SECRET = self.NOW_ACCOUNT[3]

        # 기능 실행을 위해 필요한 속성
        self.tistory = Tistory(BLOG_URL, CLIENT_ID, CLIENT_SECRET)
        if JUST_CHECK_GUI:
            self.writing = None
        else:
            self.writing = writing_food.Writing()

        # 기타 설정
        self.tistory.access_token = ACCESS_TOKEN
        self.uploader = uploader_food.Uploader(self.NOW_ACCOUNT)

    def _insertImage(self):
        images_added_html = "</ol>\n" + self._getImageHTML()
        self.content = self.content.replace("</ol>", images_added_html)

    # 이미지 개수에 따른 HTML 코드 작성
    def _getImageHTML(self):
        num_img_addresses = len(self.img_addresses)

        if num_img_addresses == 0:
            return ""

        return_html = IMAGE_HTML_START
        for i in range(0, num_img_addresses):
            return_html += IMAGE_HTML_IMG.format(self.img_addresses.pop(0), i)
        return_html += IMAGE_HTML_END
        return return_html

    def _upload(self):
        self.uploader.update(self.title, self.content, self.category, self.thumbnail_img)
        if not self.uploader.customUpload():
            self.NOW_ACCOUNT_INDEX += 1
            self.NOW_ACCOUNT = T_STORY_ACCOUNT_LIST[self.ACCOUNT_LIST_KEY[self.NOW_ACCOUNT_INDEX]]
            self.uploader = uploader_food.Uploader(self.NOW_ACCOUNT)
            sleep(3)
            self._upload()

    def _thumbnailCreate(self):
        # 썸네일 이미지 업로드
        imageUploader = image_uploader_food.ImageUploaderFood(keyword=self.keyword, tistory=self.tistory, is_thumbnail=True)
        self.thumbnail_img = imageUploader.upload()

    def _recipeImageUpload(self):
        imageUploader = image_uploader_food.ImageUploaderFood(keyword=self.keyword, tistory=self.tistory)
        self.img_addresses = imageUploader.upload()

    def autoFoodExecute(self):
        # 자동으로 책에 대한 내용들 적도록 해야겠다.
        with open('data/recipe_data.json', encoding="utf-8") as f:
            js = json.loads(f.read())  ## json 라이브러리 이용
        df = pd.DataFrame(js)
        df = df[
            ['나트륨', '단백질', '만드는 법 1 이미지', '만드는 법 1', '만드는 법 2 이미지', '만드는 법 2', '만드는 법 3 이미지', '만드는 법 3', '만드는 법 4 이미지', '만드는 법 4', '만드는 법 5 이미지',
             '만드는 법 5',
             '만드는 법 6 이미지', '만드는 법 6', '만드는 법 7 이미지', '만드는 법 7', '만드는 법 8 이미지', '만드는 법 8', '만드는 법 9 이미지', '만드는 법 9', '만드는 법 10 이미지', '만드는 법 10',
             '만드는 법 11 이미지', '만드는 법 11', '만드는 법 12 이미지', '만드는 법 12', '만드는 법 13 이미지', '만드는 법 13', '만드는 법 14 이미지', '만드는 법 14', '만드는 법 15 이미지',
             '만드는 법 15',
             '만드는 법 16 이미지', '만드는 법 16', '만드는 법 17', '만드는 법 17 이미지', '만드는 법 18 이미지', '만드는 법 18', '만드는 법 19 이미지', '만드는 법 19', '만드는 법 20 이미지',
             '만드는 법 20',
             '썸네일', '열량', '요리명', '재료', '저감 조리법 TIP', '조리방법', '종류', '지방', '탄수화물', 'col_1', 'col_2', 'col_0', 'col_4']]

        pre_food_list = pd.read_excel('data\\pre_food_list.xlsx', index_col=0)

        for i, data in df.iterrows():
            if data["요리명"] in [pre_food_name[1] for pre_food_name in pre_food_list.itertuples()]:
                continue

            # 책 정보 및 링크 가져오기
            self.keyword = data["요리명"]
            self.category = CATEGORY[0]

            # -----------------------------------------------------------------------------
            # ChatGTP를 통한 글 제목과 content 저장
            self.writing.setting(data=data, category=self.category)
            try:
                self.title, self.content = self.writing.writeContent()

                if self.title == "" and self.content == "":
                    continue
            except Exception as e:
                print(e)
                continue
            # -----------------------------------------------------------------------------
            need_check = False
            wrong_keywords = ["마크다운", "블로그", "작성해드리겠습니다."]

            for wrong_keyword in wrong_keywords:
                if wrong_keyword in self.content:
                    need_check = True
                    break

            if need_check:
                # 잘못된 키워드 있을 시 체크 필요
                # 이미지들 삽입 전 메일로 확인
                # 설정
                user = GMAIL_ACCOUNT['email']
                password = GMAIL_ACCOUNT['password']
                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.ehlo()
                smtp.starttls()
                smtp.login(user, password)

                # 메일 보내기
                send_msg = MIMEText(self.content)
                send_msg['Subject'] = self.title
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
                total_continue = False
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
                    if str(subject).startswith(self.keyword) and str(subject).find("@") != -1:
                        # 0일 경우, 그냥 그대로 진행
                        # 1일 경우, 바뀐 본문 넣기
                        # 2일 경우, 그냥 스킵
                        choice = int(str(subject).split("@")[1])
                        body = ""
                        if choice == 0:
                            break
                        elif choice == 1:
                            # 메일 내용
                            self.title = str(subject).split("@")[0]

                            if email_message.is_multipart():
                                for part in email_message.walk():
                                    ctype = part.get_content_type()
                                    cdispo = str(part.get('Content-Disposition'))
                                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                                        body = part.get_payload(decode=True)  # decode
                                        break
                            else:
                                body = email_message.get_payload(decode=True)

                            body = body.decode('utf-8')
                            self.content = body
                            break
                        elif choice == 2:
                            total_continue = True
                            break
                    else:
                        continue

                if total_continue:
                    print("skip!")
                    continue

            # -----------------------------------------------------------------------------
            # 이미지 삽입
            # self._getGenericImages()
            self._recipeImageUpload()
            self._insertImage()

            # -----------------------------------------------------------------------------
            # 썸네일 만들기
            self._thumbnailCreate()

            # -----------------------------------------------------------------------------
            # 업로드
            self._upload()

            # -----------------------------------------------------------------------------
            # 이미 작성한 음식이라고 명시
            pre_food_list = pd.read_excel('data\\pre_food_list.xlsx', index_col=0)
            food_row = pd.DataFrame([{'요리명': data["요리명"]}])
            update_pre_book_list = pd.concat([pre_food_list, food_row], ignore_index=True)
            update_pre_book_list.to_excel('data\\pre_food_list.xlsx')


if __name__ == "__main__":
    try:
        main = Main()
        main.autoFoodExecute()
    except Exception as e:
        print(f"오류 발생: {e}")
