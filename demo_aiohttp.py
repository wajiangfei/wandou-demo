# -*- coding:utf-8 -*-
"""并发代理请求，暂不支持socks5

"""
import asyncio
import aiohttp
import wandou
import auth
import time


class ProxySession(object):
    """
    用于并发请求的类，待完善，此处只做demo使用
    使用loop返回的result()来同步返回结果

    Args:
        proxies

    Method:
        get
        post
        down_file
        get_json
    """
    def __init__(self, proxies=None):
        self.proxies = None
        if proxies is not None:
            self.proxies = proxies

    def get(self, url_by_proxy):
        print(len(url_by_proxy))
        loop = asyncio.get_event_loop()
        task = [self._get(url, proxy) for url, proxy in url_by_proxy]
        for item in loop.run_until_complete(asyncio.wait(task))[0]:
            try:
                assert isinstance(item.result(), ProxyResponse)
                yield item.result()
            except Exception as e:
                print(str(e))

    async def _get(self, url, proxy=None):

        print('请求...'+url)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=proxy) as resp:
                    await_data = {}

                    text = await resp.text()
                    await_data['text'] = text
                    read = await resp.read()
                    await_data['read'] = read

                    data = {}

                    data['data'] = resp.status
                    data['url'] = resp.url
                    data['headers'] = resp.headers
                    data['history'] = resp.history
                    data['links'] = resp.links
                    data['charset'] = resp.charset
                    data['connection'] = resp.connection
                    data['content_disposition'] = resp.content_disposition
                    data['ATTRS'] = resp.ATTRS
                    data['content_length'] = resp.content_length
                    data['content_type'] = resp.content_type
                    data['cookies'] = resp.cookies
                    data['get_encoding'] = resp.get_encoding()
                    data['host'] = resp.host
                    data['method'] = resp.method
                    data['raw_headers'] = resp.raw_headers
                    data['closed'] = resp.closed
                    data['real_url'] = resp.real_url
                    data['reason'] = resp.reason
                    data['request_info'] = resp.request_info
                    data['version'] = resp.version
                    response = ProxyResponse(data, await_data)
                    return response
            except Exception as e:
                print('请求...'+url+'出错')
                print(str(e))


class ProxyBaseResponse(object):
    def __init__(self, data):
        self.status = data['data']
        self.url = data['url']
        self.headers = data['headers']
        self.history = data['history']
        self.links = data['links']
        self.charset = data['charset']
        self.connection = data['connection']
        self.content_disposition = data['content_disposition']
        self.ATTRS = data['ATTRS']
        self.content_length = data['content_length']
        self.content_type = data['content_type']
        self.cookies = data['cookies']
        self.encoding = data['get_encoding']
        self.host = data['host']
        self.method = data['method']
        self.raw_headers = data['raw_headers']
        self.closed = data['closed']
        self.real_url = data['real_url']
        self.reason = data['reason']
        self.request_info = data['request_info']
        self.version = data['version']

    def get_encoding(self):
        return self.encoding


class ProxyResponse(ProxyBaseResponse):
    """
    对aiohttp异步和同步返回的结果封装
    """

    def __init__(self, data, await_data):
        super(ProxyResponse, self).__init__(data)
        self.text = await_data['text']
        self.read = await_data['read']


if __name__ == '__main__':
    session = ProxySession()
    app_key = "xxxxxxxxxxxxxxxxxxxx"
    myauth = auth.Auth(app_key) # 传入app_key
    mywandou = wandou.WandouManager(myauth)  # 传入myauth

    url_list = ['http://myip.ipip.net'] * 10  # 需要访问的url列表
    proxies = []
    proxies.extend([ps for ps in mywandou.proxies(num=10)]) # 获取代理ip列表
    url_by_proxy = list(zip(url_list, proxies))  # 每项为url和代理ip的的二元组
    print(url_by_proxy)

    start_time = time.time()
    result = session.get(url_by_proxy)  # 请求。。。受代理ip可靠性和目标网站影响速度
    end_time = time.time()
    tol = end_time - start_time

    j = 0
    for i in result:
        if i.status == 200:
            j += 1

    print('true_num：'+str(j))
    print("time："+str(tol))
