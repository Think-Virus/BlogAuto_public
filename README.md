# **ChatGPT & Selenium을 활용한 티스토리 자동 블로깅**

## ⚠️ **프로젝트 상태 (중요)**

> ⚠️ **이 프로젝트는 2년 전에 마지막으로 업데이트되었으며, 현재 정상적으로 동작하지 않을 가능성이 있습니다.**  
> 최근 **ChatGPT 인터페이스 및 티스토리 API 변경**으로 인해 일부 기능이 작동하지 않을 수 있습니다.  
> 프로젝트 실행 전, **코드를 검토하고 최신 환경에 맞게 수정하는 것이 필요합니다.**

## 🚀 **이 프로젝트를 공개한 이유**  
이 프로젝트는 원래 **GitHub 저장소** `BlogAuto`에서 개발되었으며, 개발 과정에서 여러 번 커밋되었습니다.  
그러나 당시 Git을 올바르게 사용하지 못해, **민감한 개인 정보(ID, 비밀번호)가 포함된 상태로 커밋**되어  
보안상의 이유로 원본 저장소를 공개할 수 없었습니다.  

이에 따라 **개인 정보가 제거된 별도의 공개 저장소를 생성**하여,  
프로젝트의 핵심 기능을 유지한 채 포트폴리오 용도로 공유하게 되었습니다.  

## 📌 **프로젝트 개요**

이 프로젝트는 **Python Selenium**을 활용하여 **API 없이 무료로 ChatGPT를 이용**하고,  
**티스토리 블로그에 게시글을 자동으로 업로드하는 기능**을 제공합니다.  
초기에는 GUI를 통해 게시글을 검토한 후 업로드하는 방식이었지만,  
이후 자동화를 도입하여 **이메일 검토 후 자동 업로드가 가능하도록 개선**되었습니다.  

<p align="center">
  <img src="https://github.com/user-attachments/assets/324e9b3c-adda-40be-9707-df4f005a6e14" height="500" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/user-attachments/assets/b0e84a2f-c242-4588-b961-1f1d6eb41b19" height="500" />
</p>

---

## ✨ **핵심 기능**
### 📖 **자동 책 요약 및 리뷰 생성**
✅ ChatGPT를 이용하여 **책 요약 및 리뷰 자동 생성**  
✅ **Markdown 형식으로 블로그 게시글 작성**  
✅ 나무위키 등의 소스를 분석하여 **내용 보완**  
✅ ChatGPT를 활용하여 **적절한 이미지 추천 및 삽입**  
✅ **자동 썸네일 생성**  

### 🍳 **자동 요리 레시피 작성**
✅ **요리 레시피 및 조리법 자동 생성**  
✅ **관련 이미지를 크롤링하여 자동 첨부**  

### 📷 **이미지 크롤링 및 업로드**
✅ **구글에서 상업적으로 사용 가능한 이미지 크롤링**  
✅ **티스토리 API를 이용해 이미지 자동 업로드**  
✅ **API 업로드 제한 시 자동 계정 전환**  

### 📨 **이메일 검토 후 업로드**
✅ ChatGPT가 생성한 게시글을 이메일로 전송  
✅ 사용자가 승인하면 자동으로 게시  

---

## 🔧 **설치 및 실행 방법**

### 1️⃣ **필수 라이브러리 설치**

```bash
pip install -r requirements.txt
```

### 2️⃣ **Chrome WebDriver 설정**
- `webdriver_manager`를 사용하여 자동 설치  
- 또는 ChromeDriver를 직접 다운로드하여 실행 환경에 추가  

### 3️⃣ **환경 변수 설정**
- `env/settings.py` 파일에 API 키 및 계정 정보 설정  

### 4️⃣ **프로그램 실행**
책 리뷰 블로그 게시글 자동 생성:

```bash
python main_book.py
```

요리 레시피 블로그 게시글 자동 생성 및 업로드:

```bash
python main_food.py
```

---

## 📂 **프로젝트 폴더 구조**

```
/project-root
│── src
│   │── main
│   │   │── book
│   │   │   ├── MainBook.py
│   │   │   └── WritingBook.py
│   │   │
│   │   │── food
│   │   │   ├── MainFood.py
│   │   │   ├── WritingFood.py
│   │   │   └── ImageUploaderFood.py
│   │   │
│   │   │── image
│   │   │   ├── ImageChoice.py
│   │   │   ├── ImageCrawler.py
│   │   │   ├── ImageUploader.py
│   │   │   └── ImageUploaderFood.py
│   │   │
│   │   │── network
│   │   │   ├── Uploader.py
│   │   │   └── UploaderFood.py
│   │   │
│   │   │── utils
│   │   │   ├── Utils.py
│   │   │   ├── SkipBook.txt
│   │   │   └── Test.txt
│
│── env
│   ├── settings.py
│
│── venv  (가상 환경)
│
└── .gitignore

```

### 📜 **파일 설명**
📜 **주요 모듈**  
- `main_book.py` : **책 관련 블로그 게시글 자동 생성 및 업로드**  
- `main_food.py` : **요리 레시피 블로그 게시글 자동 생성 및 업로드**  

📜 **이미지 처리**  
- `image_crawler.py` : **구글에서 이미지 크롤링**  
- `image_uploader.py` : **크롤링한 이미지를 티스토리에 업로드**  
- `image_uploader_food.py` : **요리 관련 이미지를 업로드**  

📜 **자동화 및 글 작성**  
- `writing.py` : **ChatGPT를 활용한 자동 글 작성**  
- `writing_food.py` : **요리 관련 자동 글 작성**  
- `uploader.py` : **티스토리 블로그 업로드 관리**  
- `uploader_food.py` : **요리 관련 블로그 업로드 관리**  

📜 **유틸리티**  
- `utils.py` : **공통 기능 처리**  

---

## ⚙️ **환경 설정 (`settings.py`)**
프로그램 실행 전에 `env/settings.py` 파일을 생성하고 다음과 같이 설정합니다.  

### **1️⃣ 티스토리 계정 정보**
```python
T_STORY_ACCOUNT_LIST = {
    'example_user': ['example@gmail.com', 'password', 'client_id', 'client_secret'],
    'another_user': ['another@gmail.com', 'password', 'client_id', 'client_secret']
}
```
💡 설명  
- `T_STORY_ACCOUNT_LIST` : 여러 티스토리 계정 정보를 저장  
- `'example_user'`, `'another_user'` : 계정 ID  
- 리스트 내부: `[이메일, 비밀번호, CLIENT_ID, CLIENT_SECRET]`

### **2️⃣ ChatGPT 계정 설정**
```python
CHAT_GPT_ACCOUNT = {
    'email': 'your_chatgpt_email@gmail.com',
    'password': 'your_chatgpt_password',
}
```
💡 설명  
- `email` : ChatGPT 계정 이메일  
- `password` : ChatGPT 계정 비밀번호  

### **3️⃣ 이메일 검토용 Gmail 계정**
```python
GMAIL_ACCOUNT = {
    'email': 'your_gmail@gmail.com',
    'password': 'your_gmail_app_password',
}
```
💡 설명  
- `email` : 이메일 검토용 Gmail 계정  
- `password` : Gmail 앱 비밀번호  

### **4️⃣ 티스토리 블로그 및 API 설정**
```python
BLOG_URL = 'https://your-blog.tistory.com/'
ACCESS_TOKEN = 'your_tistory_api_access_token'
```
💡 설명  
- `BLOG_URL` : 블로그 URL  
- `ACCESS_TOKEN` : 티스토리 API 액세스 토큰  

### **5️⃣ 블로그 게시글 카테고리**
```python
FOOD_ID = 1234567
BOOK_ID = 8910111

CATEGORY = ["FOOD", "BOOK"]
```
💡 설명  
- `FOOD_ID`, `BOOK_ID` : 블로그 카테고리 ID  
- `CATEGORY` : 카테고리 리스트  

### **6️⃣ 이미지 저장 경로 및 기본 설정**
```python
IMAGE_PATH = './images'
GENERIC_IMAGE_DICT = {'Sunset': ['image_url_1', 'image_url_2']}
```
💡 설명  
- `IMAGE_PATH` : 이미지 저장 경로  
- `GENERIC_IMAGE_DICT` : 특정 키워드와 연결된 이미지 URL 목록  

✅ 위 설정을 `env/settings.py`에 저장한 후 프로그램을 실행할 수 있습니다.

---

## 🔥 **향후 개선 사항**
✅ **코드 리팩토링**  
- 여러 기능이 한 파일에 섞여 있음 → 모듈별로 분리하여 유지보수성 향상  
- 중복 코드 제거 및 기능별 통합  

✅ **불필요한 UI 관련 코드 제거**  
- 초기 GUI 코드가 남아 있으나, 현재는 완전 자동화되어 필요 없음