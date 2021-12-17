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
        "Host": "gab.122.gov.cn",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,zh-CN;q=0.9",
        # "Cookie": "_uab_collina=163660878745036298112246; _gscu_1924143127=36608114bwrzcl20; aliyungf_tc=d4d5e65562bfe28f3c3713bbb974e71406791db63dcb7136e38138a70d50e2a5; acw_tc=781bad3f16394516140422373e291aa5ff121298d4a1dc63deedf31cf3b415; JSESSIONID-L=3740d0f3-4f73-43a6-90fe-361230db17a2; accessToken=++XcryJMImlLu23BjaFVDmAftTlIeV/rlkaTQUgFKciKdWKRslhmQI8MOaWZ+tUFxhBbohQA0e3Hw4wMQGg6XBDW5IDbVhFIKppY72EShmDYZmQai9peAHxEZPMvdNrSmJDywa7U7waB6BRO07HebA829ICLjOisuH/Yy5Gy+dsDTI+cnVyiYr40FIXlds7a; _gscbrs_1924143127=1; _gscs_1924143127=39451613t6rqpo99|pv:1",
        "User-Agent": user_agent,
    }

    request = urllib.request.Request(img_url, headers=header)

    proxies = {
        "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
        "https": "http://%(proxy)s/" % {"proxy": proxy_ip}
    }
    # print(proxies)

    # 使用代理IP发送请求
    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)

    try:
        response = opener.open(request, timeout=5)
        print('响应码：' + str(response.code))  # 获取Reponse的返回码
        filename = './captcha_122_images/' + str(time.time()) + '.jpg'
        img = response.read()  ## 这里也会超时？？
        with open(filename, 'wb') as f:
            f.write(img)
    except Exception as e:
        print(e.__str__())
        time.sleep(0.1)
    else:
        print(filename + '，下载成功！')
        time.sleep(2)


def get_image(max):
    n = 1
    m = max

    # proxy = "127.0.0.1:10086"

    proxy = get_proxy_ip()
    print('代理IP：' + proxy)

    ua = UserAgent(verify_ssl=False)
    ua = ua.random
    print('User-Agent：' + ua)

    while n < m + 1:
        url = 'https://gab.122.gov.cn/m/tmri/captcha/math?nocache=' + str(int(time.time()))
        print('第' + str(n).zfill(3) + '/' + str(m).zfill(3) + '张图片，下载中...')
        if n % 10 == 0:
            ua = UserAgent(verify_ssl=False)
            ua = ua.random
        download_url_img(url, proxy, ua)
        n = n + 1

    print('执行完成')


def run():
    print("多线程执行..")
    image_max = 20

    t_num = 0
    t_max = 100
    while t_num < t_max:
        Thread(target=get_image, args=(image_max,)).start()
        t_num = t_num + 1


if __name__ == '__main__':
    run()
