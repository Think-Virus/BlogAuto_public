# **Automated Tistory Blogging with ChatGPT & Selenium**

## ⚠️ **Project Status (Important)**

> ⚠️ **This project was last updated two years ago and may no longer function as expected.**  
> Due to recent **changes in the ChatGPT interface and the Tistory API**, some features may be broken.  
> Before running the project, **review and update the code as needed to match current environments.**

## 🚀 **Why This Project Was Made Public**  
This project was originally developed in the private GitHub repository `BlogAuto`.  
However, due to poor Git practices at the time, **sensitive personal information (e.g., login credentials) was committed** to the repository.  
For security reasons, the original repository could not be made public.

A **new public version was created with all personal information removed**,  
preserving the core functionalities and shared as part of a portfolio.

## 📌 **Project Overview**

This project uses **Python Selenium** to **utilize ChatGPT without an API**,  
and **automatically uploads blog posts to Tistory**.  
Initially, it included a GUI for reviewing posts before uploading,  
but later evolved into a fully automated system that **uploads posts after email approval**.

<p align="center">
  <img src="https://github.com/user-attachments/assets/324e9b3c-adda-40be-9707-df4f005a6e14" height="500" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/user-attachments/assets/b0e84a2f-c242-4588-b961-1f1d6eb41b19" height="500" />
</p>

---

## ✨ **Key Features**

### 📖 **Automatic Book Summarization and Review**
✅ Automatically generates **book summaries and reviews using ChatGPT**  
✅ Writes posts in **Markdown format**  
✅ Enhances content with data from sources like **Namuwiki**  
✅ **Recommends and inserts images** with ChatGPT  
✅ **Generates thumbnails automatically**

### 🍳 **Automatic Recipe Post Generation**
✅ Generates **recipes and cooking instructions automatically**  
✅ **Crawls relevant images** and attaches them to posts  

### 📷 **Image Crawling and Uploading**
✅ **Crawls commercially usable images from Google**  
✅ **Uploads images to Tistory using its API**  
✅ **Automatically switches accounts when API upload limits are reached**

### 📨 **Email Review Before Upload**
✅ Sends generated posts to your email  
✅ Automatically uploads the post once approved  

---

## 🔧 **Installation & Execution**

### 1️⃣ **Install Required Libraries**

```bash
pip install -r requirements.txt
```

### 2️⃣ **Set Up Chrome WebDriver**
- Automatically installed via `webdriver_manager`  
- Or download manually and add it to your system path  

### 3️⃣ **Set Environment Variables**
- Add your API keys and credentials in `env/settings.py`  

### 4️⃣ **Run the Program**

Generate a book review post:
```bash
python main_book.py
```

Generate and upload a recipe post:
```bash
python main_food.py
```

---

## 📂 **Project Directory Structure**

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
│── venv  (Virtual Environment)
│
└── .gitignore
```

### 📜 **File Descriptions**

📜 **Main Modules**  
- `main_book.py`: Auto-generate and upload book-related posts  
- `main_food.py`: Auto-generate and upload recipe-related posts  

📜 **Image Handling**  
- `image_crawler.py`: Crawl images from Google  
- `image_uploader.py`: Upload images to Tistory  
- `image_uploader_food.py`: Upload food-related images  

📜 **Automation & Content Writing**  
- `writing.py`: Write blog content with ChatGPT  
- `writing_food.py`: Write cooking content  
- `uploader.py`: Tistory blog post management  
- `uploader_food.py`: Food-specific blog management  

📜 **Utilities**  
- `utils.py`: Common helper functions  

---

## ⚙️ **Environment Configuration (`settings.py`)**

Before running the program, create the file `env/settings.py` and configure the following:

### 1️⃣ Tistory Account Info
```python
T_STORY_ACCOUNT_LIST = {
    'example_user': ['example@gmail.com', 'password', 'client_id', 'client_secret'],
    'another_user': ['another@gmail.com', 'password', 'client_id', 'client_secret']
}
```

### 2️⃣ ChatGPT Account
```python
CHAT_GPT_ACCOUNT = {
    'email': 'your_chatgpt_email@gmail.com',
    'password': 'your_chatgpt_password',
}
```

### 3️⃣ Gmail Account for Email Review
```python
GMAIL_ACCOUNT = {
    'email': 'your_gmail@gmail.com',
    'password': 'your_gmail_app_password',
}
```

### 4️⃣ Blog URL & Access Token
```python
BLOG_URL = 'https://your-blog.tistory.com/'
ACCESS_TOKEN = 'your_tistory_api_access_token'
```

### 5️⃣ Post Categories
```python
FOOD_ID = 1234567
BOOK_ID = 8910111

CATEGORY = ["FOOD", "BOOK"]
```

### 6️⃣ Image Settings
```python
IMAGE_PATH = './images'
GENERIC_IMAGE_DICT = {'Sunset': ['image_url_1', 'image_url_2']}
```

✅ After setting up `env/settings.py`, you're ready to run the project.

---

## 🔥 **Future Improvements**
✅ **Code Refactoring**  
- Clean up and separate functionality into modules  
- Remove duplicate code and improve maintainability  

✅ **Remove Deprecated GUI Code**  
- Early GUI logic is still present but no longer needed due to full automation  
