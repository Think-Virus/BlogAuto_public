import email
import imaplib
import random
import re
import smtplib
import sys
import tkinter as tk
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from time import sleep

import pandas as pd
from PyQt5 import QtWidgets
from UI.UI import UiMainWindow
from tistory import Tistory
from tkhtmlview import HTMLLabel

import image_choice
import image_crawler
import image_uploader
import uploader
import writing
import util.utils
from env.settings import ACCESS_TOKEN, BLOG_URL, IMAGE_HTML_START, IMAGE_HTML_IMG, IMAGE_HTML_END, JUST_CHECK_GUI, CATEGORY, \
    GENERIC_IMAGE_DICT, T_STORY_ACCOUNT_LIST, GMAIL_ACCOUNT
from util.utils import markdown2html


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
            self.writing = writing.Writing()

        # UI와 관련된 속성들
        self.ui = None

        # 기타 설정
        self.tistory.access_token = ACCESS_TOKEN
        self.uploader = uploader.Uploader(self.NOW_ACCOUNT)

    def runGUI(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = UiMainWindow(MainWindow,
                               self.writingExecute,
                               self._createHTML,
                               self._upload,
                               self._scaling,
                               self._imgProcess,
                               self._imgDeleteChoice,
                               self._imgView,
                               self._imgUpload,
                               self._thumbnailCreate,
                               self._onKeywordChange,
                               self._onCategoryChange,
                               self._onTitleChange,
                               self._onContentChange)
        self.ui.setupUi()

        sys._excepthook = sys.excepthook
        sys.excepthook = self.ui.my_exception_hook

        MainWindow.show()
        sys.exit(app.exec_())

    def writingExecute(self):
        # ChatGTP를 통한 글 제목과 content 저장
        self.writing.setting(keyword=self.keyword, category=self.category)
        self.title, self.content = self.writing.writeContent()

        self.ui.le_title.setText(self.title)
        self.ui.pte_content.setPlainText(self.content)

    def _imgProcess(self):
        imageCrawler = image_crawler.ImageCrawler(keyword=self.keyword,
                                                  search_keyword=self.ui.le_search_keyword.text(),
                                                  maxImages=int(self.ui.le_search_max.text()) if self.ui.le_search_max.text() else 10)
        imageCrawler.crawling()
        imageCrawler.driver.close()
        self._imgDeleteChoice()

    def _scaling(self):
        imageCrawler = image_crawler.ImageCrawler(keyword=self.keyword, search_keyword=self.ui.le_search_keyword.text())
        imageCrawler._scaling(image_crawler.TYPE_ALL)

    def _imgDeleteChoice(self):
        # 이미지 선택
        image_choice.ImageViewer(self.keyword, self._imgUpload, image_choice.TYPE_DELETE_CHOICE, self.ui.le_image_num).execute()

    def _imgView(self):
        # 이미지 선택
        image_choice.ImageViewer(self.keyword, self._imgUpload, image_choice.TYPE_VIEW, self.ui.le_image_num).execute()

    def _imgUpload(self):
        # 이미지 업로드
        imageUploader = image_uploader.ImageUploader(keyword=self.keyword, tistory=self.tistory)
        self.img_addresses = imageUploader.upload()

    def _createHTML(self):
        tmp_save_img_addresses = self.img_addresses

        # 최종 형태 표시
        root = tk.Tk()
        root.title("HTML Viewer")
        hl_final_content = HTMLLabel(root)
        hl_final_content.pack(expand=True, fill='both')

        # 업로드한 이미지 주소로 적절한 위치에 이미지들 삽입
        self._insertImage()

        # content html로 변환
        self.html_code = markdown2html(self.content, self.thumbnail_img)
        hl_final_content.set_html(self.html_code)

        self.img_addresses = tmp_save_img_addresses

        root.mainloop()

    def _insertImage(self):
        lines = self.content.split("\n")
        new_lines = []

        for line in lines:
            new_lines.append(line)
            if line.startswith("<h1>"):
                sub_title_line = new_lines.pop(-1)
                new_lines.append(self._getImageHTML())
                new_lines.append(sub_title_line)

        new_lines.append(self._getImageHTML())
        self.content = "\n".join(new_lines)

    # 이미지 개수에 따른 HTML 코드 작성
    def _getImageHTML(self):
        num_img_addresses = len(self.img_addresses)

        if num_img_addresses == 0:
            return ""

        return_html = IMAGE_HTML_START
        for i in range(0, num_img_addresses):
            # 마지막이 아닐 경우, 최대 3개로 제한
            if i == 3:
                break

            return_html += IMAGE_HTML_IMG.format(self.img_addresses.pop(0), i)
        return_html += IMAGE_HTML_END
        return return_html

    def _upload(self):
        self.uploader.update(self.title, self.content, self.category, self.thumbnail_img)
        if not self.uploader.customUpload():
            self.NOW_ACCOUNT_INDEX += 1
            self.NOW_ACCOUNT = T_STORY_ACCOUNT_LIST[self.ACCOUNT_LIST_KEY[self.NOW_ACCOUNT_INDEX]]
            self.uploader = uploader.Uploader(self.NOW_ACCOUNT)
            sleep(3)
            self._upload()

    def _thumbnailCreate(self):
        invalid_chars = r'[\\/:*?"<>|]'
        thumbnail = util.utils.create_image(self.keyword)
        thumbnail.save('images/{0}.png'.format(re.sub(invalid_chars, '', self.keyword) + "_thumbnail"), "PNG")

        # 썸네일 이미지 업로드
        imageUploader = image_uploader.ImageUploader(keyword=re.sub(invalid_chars, '', self.keyword), tistory=self.tistory, is_thumbnail=True)
        self.thumbnail_img = imageUploader.upload()

    def _getGenericImages(self):
        for subject in self.writing.image_subjects:
            self.img_addresses += random.sample(GENERIC_IMAGE_DICT[subject], 10)
        random.shuffle(self.img_addresses)

    def _onKeywordChange(self):
        self.keyword = self.ui.le_keyword.text()
        self.ui.le_search_keyword.setText(self.keyword)

    def _onCategoryChange(self, category):
        self.category = category

    def _onTitleChange(self):
        self.title = self.ui.le_title.text()

    def _onContentChange(self):
        self.content = self.ui.pte_content.toPlainText()

    def autoBookExecute(self):
        # 자동으로 책에 대한 내용들 적도록 해야겠다.
        book_list = pd.read_excel('data\\book_list.xlsx', index_col='index')
        pre_book_list = pd.read_excel('data\\pre_book_list.xlsx', index_col=0)

        for book in book_list.itertuples():
            if book[1] in [pre_book_name[1] for pre_book_name in pre_book_list.itertuples()]:
                continue

            # 책 정보 및 링크 가져오기
            book_name = str(book[1])
            book_link = book[2]
            self.keyword = book_name
            self.category = CATEGORY[1]

            # -----------------------------------------------------------------------------
            # ChatGTP를 통한 글 제목과 content 저장
            self.writing.setting(keyword=self.keyword, category=self.category)
            try:
                self.title, self.content = self.writing.writeContent(isAuto=True, namuwiki_url=book_link)

                if self.title == "" and self.content == "":
                    user = GMAIL_ACCOUNT['email']
                    password = GMAIL_ACCOUNT['password']
                    smtp = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(user, password)

                    # 메일 보내기
                    send_msg = MIMEText("스킵됨!")
                    send_msg['Subject'] = book_name + " 스킵됨!"
                    smtp.sendmail(user, user, send_msg.as_string())
                    smtp.quit()
                    continue
            except Exception as e:
                print(e)
                continue
            # -----------------------------------------------------------------------------
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
            self._getGenericImages()
            self._insertImage()

            # -----------------------------------------------------------------------------
            # 썸네일 만들기
            self._thumbnailCreate()

            # -----------------------------------------------------------------------------
            # 업로드
            self._upload()

            # -----------------------------------------------------------------------------
            # 이미 작성한 책이라고 명시
            # 이미 작성한 책이라고 명시
            pre_book_list = pd.read_excel('data\\pre_book_list.xlsx', index_col=0)
            book_row = pd.DataFrame([{'책 이름': book_name, '나무위키 링크': book_link, '존재': 1}])
            update_pre_book_list = pd.concat([pre_book_list, book_row], ignore_index=True)
            update_pre_book_list.to_excel('data\\pre_book_list.xlsx')


if __name__ == "__main__":
    # tmp_count = 0
    # while True:
    #     tmp_count += 1
    #     try:
    #         if tmp_count == 10:
    #             break
    #         main = Main()
    #         # main.runGUI()
    #         main.autoBookExecute()
    #     except Exception as e:
    #         print(f"오류 발생: {e}")
    #         print("잠시 후에 다시 실행합니다.")
    #         sleep(5)  # 5초 후에 재실행
    #     else:
    #         print("프로그램이 정상적으로 종료되었습니다.")
    #         sys.exit(0)  # 정상적인 종료
    try:
        main = Main()
        main.autoBookExecute()
    except Exception as e:
        print(f"오류 발생: {e}")
