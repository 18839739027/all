# -*- coding: utf-8 -*-
# @Time    : 2019/1/7  12:05
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
import json
import pymysql
import jieba
import pygal
from wordcloud import WordCloud


class Tb(object):
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.string = ""

    def open_json(self):
        """打开json文件"""
        with open('tb_comments_1.json', encoding='utf-8') as f:
            comments1 = json.load(f)
        with open('tb_comments_2.json', encoding='utf-8') as c:
            comments2 = json.load(c)
            return comments1, comments2

    def parse_json(self, comments1, comments2):
        data_list = comments1['rateDetail']['rateList'], comments2['rateDetail']['rateList']
        count = 0
        for data_list in data_list:
            for data in data_list:
                if data['appendComment']:
                    append_content = data['appendComment']['content']
                else:
                    append_content = '此订单，用户未追评！'
                rate_date = data['rateDate']
                rate_content = data['rateContent']
                comment_id = data['id']
                auction_sku = data['auctionSku']
                count += 1
                print(count, '正在保存订单编号：{}的数据'.format(data['id']))
                self.save_sql(comment_id, rate_content, rate_date, append_content, auction_sku)

    def select_sql_1(self):
        self.connect_sql()
        sql = "SELECT comment_id, rate_content, rate_date, append_content, action_sku FROM taobao.comments"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.close_sql()
        return data

    def select_sql_3(self):
        self.connect_sql()
        sql = "SELECT rate_content,append_content, rate_date FROM taobao.comments order by rate_date desc"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.close_sql()
        return data

    def select_sql_5(self):
        self.connect_sql()
        sql = "SELECT action_sku FROM taobao.comments"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.close_sql()
        return data

    def gen_pei(self, data):
        black = 0
        jin = 0
        lan = 0
        bai = 0
        for s in data:
            if '黑色' in s[0]:
                black += 1
            if '金色' in s[0]:
                jin += 1
            if '蓝色' in s[0]:
                lan += 1
            if '白色' in s[0]:
                bai += 1
        pie_chart = pygal.Pie()
        pie_chart.title = '购买手机颜色比例(in % )'
        pie_chart.add('黑色', float('%.2f' % (black / 0.2)))
        pie_chart.add('金色', float('%.2f' % (jin / 0.2)))
        pie_chart.add('蓝色', float('%.2f' % (lan / 0.2)))
        pie_chart.add('白色', float('%.2f' % (bai / 0.2)))
        pie_chart.render_to_file('数据可视化(饼状图).svg')

    def word_cloud(self):
        font = 'msyh.ttc'
        wc = WordCloud(
            font_path=font,
            background_color='white',
            width=1500,
            height=1200,
            # max_font_size=200,
            # min_font_size=20,
        ).generate(self.string)
        wc.to_file('词云1.png')

    def save_sql(self, *args):
        self.connect_sql()
        sql = "SELECT comment_id FROM taobao.comments WHERE comment_id={}".format(args[0])
        result = self.cursor.execute(sql)
        if not result:
            sql = "INSERT INTO taobao.comments VALUES (null, '{}', '{}', '{}', '{}', '{}')".format(args[0], args[1], args[2], args[3], args[4])
        else:
            print('该订单信息已存在')
        self.cursor.execute(sql)
        self.close_sql()

    def connect_sql(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3309,
            user='root',
            password='123456',
            db='taobao'
        )
        self.cursor = self.conn.cursor()

    def close_sql(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def run(self):
        print('1.爬取数据')
        print('2.输出数据_考试要求一')
        print('3.输出数据_考试要求三')
        print('4.生成词云图')
        print('5.生成饼状图')
        print('0.退出')
        while True:
            select = int(input('请输入您的选择：'))
            if select == 1:
                comments1, comments2 = self.open_json()
                self.parse_json(comments1, comments2)
            elif select == 2:
                data = self.select_sql_1()
                for d in data:
                    print(d)
            elif select == 3:
                data = self.select_sql_3()
                for d in data:
                    print(d)
            elif select == 4:
                data = self.select_sql_3()
                print('词云图生成中，请稍等。。。')
                for d in data:
                    # if d[0] == '此订单，用户未追评！':
                    self.string += "".join(jieba.cut(f'{d[0]}', cut_all=False))
                    self.string += "".join(jieba.cut(f'{d[1]}', cut_all=False))
                self.word_cloud()
                print('词云图生成完毕，赶紧去看看吧！')
            elif select == 5:
                print('饼状图生成中， 请稍等。。。')
                data = self.select_sql_5()
                self.gen_pei(data)
                print('饼状图生成完毕，赶紧去看看吧！')
            else:
                break


if __name__ == '__main__':
    s = Tb()
    s.run()