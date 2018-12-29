# -*- coding: utf-8 -*-
# @Time    : 2018/12/28  12:01
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
import requests
import time
import json
import csv
import pymysql.cursors


class JdComment(object):
    def __init__(self):
        self.url = 'https://sclub.jd.com/comment/productPageComments.action'
        self.headers = {
            'authority': 'sclub.jd.com',
            'cookie': '您的cookie',
            'referer': 'https://item.jd.com/100000287113.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.js_content = ''
        self.conn = None
        self.cursor = None
        # self.headers_csv()

    def connect_sql(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='您的账号',
            password='您的密码',
            db='jd'
        )
        self.cursor = self.conn.cursor()

    def close_sql(self):
        self.cursor.close()
        self.conn.close()

    def get_html(self, params):
        """获取返回信息，对信息进行分割，去掉无用信息"""
        # resp = requests.get(self.url, headers=self.headers).text
        # self.js_content = resp.split('15267(')[-1].split(');')[0]
        self.js_content = requests.get(self.url, headers=self.headers, params=params).text
        # print(self.js_content)

    def parse_html(self):
        content_dict = json.loads(self.js_content)
        comments = content_dict['comments']
        data_list = []
        for data in comments:
            small_list = []
        #     超复杂，写了一半，舍弃
        #     id = data['id']
        #     nickname = ['nickname']
        #     content = data['content']
        #     # creationTime = data['creationTime']
        #     referenceName = data['referenceName']
        #     usefulVoteCount = data['usefulVoteCount']
        #     replyCount = data['replyCount']
        #     score = data['score']
        # #     images = data['images']
        # #     # for image in images:
        # #         # print(image['imgUrl'])
        # #     print(id, content)
        # # goodRateShow = content_dict['productCommentSummary']['goodRateShow']
        # # comments = content_dict['comments']
        # # for data in comments:
        #     userLevelName = data['userLevelName']
        #     color = data['productColor']
        #     size = data['productSize']
        # 中等复杂， 已写完
            small_list.append(data['id'])
            small_list.append(data['nickname'])
            small_list.append(data['content'])
            small_list.append(data['referenceName'])
            small_list.append(data['usefulVoteCount'])
            small_list.append(data['replyCount'])
            small_list.append(data['score'])
            small_list.append(data['userLevelName'])
            small_list.append(data['productColor'])
            small_list.append(data['productSize'])
            data_list.append(small_list)
        # 精简模式，已写完，暂时不用
        #     kes=['id', 'nickname', 'content', '此处数据待添加']
        #     for k in kes:
        #         print(small_list.append(data[k]))
        #     data_list.append(small_list)
        #
        # print(len(data_list))
        return data_list

    def headers_csv(self):
        with open('Jd_js_comments.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['用户ID', '用户名', '评论内容', '手机信息', '点赞数', '评论数', '排序规则', '会员等级', '手机颜色', '型号'])

    def save_csv(self, data):
        """更多的存储方式"""
        with open('Jd_js_comments.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def save_sql(self, data):
        self.connect_sql()
        for i in data:
            print(i)
            sql = "INSERT INTO jd.comments VALUES (NULL , '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(str(i[0]), str(i[1]), i[2], i[3], str(i[4]), str(i[5]), str(i[6]), i[7], i[8], i[9])
            self.cursor.execute(sql)
            self.conn.commit()
        self.close_sql()

    def run(self):
        for x in range(10):
            page = x
            params = {
                'productId': 5089253,
                'sortType': 5,
                'score': 0,
                'page': page,
                'pageSize': 10,
                # 'callback': 'fetchJSON_comment98vv105467',
                # 'isShadowSku': 0,
                # 'fold': 1
            }
            self.get_html(params)
            data = self.parse_html()
            # self.save_csv(data)
            self.save_sql(data)
            print('第{}页数据爬取完毕，等待数据保存'.format(x + 1))
            time.sleep(5)


if __name__ == '__main__':
    s = JdComment()
    s.run()

