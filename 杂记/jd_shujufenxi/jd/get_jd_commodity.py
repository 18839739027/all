# -*- coding: utf-8 -*-
# @Time    : 2019/1/5  15:48
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
import requests
import pymysql
from lxml import etree


class JdShop(object):
    """爬取京东商品列表页，并存储至数据库"""
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.url = 'https://search.jd.com/Search?keyword=phone&enc=utf-8&wq=phone&pvid=17a946bf54304714a28ab2c02504d782'
        self.html = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }

    def get_html(self):
        try:
            content = requests.get(self.url, headers=self.headers).content.decode(encoding='UTF-8')
            # print(content)
            self.html = etree.HTML(content)
        except Exception as e:
            print(e)

    def parse_html(self):
        id = self.html.xpath('//ul[@data-tpl="3"]/li/@data-pid')
        s_name = self.html.xpath('//ul[@data-tpl="3"]/li/div/div[@class="p-name p-name-type-2"]/a/em/text()')
        s_price = self.html.xpath('//ul[@data-tpl="3"]/li/div/div[@class="p-price"]/strong/i/text()')
        # image = self.html.xpath('//ul[@data-tpl="3"]/li/div/div[@class="p-img"]/a/img/@src')
        # 图片是js加载的
        print(id, s_price, s_name)
        data = zip(id, s_name, s_price)
        return data

    def connect_sql(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3309,
            user='root',
            password='123456',
            db='jd_comments'
        )
        self.cursor = self.conn.cursor()

    def close_sql(self):
        self.cursor.close()
        self.conn.close()

    def save_sql(self, data):
        self.connect_sql()
        for i in data:
            assert i is not None, '数据不能为空。'
            # print(i)
            # print(type(i[0]), type(i[1]), type(i[2]))
            sql = "INSERT INTO jd_comments.jd_commodity VALUES ('{}', '{}', {})".format(i[0], i[1], float(i[2]))
            self.cursor.execute(sql)
            self.conn.commit()
        self.close_sql()


if __name__ == '__main__':
    s = JdShop()
    s.get_html()
    data = s.parse_html()
    s.save_sql(data)
    print('第一页数据爬取完毕')
