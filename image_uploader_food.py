import os
import re

import requests
from tistory import Tistory


class ImageUploaderFood:
    def __init__(self, keyword, tistory: Tistory, is_thumbnail=False):
        self.keyword = keyword
        self.keyword_path = "./images/food_data/" + keyword + "/"
        # self.tistory = tistory #원래는 이게 맞으나, 잠시 이미지 제한 걸려서 다른 걸로 대체
        self.tistory = Tistory("https://small-think3.tistory.com/", "31faf3e5bc7ffb5db4c033f04108f58f",
                               "31faf3e5bc7ffb5db4c033f04108f58f43b603193c9ba957684a99e32f2fd1f6fb296ad9")
        self.is_thumbnail = is_thumbnail

    def upload(self):
        thumbnail_path = os.path.join(self.keyword_path + "썸네일.png")
        if not self.is_thumbnail:
            # 일반 이미지들
            img_addresses = []

            for filename in [file for file in os.listdir(self.keyword_path) if file != "썸네일.png"]:
                file_path = os.path.join(self.keyword_path, filename)
                img_address = self._getImgAddress(file_path)
                if img_address and img_address != thumbnail_path:
                    img_addresses.append(img_address)
            return img_addresses
        else:
            # 썸네일
            return self._getImgAddress(thumbnail_path).replace('"style":"alignCenter"', '"style":"alignCenter","alt":"썸네일"')

    def _getImgAddress(self, file_path):
        files = {'uploadedfile': open(file_path, 'rb')}
        # params = {'access_token': ACCESS_TOKEN, 'blogName': self.tistory.blog_name, 'targetUrl': BLOG_URL, 'output': 'json'}
        params = {'access_token': "0ef067b616ecae7e117530fd08030855_93b49a88751d3056da93fc1aa3d1add8", 'blogName': self.tistory.blog_name,
                  'targetUrl': "https://small-think3.tistory.com", 'output': 'json'}
        res_upload = requests.post('https://www.tistory.com/apis/post/attach', params=params, files=files)

        replacer = res_upload.json()['tistory']['replacer']

        if self.is_thumbnail:
            img_address = str(replacer).replace("|||_##]", 'alt="{0} 썸네일"|||_##]'.format(self.keyword))
        else:
            pattern = r'@(\w+/[\w./]+)'
            match = re.search(pattern, replacer)
            img_address = "https://blog.kakaocdn.net/dn/" + match.group(1)
        return img_address
