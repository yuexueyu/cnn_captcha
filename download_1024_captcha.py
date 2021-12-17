#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import zlib
import urllib.request
import urllib.parse
import time
import random
from fake_useragent import UserAgent
import ssl
import asyncio
from threading import Thread
from tqdm import tqdm

# 全局取消证书验证，避免访问https网页报错
ssl._create_default_https_context = ssl._create_unverified_context


def get_proxy_ip():
    options = {
        "orderid": "992691716744351",
        "num": "1",
        "pt": "1",
        "dedup": "1",  ## 过滤今天提取过的IP，不带此参数代表不过滤
        "sep": "1",
        "sign_type": "simple",
        "signature": "xynjb77zv0clfx1ewhqkrdmbvj8rkq1y",
    }
    params = urllib.parse.urlencode(options)
    url = "https://dps.kdlapi.com/api/getdps/?%s" % params
    # print(url)
    headers = {"Accept-Encoding": "Gzip"}
    request = urllib.request.Request(url=url, headers=headers)

    with  urllib.request.urlopen(request) as response:
        # print(response.code)  # 获取Reponse的返回码
        content_encoding = response.headers.get('Content-Encoding')
        if content_encoding and "gzip" in content_encoding:
            ip = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS).decode('utf-8')  # 获取页面内容
        else:
            ip = response.read().decode('utf-8')  # 获取页面内容

        return ip


def download_url_img(img_url, proxy_ip, user_agent):
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,zh-CN;q=0.9",
        "Cache-Control": "max-age=0",
        # "Cookie": "227c9_lastvisit=0%091635044614%09%2Fread.php%3Ftid%3D4750601; PHPSESSID=88qiemg4npchv7s234qimmmbf6; cf_chl_2=4d347a8cd630608; cf_chl_prog=x12; cf_clearance=F6_owvUgNgo3hgkNHyYtwKWWAg2tzc7F221Ql5NpO0U-1639200662-0-250",
        "DNT": "1",
        "Host": "t66y.com",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": user_agent,
    }

    # img_url = "https://dev.kdlapi.com/testproxy"
    request = urllib.request.Request(img_url, headers=header)

    # username = "jack"
    # password = "vq97hr02"
    # proxies = {
    #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    # }
    proxies = {
        "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
        "https": "http://%(proxy)s/" % {"proxy": proxy_ip}
    }
    # print(proxies)

    # 使用代理IP发送请求
    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)
    # urllib.request.install_opener(opener)

    try:
        response = opener.open(request, timeout=5)
        # response = urllib.request.urlopen(request, timeout=5)
        print('响应码：' + str(response.code))  # 获取Reponse的返回码
        filename = './captcha_1024_images/' + str(time.time()) + '.jpg'
        img = response.read()  ## 这里也会超时？？
        with open(filename, 'wb') as f:
            f.write(img)
    except Exception as e:
        time.sleep(0.1)
        print(e.__str__())
    else:
        time.sleep(0.1)
        # content_encoding = response.headers.get('Content-Encoding')
        # if content_encoding and "gzip" in content_encoding:
        #     print(zlib.decompress(response.read(), 16 + zlib.MAX_WBITS).decode('utf-8'))  # 获取页面内容
        # else:
        #     print(response.read().decode('utf-8'))  # 获取页面内容
        print(filename + '，下载成功！')


def get_image(max):
    n = 1
    m = max

    proxy = "127.0.0.1:10086"
    # proxy = get_proxy_ip()
    ua = UserAgent(verify_ssl=False)
    ua = ua.random

    print('代理IP：' + proxy)
    print('User-Agent：' + ua)

    while n < m + 1:
        url = 'http://t66y.com/require/codeimg.php?' + str(random.random())
        print('第' + str(n).zfill(3) + '/' + str(m).zfill(3) + '张图片，下载中...')
        if n % 10 == 0:
            ua = UserAgent(verify_ssl=False)
            ua = ua.random
        # print('User-Agent：' + ua)
        download_url_img(url, proxy, ua)
        n = n + 1

    print('执行完成')


def run():
    print("多线程执行..")
    image_max = 50

    t_num = 0
    t_max = 100
    while t_num < t_max:
        Thread(target=get_image, args=(image_max,)).start()
        t_num = t_num + 1
        time.sleep(0.5)


if __name__ == '__main__':
    run()
