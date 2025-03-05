import os
import tkinter as tk
from PIL import Image, ImageTk
from PyQt5 import QtWidgets

from env.settings import IMAGE_PATH

TYPE_VIEW = "TYPE_VIEW"
TYPE_DELETE_CHOICE = "TYPE_DELETE_CHOICE"


class ImageViewer:
    def __init__(self, keyword, img_upload_func, type, le_image_num: QtWidgets.QLineEdit):
        self.img_upload_func = img_upload_func
        self.type = type
        self.le_image_num = le_image_num

        # 속성 설정
        self.window = tk.Tk()
        self.c_gallery = tk.Canvas(self.window, width=600, height=600)
        self.f_gallery = tk.Frame(self.window)
        self.img_path = IMAGE_PATH + "\\" + keyword
        self.images = os.listdir(self.img_path)
        self.remove_images = []

    def execute(self):
        # GUI 설정
        self.c_gallery.pack()

        # 스크롤바 생성
        scrollbar = tk.Scrollbar(self.window, command=self.c_gallery.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # 스크롤 영역과 스크롤바 연결
        self.c_gallery.configure(yscrollcommand=scrollbar.set)
        self.c_gallery.create_window((0, 0), window=self.f_gallery)
        self.c_gallery.bind_all("<MouseWheel>", self._on_mousewheel)
        self.f_gallery.bind("<Configure>", self._update_scroll_region)

        b_save = tk.Button(self.window, text="선택한 이미지 삭제하기", width=20, height=2, command=self._removeExecute)
        b_save.pack(pady=3)

        self._refreshGrid()

        self.window.mainloop()

    def _removeExecute(self):
        if self.type == TYPE_DELETE_CHOICE:
            for image in self.remove_images:
                image_path = os.path.join(self.img_path, image)
                os.remove(image_path)

            self.img_upload_func()
        self.le_image_num.setText(str(len(self.images) - len(self.remove_images)))
        self.window.destroy()

    def _refreshGrid(self):
        # 그리드 초기화
        for widget in self.f_gallery.winfo_children():
            widget.destroy()

        # 그리드에 이미지 표시
        for i, image in enumerate(self.images):
            image_path = os.path.join(self.img_path, image)

            try:
                # 이미지 열기
                img = Image.open(image_path)

                # 이미지 크기 조정
                img = img.resize((200, 200))

                # 이미지 표시
                photo = ImageTk.PhotoImage(img, master=self.window)
                label = tk.Label(self.f_gallery, image=photo)
                label.grid(row=i // 3, column=i % 3)

                if self.type == TYPE_DELETE_CHOICE:
                    check_button = tk.Checkbutton(
                        self.f_gallery,
                        width=3,
                        height=3,
                        command=lambda index=i: self._on_check_button_click(index)
                    )
                    check_button.grid(row=i // 3, column=i % 3)

                # PhotoImage 객체를 유지하기 위해 참조
                label.image = photo
            except Exception as e:
                print(str(e))
                print(f"Failed to open image: {image_path}")

    def _on_check_button_click(self, index):
        image = self.images[index]
        if image not in self.remove_images:
            self.remove_images.append(image)
        else:
            self.remove_images.remove(image)

    def _on_mousewheel(self, event):
        self.c_gallery.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_scroll_region(self, event):
        self.c_gallery.configure(scrollregion=self.c_gallery.bbox("all"))
