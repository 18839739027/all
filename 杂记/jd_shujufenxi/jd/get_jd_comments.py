# -*- coding: utf-8 -*-
# @Time    : 2019/1/6  12:27
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
import requests
import time
import json
import pymysql.cursors


class JdComment(object):
    def __init__(self):
        self.url = 'https://sclub.jd.com/comment/productPageComments.action'
        self.headers = {
            'authority': 'sclub.jd.com',
            'cookie': '__jdu=15458173032631217264851; PCSYCityID=412; shshshfpa=7907750f-3dcc-5115-8a9c-8143a9eaf56f-1545817309; user-key=04239375-678c-4f1e-8eb1-4175598c2c21; pinId=eEHD3FIVsA2IRsN8YpFfgrV9-x-f3wj7; pin=jd_71f839b31d9eb; unick=%E9%95%BF%E4%BA%AD%E5%A4%96%E4%B8%B6%E9%91%AB; _tp=YhBXX5Pt4wOJtxp7D%2FeUdcWtwV4%2B9ms%2BPd7tViUIMQ8%3D; _pst=jd_71f839b31d9eb; cn=3; ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbUsEQR12XxFdKBpfVWIHEwhLXkZAfAxGXCxOWAUyUBMPclRCFXwURldnGloUZwUZWEpcRxVFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJAxNaS1ZFF3ILQlR4KWwGZzMSXHJXRxBxAUZSeRheBmABEl5CUUAScAFCVEspWzVXMxBeS19FE0UJdlVLWwhZbgsTX0RRDhVxDUJdex9eBGUAFV9CVEMTdg9DXX8ZbARXAA%3d%3d; __jdv=122270672|baidu|-|organic|not set|1545904195849; _gcl_au=1.1.751433558.1545966438; __jdc=122270672; wlfstk_smdl=whatbh9efesodpq634uldo9js2jg28ay; TrackID=1XRONOAYOzKCupnCGzDbsLRM5pO9JseIyUlqIx52kMJtFqvcqjHEBk-1owWYznr-mJqY1RbTn-5VizwzZf3k1kIKKU7rTpoQT7gcEEK-mUhw; ceshi3.com=103; 3AB9D23F7A4B3C9B=SAJVM6N5O5ADSRZXJLSKZWHJSXPONRB43YXRBZGZP4JA5CJT4TFV54STEGHOQPNNDHJKIZVZ2NUMMH7245242VESKE; shshshfpb=kvpXC66MMSaCU2Z1v7AET1Q%3D%3D; shshshfp=5d84a639a493d08cc0edbcc9e194c03c; JSESSIONID=CC066A9D5552D1571606B92254234727.s1; shshshsID=97fc34cfb6b6f246ec31ca78fcd6c7fb_1_1546002256734; __jda=122270672.15458173032631217264851.1545817303.1545996264.1546002267.11; __jdb=122270672.1.15458173032631217264851|11.1546002267; thor=E2F397084CA2075882DAFB3C3B218A432249C868525DB8D425F46B5946E89AA0C848C3FB1E33BCE1358EDE4527C02159E8ED3720E38A87159C9D9F1CFA99AC4CB9D3C0634331CF5EBC9A587313D38CFE314E54D5A2FE6B836A4402995A40E2C2C80CA960B499B1EDA8B9FC7447E748B852F384BF85E12213FB556D00BDCBF023D78A46C469B13038511F0245CA7ABD5042A3D1E38B6D76F7F6E688907363DC8E',
            'referer': 'https://item.jd.com/100000287113.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.js_content = ''
        self.conn = None
        self.cursor = None

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

    def get_html(self, params):
        """获取返回信息，对信息进行分割，去掉无用信息"""
        self.js_content = requests.get(self.url, headers=self.headers, params=params).text
        # print(self.js_content)

    def parse_html(self):
        content_dict = json.loads(self.js_content)
        comments = content_dict['comments']
        data_list = []
        for data in comments:
            small_list = []
            small_list.append(data['id'])
            # 用户id
            small_list.append(data['referenceName'])
            # 手机名
            small_list.append(data['productColor'])
            # 手机颜色
            small_list.append(data['productSize'])
            # 手机型号（公开版|其他）
            small_list.append(data['usefulVoteCount'])
            # 点赞数
            small_list.append(data['replyCount'])
            # 评论数
            small_list.append(data['score'])
            # 排序规则
            small_list.append(data['userLevelName'])
            # 用户vip等级
            small_list.append(data['creationTime'])
            # 评论发表时间
            small_list.append(data['content'])
            # 评论内容
            small_list.append(data['referenceId'])
            # 商品id
            data_list.append(small_list)
        # 精简模式，已写完，暂时不用
        #     kes=['id', 'nickname', 'content', '此处数据待添加']
        #     for k in kes:
        #         print(small_list.append(data[k]))
        #     data_list.append(small_list)
        #
        # print(len(data_list))
        return data_list

    def save_sql(self, data):
        self.connect_sql()
        # 存入数据库
        for i in data:
            assert i is not None, '数据不能为空。'
            print(i)
            sql = "INSERT INTO jd_comments.jd_comment VALUES (NULL , {},'{}','{}','{}',{},{},{},'{}','{}','{}', '{}')".format(int(i[0]), str(i[1]), i[2], i[3], int(i[4]), int(i[5]), int(i[6]), i[7], i[8], str(i[9]), i[10])
            self.cursor.execute(sql)
            self.conn.commit()
        self.close_sql()

    def run(self, s_id, page_size=10):
        for x in range(10):
            page = x
            params = {
                'productId': s_id,
                'sortType': 5,
                'score': 0,
                'page': page,
                'pageSize': page_size,
            }
            self.get_html(params)
            data = self.parse_html()
            self.save_sql(data)
            print('第{}页数据爬取完毕，等待数据保存'.format(x + 1))
            time.sleep(1.5)


if __name__ == '__main__':
    s = JdComment()
    s.run(s_id=5089253)
