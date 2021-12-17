#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import os
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt


# 删除临时文件夹下的所有文件
def del_files(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_files(c_path)
        else:
            os.remove(c_path)


# 临时图片保存
def save_tmp_image(img, root_dir, image_suffix):
    # 判断文件夹是否存在
    root_dir = root_dir + 'tmp/'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    # 保存在本地
    img_name = str(time.time()).replace(".", "")
    img_path = root_dir + img_name + '.' + image_suffix
    with open(img_path, 'wb') as f:
        img.save(f)
        return img_path


# 验证码图片保存
def save_captcha_image(img, code, root_dir, image_suffix):
    # 判断文件夹是否存在
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    # 保存在本地
    img_name = str(time.time()).replace(".", "") + "_" + code
    img_path = root_dir + img_name + '.' + image_suffix
    print(img_path)
    with open(img_path, 'wb') as f:
        img.save(f)


# 生成随机字母
def rndChar(characters):
    characters = list(characters)
    return random.choice(characters)


# 生成随机背景颜色
def randomBgColor():
    return (random.randint(180, 220), random.randint(190, 230), random.randint(200, 240))


# 生成随机字体颜色
def rndomCharColor():
    return (random.randint(0, 125), random.randint(10, 125), random.randint(20, 125))


# 生成随机颜色
def rndColor():
    return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))


def create_captcha_image_v1(characters, char_length, width, height, font_file, font_size):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=randomBgColor())
    draw = ImageDraw.Draw(img, mode='RGB')

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(30):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    # 写干扰星号 *
    for i in range(30):
        w = random.randint(1, width)
        h = random.randint(1, height)
        draw.text([w, h], "*", rndColor())

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar(characters)
        code.append(char)
        h = random.randint(1, 15)
        draw.text([i * width / char_length, h], char, font=font, fill=rndomCharColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


# 创建背景图
def create_bg_image(width, height, root_dir, image_suffix):
    img = Image.new(mode='RGB', size=(width, height), color=randomBgColor())
    draw = ImageDraw.Draw(img, mode='RGB')

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(30):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    # 写干扰星号 *
    for i in range(30):
        w = random.randint(1, width)
        h = random.randint(1, height)
        draw.text([w, h], "*", rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return img
    # img_path = save_tmp_image(img, root_dir, image_suffix)
    # return img_path


# 创建透明背景的png
def create_captcha_image_v2(width, height, characters, char_length, font_file, font_size, root_dir, image_suffix):
    # draw = ImageDraw.Draw(img, mode='RGBA')

    item_width = int(width / char_length)
    tmp_imgs = []
    code = []
    for i in range(int(char_length)):
        if i == (char_length - 1):
            w = width - (item_width * i)
        else:
            w = item_width

        img = Image.new(mode='RGBA', size=(w, height), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img, mode='RGBA')

        char = rndChar(characters)
        code.append(char)
        font = ImageFont.truetype(font_file, int(font_size))
        # 让文字位于图片居中
        imwidth, imheight = img.size
        font_width, font_height = draw.textsize(char, font)
        x = (imwidth - font_width - font.getoffset(char)[0]) / 2
        y = (imheight - font_height - font.getoffset(char)[1]) / 2
        draw.text((x, y), text=char, font=font, fill=rndomCharColor())
        # img.show()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
        # 旋转图片
        angle = random.randint(-15, 15)  # 旋转角度
        if i != 0 | i != (char_length - 1):
            angle = random.randint(-20, 20)
        center = (x, y)  # 中心点
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        t_img = cv2.warpAffine(img, M, (w, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        # cv2.imshow('image', t_img)
        # cv2.waitKey(0)
        tmp_imgs.append(t_img)

    imgs = tmp_imgs[0]
    for k, im in enumerate(tmp_imgs):
        # print(k, im)
        if k > 0:
            imgs = np.hstack([imgs, im])

    imgs = Image.fromarray(cv2.cvtColor(imgs, cv2.COLOR_BGRA2RGBA))
    return imgs, ''.join(code)
    # imgs.show()
    # img_path = save_tmp_image(imgs, root_dir, 'png')
    # return img_path, ''.join(code)


# 合并图片
def paste_image2(img_up, img_bg):
    # # 下层图片
    # img1 = Image.open(img_bg).convert('RGBA')
    # # 上层图片
    # img2 = Image.open(img_up).convert('RGBA')

    # 下层图片
    img1 = img_bg
    # 上层图片
    img2 = img_up
    r, g, b, a = img2.split()

    img1.paste(img2, (0, 0), mask=a)
    return img1


def run():
    with open("conf/captcha_config_v2.json", "r") as f:
        config = json.load(f)
    # 配置参数
    root_dir = config["root_dir"]  # 图片储存路径
    image_suffix = config["image_suffix"]  # 图片储存后缀
    characters = config["characters"]  # 图片上显示的字符集
    char_length = config["char_length"]  # 图片上的字符数量
    count = config["count"]  # 生成多少张样本
    width = config["width"]  # 图片宽度
    height = config["height"]  # 设置图片高度
    font_file = config["font_file"]  # 字体
    font_size = config["font_size"]  # 字体大小

    for i in range(count):
        tmp_bg_img_path = create_bg_image(width, height, root_dir, image_suffix)
        # print(tmp_bg_img_path)
        tmp_captcha_img_path, code = create_captcha_image_v2(width, height, characters, char_length, font_file,
                                                             font_size,
                                                             root_dir, image_suffix)
        # print(tmp_captcha_img_path, code)
        img = paste_image2(tmp_captcha_img_path, tmp_bg_img_path)
        # img.show()
        save_captcha_image(img, code, root_dir, image_suffix)
        # del_files(root_dir + '/tmp')


if __name__ == '__main__':
    run()
