# -*- coding: utf-8 -*-
# @Time    : 2019/1/7  10:58
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
import requests
import time
import json
import csv


class BilBil(object):
    def __init__(self):
        self.url = 'https://api.bilibili.com/x/web-interface/newlist'
        self.html = ''
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer':'https://www.bilibili.com/v/anime/serial/?spm_id_from=333.334.b_7072696d6172795f6d656e75.8',
            'Cookie':'LIVE_BUVID = AUTO7515461750678100;stardustvideo = 1;CURRENT_FNVAL = 16;rpdid = iqxlpsxopxdospxomswpw;DedeUserID = 329431095;DedeUserID__ckMd5 = 43c75377ea535c6c;SESSDATA = 0c68e8ec % 2C1548767164 % 2Cdf27a5c1;bili_jct = a4ed8b9d75da712298420bd449f53e7c;CURRENT_QUALITY = 80;UM_distinctid = 167ff3a069f8bf - 06afb5786680d3 - 3f674604 - 144000 - 167ff3a06a18eb;buvid3 = 4F573F3E - 0896 - 41D4 - 8BA9 - F1D0A0F5B7FC85451infoc;bsource = seo_baidu;sid = cn8hyigd;_dfcaptcha = c8a57572eeefc5409f83ac25ddd8f513',
            'Host':'api.bilibili.com',
        }
        self.data_list = []

    def get_html(self, params):
        """获取json源码"""
        try:
            self.html = requests.get(url=self.url, params=params, headers=self.headers).text
        except Exception as e:
            print(e)
            print('错误，请重新请求！')

    def parse_html(self):
        """解析json数据"""
        data_dict = json.loads(self.html)
        data_list = data_dict['data']['archives']
        for data in data_list:
            list1 = []
            list1.append(data['aid'])
            list1.append(data['title'])
            list1.append(data['attribute'])
            list1.append(data['duration'])
            list1.append(data['pic'])
            list1.append(data['ctime'])
            self.data_list.append(list1)
        print(self.data_list)

    def save_csv(self):
        """保存数据至csv"""
        # w直接从开始写入,a追加写入
        with open('BilBil.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['番号', '名字', '观看数', '评论数', '缩略图地址', '发布时间'])
        with open('BilBil.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for x in self.data_list:
                writer.writerow(x)
                # time.sleep(0.1)
            # 数据写入需要时间，程序结束过快会导致数据写入不全

    def run(self):
        # '?callback=jqueryCallback_bili_9989938033309436&rid=33&type=0&pn=2&ps=20&jsonp=jsonp&_=1546830252656'
        for x in range(0, 10):
            page = x
            params = {
                'rid': '33',
                'type': '0',
                'pn': page,
                'jsonp': 'jsonp',
                '_': '1546830252656'
            }
            self.get_html(params)
            self.parse_html()
            self.save_csv()
            time.sleep(1)
            print('第{}页数据爬取完毕'.format(x + 1))


if __name__ == '__main__':
    s = BilBil()
    s.run()