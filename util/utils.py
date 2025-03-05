import random
import mistune
from PIL import Image, ImageDraw, ImageFont

YELLOW = (251, 216, 93)
GREEN = (204, 238, 188)
PURPLE = (150, 129, 235)
ORANGE = (255, 214, 165)
COLOR_LIST = [YELLOW, GREEN, PURPLE, ORANGE]


def markdown2html(markdonw, thumbnail_img):
    html = mistune.markdown(markdonw)
    html = html \
        .replace('&lt;', '<') \
        .replace('&gt;', '>') \
        .replace('&quot;', '"') \
        .replace('<p><div class="auto-image-container">', '<div class="auto-image-container">') \
        .replace('</div></p>', '</div>') \
        .replace('<hr />', '<hr data-ke-style="style1" />')

    html = thumbnail_img + "\n" + html

    return html


def create_image(message: str):
    # 9글자가 넘어가면 이미지를 넘어감으로 줄바꿈 필요
    if len(message.replace(" ", "")) > 8:
        word_list = message.split(" ")
        message = ""
        group_len = 0
        for word in word_list:
            if group_len + len(word) > 8:
                message += "\n" + word
                group_len = 0
            else:
                message += " " + word
                group_len += len(word)

    message = message.strip()

    size = (1280, 720)
    W, H = size
    font = ImageFont.truetype("UI/font/TTTogether.ttf", 120)
    image = Image.new('RGB', size, COLOR_LIST[random.randrange(0, 4)])
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), message, font=font, fill='black')
    return image
