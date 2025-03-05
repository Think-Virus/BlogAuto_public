import os
import re
import requests
from tistory import Tistory

from env.settings import IMAGE_PATH, ACCESS_TOKEN, BLOG_URL


class ImageUploader:
    def __init__(self, keyword, tistory: Tistory, is_thumbnail=False):
        self.keyword = keyword
        self.keyword_path = IMAGE_PATH + "/" + keyword
        # self.tistory = tistory #원래는 이게 맞으나, 잠시 이미지 제한 걸려서 다른 걸로 대체
        self.tistory = Tistory("https://small-think3.tistory.com/", "31faf3e5bc7ffb5db4c033f04108f58f", "31faf3e5bc7ffb5db4c033f04108f58f43b603193c9ba957684a99e32f2fd1f6fb296ad9")
        self.is_thumbnail = is_thumbnail

    def upload(self):
        invalid_chars = r'[\\/:*?"<>|]'

        thumbnail_path =os.path.join(IMAGE_PATH, re.sub(invalid_chars, '', self.keyword) + "_thumbnail.png")
        if not self.is_thumbnail:
            # 일반 이미지들
            img_addresses = []

            for filename in os.listdir(self.keyword_path):
                file_path = os.path.join(self.keyword_path, filename)
                img_address = self._getImgAddress(file_path)
                if img_address and img_address != thumbnail_path:
                    img_addresses.append(img_address)
            return img_addresses
        else:
            # 썸네일
            return self._getImgAddress(thumbnail_path)

    def _getImgAddress(self, file_path):
        files = {'uploadedfile': open(file_path, 'rb')}
        # params = {'access_token': ACCESS_TOKEN, 'blogName': self.tistory.blog_name, 'targetUrl': BLOG_URL, 'output': 'json'}
        params = {'access_token': "c6caab52bc234bd5e93e37be2a0cae7a_29a1163b5a1f34116cf3974faf09edec", 'blogName': self.tistory.blog_name, 'targetUrl': "https://small-think3.tistory.com", 'output': 'json'}
        res_upload = requests.post('https://www.tistory.com/apis/post/attach', params=params, files=files)

        replacer = res_upload.json()['tistory']['replacer']

        if self.is_thumbnail:
            img_address = replacer
        else:
            pattern = r'@(\w+/[\w./]+)'
            match = re.search(pattern, replacer)
            img_address = "https://blog.kakaocdn.net/dn/" + match.group(1)
        return img_address
