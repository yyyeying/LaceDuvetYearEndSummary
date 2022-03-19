from typing import List

from WeiboCrawler.weibo_crawler import WeiboCrawler
from WeiboCrawler.weibo_card import WeiboCard
from ImageGenerator.image_generate_weibo import ImageGeneratorWeibo

if __name__ == '__main__':
    crawler = WeiboCrawler()
    weibo_list: List[WeiboCard] = crawler.get_weibo_list()
    generator = ImageGeneratorWeibo(weibo_list, page_num=26)
    generator.generate()
