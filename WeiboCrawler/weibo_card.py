from bs4 import BeautifulSoup


class WeiboCard(object):
    def __init__(self, raw_json):
        # print(raw_json)
        self.raw_json = raw_json
        self.url = raw_json['scheme']
        raw_json_mblog = raw_json['mblog']
        self.mid = raw_json_mblog['mid']
        self.raw_create_time = raw_json_mblog['created_at']
        self.year, self.month, self.day = self.decode_create_time()
        self.rich_text = BeautifulSoup(raw_json_mblog['text'], 'html.parser')
        # print(self.rich_text)
        print(self.year, self.month, self.day)
        # print(self.is_needed())

    def decode_create_time(self):
        cr = self.raw_create_time.split(' ')
        year = cr[-1]
        month = cr[1]
        day = cr[2]
        return year, month, day

    def is_needed(self):
        tags = self.rich_text.findAll('span', attrs={'class': 'surl-text'})
        for tag in tags:
            if tag.string == '#d酱今天穿这个上班#':
                return True
        return False

    def get_dress_name(self):
        if not self.is_needed():
            return None
        brs = self.rich_text.findAll('br')
        dress_name = ''
        for sibling in brs[1].next_siblings:
            # print(sibling)
            if sibling not in brs:
                # 如果@了店家，这里会有一个<a></a>标签，需要把它解出来
                if isinstance(sibling, str):
                    dress_name += sibling
                else:
                    dress_name += sibling.string
            else:
                break
        # print(dress_name)
        return dress_name

    def get_pictures(self):
        if not self.is_needed():
            return None
        pics = self.raw_json['mblog']['pic_ids']
        # print(pics)
        if len(pics) >= 2:
            return ['https://wx3.sinaimg.cn/large/{}.jpg'.format(p) for p in pics[:2]]
        else:
            return ['https://wx3.sinaimg.cn/large/{}.jpg'.format(pics[0])]



