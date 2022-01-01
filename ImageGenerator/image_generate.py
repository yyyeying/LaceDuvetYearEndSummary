from typing import List
import os
import requests
from PIL import Image, ImageDraw, ImageFont

from WeiboCrawler.weibo_card import WeiboCard


def dounload_image(url: str, dest: str):
    print('Downloading: {}'.format(url))
    response = requests.get(url)
    if response.status_code == 200:
        open(dest, 'wb').write(response.content)


class ImageGenerator(object):
    def __init__(self, weibo_list: List[WeiboCard], page_num: int = 9):
        self.single_height = 1080
        self.single_width = int(self.single_height * 3 / 4)
        self.rim = 20
        self.font_size = 36
        self.weibo_list = sorted(weibo_list, key=lambda x: x.get_dress_name())
        self.page_num = page_num
        self.pics_per_page = int(len(self.weibo_list) / page_num) + 1
        self.cache_path = os.path.join(os.getcwd(), 'image_cache')

    def generate(self):
        pic_width = self.single_width * 2 + 3 * self.rim
        pic_height = (self.single_height + 2 * self.rim + 2*self.font_size) * self.pics_per_page
        print(pic_width, pic_height)
        for page in range(self.page_num):
            image = Image.new(mode='RGB',
                              size=(pic_width, pic_height),
                              color=(255, 255, 255))
            for i in range(page * self.pics_per_page, (page + 1) * self.pics_per_page):
                try:
                    self.generate_single(i)
                    single_image = Image.open(os.path.join(self.cache_path,
                                                           '{}_{}.jpg'.format(
                                                               self.weibo_list[i].get_dress_name().replace('/', ', '),
                                                               'single')))
                    box = (0,
                           (self.single_height + 2 * self.rim + 2*self.font_size) * (i - page * self.pics_per_page),
                           pic_width,
                           (self.single_height + 2 * self.rim + 2*self.font_size) * (i - page * self.pics_per_page + 1))
                    print(box)
                    image.paste(im=single_image,
                                box=box)
                except IndexError:
                    print('Generate finished.')
                    break
            image.save(os.path.join(os.getcwd(),
                                    'full_{}.jpg'.format(page)),
                       quality=100)

    def generate_single(self, num: int):
        weibo: WeiboCard = self.weibo_list[num]
        pic_num = 1
        print('generate single dress: {} {} {}'.format(weibo.get_dress_name(), weibo.month, weibo.day))
        target = Image.new(mode='RGB',
                           size=(self.single_width * 2 + 3 * self.rim,
                                 self.single_height + 2 * self.rim + 2*self.font_size),
                           color=(255, 255, 255))
        for image_url in weibo.get_pictures():
            if not os.path.exists(self.cache_path):
                os.mkdir(self.cache_path)
            dounload_image(url=image_url,
                           dest=os.path.join(self.cache_path,
                                             '{}_{}.jpg'.format(weibo.get_dress_name().replace('/', ', '),
                                                                pic_num)))
            image = Image.open(os.path.join(self.cache_path,
                                            '{}_{}.jpg'.format(weibo.get_dress_name().replace('/', ', '),
                                                               pic_num)))
            w, h = image.size
            # 裁剪为 3:4
            if w / h < 0.75:
                box = (0, int(h / 2 - w * 2 / 3), w, int(h / 2 + w * 2 / 3))
            else:
                box = (int(w / 2 - h * 3 / 8), 0, int(w / 2 + h * 3 / 8), h)
            image = image.crop(box)
            image = image.resize((self.single_width, self.single_height), Image.ANTIALIAS)
            if pic_num == 1:
                target.paste(im=image,
                             box=(self.rim,
                                  self.rim,
                                  self.rim + self.single_width,
                                  self.rim + self.single_height))
            else:
                target.paste(im=image,
                             box=(2 * self.rim + self.single_width,
                                  self.rim,
                                  2 * self.rim + 2 * self.single_width,
                                  self.rim + self.single_height))
            draw = ImageDraw.Draw(target)
            draw.text(xy=(self.rim * 2, self.single_height),
                      text=weibo.get_dress_name(),
                      font=ImageFont.truetype(os.path.join(os.getcwd(), 'SourceHanSerifCN-Light.otf'), self.font_size),
                      fill=(0, 0, 0))
            draw.text(xy=(self.rim * 2, self.single_height + self.font_size),
                      text='{} {} {}'.format(weibo.year, weibo.month, weibo.day),
                      font=ImageFont.truetype(os.path.join(os.getcwd(), 'SourceHanSerifCN-Light.otf'), self.font_size),
                      fill=(0, 0, 0))
            pic_num += 1
        target.save(os.path.join(self.cache_path,
                                 '{}_{}.jpg'.format(weibo.get_dress_name().replace('/', ', '),
                                                    'single')),
                    quality=100)
