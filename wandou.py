# -*- coding: utf-8 -*-

from config import *
import requests
import time
import json

class WandouManager(object):
    """获取ip类

    包括获取地域列表和ip列表
    https://h.wandouip.com/api-doc/index.html#api-areas-list

    Attributes:
        auth: app_key，Auth对象
    """

    def __init__(self, auth):
        self.auth = auth

    def area_list(self):
        """返回当前可用的地区列表
        可能因为维护或者其他原因，返回的地区并不一定100%可用，接口有2分钟缓存


        """
        params = {
            'app_key': self.auth.app_key()
        }
        try:
            res = requests.post(api_host + arealist_api, data=params)
            return res.json()
        except requests.exceptions.RequestException as e:
            print("{} 地域列表获取失败,错误信息：".format(time.asctime()))
            print(str(e))
            return None

    def ip_list(self, num=5, protocol=1, type=2, lb=None, port=None, area_id=None):
        """ip获取：

        具体参数参见：
        https://h.wandouip.com/api-doc/index.html#api-ip-list

        Args:
            num:        请求ip数量，默认为5
            protocol:   使用协议：1.http，2.https，3.socks5，默认为http
            type:       返回数据格式，默认json，1.text,2.json（非text则为json）
            lb:         分隔符，只有返回text格式数据时用到，可选值为：['\r\n','\r','\n','\t']
            port:       端口位数，3.3位端口, 4.4位端口 ,5.5位端口, 0.随机http(s)端口
            area_id:    地区id（城市），从地区列表接口获得，兼容标准地区编码，例如 320100 表示南京

        Returns:
            返回一个dict变量
            请求出错时返回一个None类型，并且输出报错
        """
        params = {
            'app_key': self.auth.app_key(),
            'num': num,
            'xy': protocol,
            'type': type
        }
        if lb is not None:
            params['lb'] = lb
        if port is not None:
            params['port'] = port
        if area_id is not None:
            params['area_id'] = area_id
        try:
            res = requests.post(api_host + iplist_api, data=params)
            return res.json()
        except requests.exceptions.RequestException as e:
            print("{} ip获取失败,错误信息：".format(time.asctime()))
            print(str(e))
            return None
        except json.decoder.JSONDecodeError as e:
            print(str(e))

    def proxies(self, num=5, protocol=1, type=2, lb=None, port=None, area_id=None):
        """
        返回一个可迭代的对象，只有ip和port

        参数同ip_list
        """
        res = self.ip_list(num, protocol, type, lb, port, area_id)
        if res is not None and res['code'] == 200:
            if protocol == 1:
                for item in res['data']:
                    yield 'http://'+item['ip']+':'+str(item['port'])
            elif protocol == 2:
                for item in res['data']:
                    yield 'https://'+item['ip']+':'+str(item['port'])
            elif protocol == 3:
                for item in res['data']:
                    yield 'socks5://'+item['ip']+':'+str(item['port'])

