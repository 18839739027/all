# -*- coding: utf-8 -*-
# @Time    : 2018/12/2620:48
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm

# 需要登陆的情况
"""
场景：个人信息页， 订单也页， 需要登陆权限后才可以访问
权限验证： 网站通过token 或 session id 来限制访问页面
sessionid: http无状态，
"""
import requests
from lxml import etree


class GitHub(object):
    def __init__(self):
        self.me_url = 'https://github.com/18839739027'
        self.profile_url = 'https://github.com/settings/profile'
        self.login_url = "https://github.com/login"
        self.do_login_url = "https://github.com/session"
        self.login_html = ''
        self.profile_dom = ''
        self.s = requests.Session()
        self.authenticity_token = ''
        self.headers = {
            'Host': 'github.com',
            'Referer': 'https://github.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }
        self.parse_login_html()
        self.session_args = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.authenticity_token,
            'login': '您的账号',
            'password': '您的密码'
        }

    def get_login_html(self):
        while True:
            try:
                login_html = self.s.get(self.login_url, headers=self.headers).text
                self.login_html = etree.HTML(login_html)
            except Exception as e:
                print(e)
                print('请求失败')
            else: break

    def parse_login_html(self):
        self.get_login_html()
        self.authenticity_token = self.login_html.xpath('//input[@name="authenticity_token"]/@value')[0]
        print('token:', self.authenticity_token)

    def get_session(self):
        while True:
            try:
                session_resp = self.s.post(self.do_login_url, headers=self.headers, data=self.session_args)
                print(session_resp)
            except Exception as e:
                print(e)
                break
            else: break

    def profile_html(self):
        # 请求个人设置页面数据并解析
        profile_resp = self.s.get(self.profile_url, headers=self.headers)
        if profile_resp.status_code != requests.codes.ok:
            raise Exception("请求个人页设置失败")
        # print(profile_resp.text)
        self.profile_dom = etree.HTML(profile_resp.text)
        profile_email = self.profile_dom.xpath('//select[@id="user_profile_email"]/option[2]/text()')[0]
        # 请求主页数据并解析
        me_resp = self.s.get(self.me_url, headers=self.headers)
        if me_resp.status_code != requests.codes.ok:
            raise Exception("请求主页失败")
        me_dom = etree.HTML(me_resp.text)
        warehouse_list = me_dom.xpath('//span[@class="pinned-repo-item-content"]/span/a/span/text()')
        print(profile_email)
        print(warehouse_list)
        # 请求个人收藏列表
        params = {
            'tab': 'stars'
        }
        stars = self.s.get(self.me_url, params=params, headers=self.headers)
        if stars.status_code != requests.codes.ok:
            raise Exception("请求收藏页失败")
        stars_dom = etree.HTML(stars.text)
        stars_list = stars_dom.xpath('//h3/a/@href')
        print(stars_list)

    def run(self):
        self.get_session()
        self.profile_html()


if __name__ == '__main__':
    A = GitHub()
    A.run()

