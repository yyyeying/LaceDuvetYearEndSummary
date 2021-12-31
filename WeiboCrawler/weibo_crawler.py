from typing import List

import requests
from WeiboCrawler.weibo_card import WeiboCard


class WeiboCrawler(object):
    def __init__(self, year: int = 2021):
        self.year = year
        self.duvet_uid = '1968464971'
        self.duvet_homepage = 'https://m.weibo.cn/u/{}'.format(self.duvet_uid)

    def get_homepage(self):
        response = requests.get(self.duvet_homepage)
        print(response.text)
        return response.text

    def get_one_page_weibo(self, since_id: int = 0):
        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {'type': 'uid',
                  'value': self.duvet_uid,
                  'containerid': '1076031968464971'}
        if since_id != 0:
            params['since_id'] = since_id
        response = requests.get(url=url,
                                params=params).json()
        weibo_card_list = []
        finished = False
        if response['ok'] == 1:
            weibo_raw_list = response['data']['cards']
            for weibo_raw_json in weibo_raw_list:
                weibo_card = WeiboCard(weibo_raw_json)
                if int(weibo_card.year) == self.year:
                    weibo_card_list.append(weibo_card)
                    finished = False
                else:
                    finished = True
        return weibo_card_list, finished

    def get_weibo_list(self) -> List[WeiboCard]:
        finished = False
        since_id = 0
        weibo_list = []
        while not finished:
            weibo_card_list, finished = self.get_one_page_weibo(since_id=since_id)
            weibo_list += weibo_card_list
            since_id = weibo_card_list[-1].mid
            # finished = True
        # print(len(weibo_list))
        return list(set(weibo_list))


if __name__ == '__main__':
    crawler = WeiboCrawler()
    crawler.get_weibo_list()
