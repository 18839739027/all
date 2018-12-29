# -*- coding: utf-8 -*-
# @Time    : 2018/12/27  17:06
# @Author  : zhangxinxin
# 感谢小六，小勾， 小胖给予的帮助
# @Email   : 778786617@qq.com
# @Software: PyCharm
import csv
import requests
import time
import json
from lxml import etree

# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=3d144eda1ae5453e80e1debdea954230
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=1&s=1&click=0
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=60&click=0


class JdMessage(object):
    def __init__(self):
        self.js_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=7652027,5089253,5853579,100001172674,100000822981,7437780,7081550,7321794,100002338246,8895275,7694047,7421462,100000727128,5089275,5089267,8735304,7437564,100000503295,8514651,100000773889,7920226,100001906474,6735790,100000971366,7651931,100000982034,8790545,8051124,7479810,1861102&callback=jQuery3699627&_=1545911372294'
        # self.url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=1&s=1&click=0'
        self.url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=3d144eda1ae5453e80e1debdea954230'
        self.index_url = 'https://www.jd.com/'
        self.html = ''
        self.js_content = ''
        self.content_list = []
        self.headers = {
            # 'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=59&click=0',
            'scheme': 'https',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': '您的cookie'
        }

    def get_html(self):
        try:
            url = requests.get(self.url, headers=self.headers).content.decode(encoding='utf-8')
            # print(url)
            self.js_content = requests.get(self.js_url, headers=self.headers)

            self.html = etree.HTML(url)
        except Exception as e:
            print(e)

    def parse_html(self):
        p_name = self.html.xpath('//li/div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@title')
        # p_comment = self.html.xpath('//li/div[@class="gl-i-wrap"]/div[@class="p-commit"]/strong/a//text()')
        # 评论是js 加载的，不能说实时，但也是近几天的,在返回的源码里并没有评论数，所以需要再发一个js请求。
        p_price = self.html.xpath('//li/div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()')
        p_shop = self.html.xpath('//div[@class="p-shop"]/span/a/text()')
        self.js_content = self.js_content.text.split('(')[-1].split(')')[0]
        jd_json = json.loads(self.js_content)
        # print(jd_json['CommentsCount'])
        comment_list = []

        for data in jd_json['CommentsCount']:
            comment_list.append(data['CommentCountStr'])
        # print(comment_list)
        # print(p_name,  p_price, p_shop)
        # print(p_comment_num)
        # print(self.js_content)
        self.content_list = zip(p_name, p_price, comment_list, p_shop)

    def save_csv(self):
        with open('JD_phone.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['商品名', '价格', '评论数', '店铺名'])
        with open('JD_phone.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for x in self.content_list:
                writer.writerow(x)
            # 数据写入需要时间，程序结束过快会导致数据写入不全
            time.sleep(3)
            print('信息写入成功')

    def run(self):
        self.get_html()
        self.parse_html()
        self.save_csv()


if __name__ == '__main__':
    s = JdMessage()
    s.run()
