from typing import List

from WeiboCrawler.weibo_crawler import WeiboCrawler
from WeiboCrawler.weibo_card import WeiboCard

if __name__ == '__main__':
    crawler = WeiboCrawler()
    weibo_list: List[WeiboCard] = crawler.get_weibo_list()
    for weibo in weibo_list:
        if weibo.is_needed():
            picture_list = weibo.get_pictures()
            print(weibo.get_dress_name(), picture_list)
