# -*- coding: utf-8 -*-

from config import *
import base64
import requests
import time
import re

class Auth(object):
    """
    豌豆HTTP鉴权类
    包括ip白名单认证和代理请求凭证

    Attributes:
        __app_key: app_key，后台[开放接口]页面中可以找到，参见https://h.wandouip.com/member/open/

    """

    def __init__(self, app_key):
        """初始化Auth类"""
        self.__check_app_key(app_key)
        self.__app_key = app_key

    @staticmethod
    def __check_app_key(app_key):
        if not app_key:
            raise ValueError('invalid key')

    def white_list(self):
        params = {'app_key': self.__app_key}
        try:
            res = requests.post(api_host + whitelist_api, data=params)
            return res.json()
        except requests.exceptions.RequestException as e:
            print(time.asctime()+" ip白名单添加失败,错误信息：")
            print(str(e))
            return None

    def update_list(self, ip=None, wid=None):
        """修改/更新ip白名单，如果只传ip且ip未达到总使用量则会新增，否则请指定id值，更新对应id的白名单ip

        Args:
            ip:     要更新的ip，,若缺省则访问myip.ipip.net获取ip。若wid缺省，则增加一个ip
            wid:    要更新的ip对应的id，可从whitelist中获取

        Returns:
            返回一个dict变量
            请求出错时返回一个None类型，并且输出报错
        """
        if ip is None:
            try:
                res = requests.get('https://myip.ipip.net')
                pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                ip = pattern.findall(res.text)[0]
                print(ip)
            except requests.exceptions.RequestException as e:
                print(time.asctime() + " 获取本地ip失败,错误信息：")
                print(str(e))
                return None

        params = {
            'app_key': self.__app_key,
            'ip': ip,
        }
        if wid is not None:
            params['id'] = wid
        try:
            res = requests.post(api_host+update_whitelist_api, data=params)
            return res.json()
        except requests.exceptions.RequestException as e:
            print(time.asctime()+" ip白名单更新失败,错误信息：")
            print(str(e))
            return None

    def _delete_list(self, ip=None, wid=None):
        """删除ip白名单，请勿调用，会将你的购买的ip都给删了，如果需要取消设置的ip白名单请使用/api/whitelist/update设置ip为空

        Args:
            ip:     要删除的ip
            wid:    要删除的ip对应的id，可从whitelist中获取

        Returns:
            返回一个dict变量
            请求出错时返回一个None类型，并且输出报错
        """
        params = {
            'app_key': self.__app_key
        }
        headers = {

        }
        if wid is not None:
            params['id'] = wid
        if ip is not None:
            params['ip'] = ip
        try:
            res = requests.post(api_host+delete_whitelist_api, data=params)
            return res.json()
        except requests.exceptions.RequestException as e:
            print("{} ip白名单删除失败,错误信息：".format(time.asctime()))
            print(str(e))
            return None

    def app_key(self):
        return self.__app_key


def authorization(username, password):

        return base64.b64encode((username+':'+password).encode('utf-8')).decode()

