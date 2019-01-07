# -*- coding: utf-8 -*-
# @Time    : 2019/1/6  16:32
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
import pymysql
import pygal


class JdShow(object):
    def __init__(self):
        self.connect = None
        self.cursor = None
        self.string = ''
        self.lv = []

    def connect_sql(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3309,
            user='root',
            password='123456',
            db='jd_comments'
        )
        self.cursor = self.connect.cursor()

    def close_sql(self):
        self.cursor.close()
        self.connect.close()

    def select_sql_vip_num(self, p_id):
        self.connect_sql()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="PLUS会员" AND p_id={p_id}')
        PLUS0 = self.cursor.fetchone()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="PLUS会员[试用]" AND p_id={p_id}')
        PLUS1 = self.cursor.fetchone()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="金牌会员" AND p_id={p_id}')
        jin = self.cursor.fetchone()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="钻石会员" AND p_id={p_id}')
        zuan = self.cursor.fetchone()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="银牌会员" AND p_id={p_id}')
        yin = self.cursor.fetchone()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="铜牌会员" AND p_id={p_id}')
        tong = self.cursor.fetchone()
        self.cursor.execute(f'SELECT count(user_vip) FROM jd_comment WHERE user_vip="注册会员" AND p_id={p_id}')
        zhuce = self.cursor.fetchone()
        self.lv = [zhuce[0], tong[0], yin[0], jin[0], zuan[0], PLUS1[0], PLUS0[0]]
        self.close_sql()

    def gen_pei(self):
        bar = pygal.Bar()
        bar.add('注册会员', self.lv[0])
        bar.add('铜牌会员', self.lv[1])
        bar.add('银牌会元', self.lv[2])
        bar.add('金牌会员', self.lv[3])
        bar.add('钻石会员', self.lv[4])
        bar.add('PLUS会员[试用]', self.lv[5])
        bar.add('PLUS会员', self.lv[6])
        bar.render_to_file('JD数据可视化(条形图).svg')

    def run(self, p_id):
        self.select_sql_vip_num(p_id)
        print('数据处理中请稍等！')
        self.gen_pei()
        print('svg生成完毕， 程序终止！')


if __name__ == '__main__':
    s = JdShow()
    s.run(p_id=100000773875)
