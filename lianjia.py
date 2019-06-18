# -*- coding:utf-8 -*-
import requests
import random
from requests.exceptions import RequestException
from time import sleep
import csv
from urllib import request as urlrequest
import ssl
from lxml import etree
import re
import threading
from bs4 import BeautifulSoup


# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# districts = ['jingan', 'xuhui', 'huangpu', 'changning', 'putuo', 'pudong', 'baoshan', 'zhabei',
#              'hongkou', 'yangpu', 'minhang', 'jinshan', 'jiading', 'chongming', 'fengxian', 'songjiang']

districts = ['xihu', "xiacheng", "jianggan",
             "gongshu", "shangcheng", "binjiang"]

availabe_proxies = ['http://112.85.130.187:9999', 'http://61.235.24.126:8123',
                    'http://27.221.32.140:80', 'http://120.79.5.147:80']


def write_to_file(content):
    with open('result.csv', 'a') as csvfile:
        headings = ["price", "district", "bizCircle",
                    "area", "direction", "roomType", "url"]
        writer = csv.DictWriter(
            csvfile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        for row in content:
            writer.writerow(row)
        csvfile.close()


# 获取页面
def get_page(url):
    req = urlrequest.Request(url)
    # req.set_proxy(random.sample(availabe_proxies, 1)[0], 'http')
    page = urlrequest.urlopen(req)
    html = page.read().decode('utf-8')
    return html


def parse_page_size(html):
    soup = BeautifulSoup(html, features="lxml")
    total = soup.find("span", "content__title--hl")
    return int(total.contents[0])


def parse_page(html):
    soup = BeautifulSoup(html, features="lxml")
    result = []
    for content in soup.find_all("div", "content__list--item"):
        try:
            url = content.find(
                "p", "content__list--item--title").find("a")['href']
            des = content.find("p", "content__list--item--des")
            desContents = des.contents
            price = content.find(
                "span",
                "content__list--item-price"
            ).find("em").contents[0]
            district = des.find_all("a")[0].contents[0]
            bizCircle = des.find_all("a")[1].contents[0]
            area = desContents[6].strip("\n").strip(" ").strip("\n")
            direction = desContents[8].strip("\n").strip(" ")
            roomType = desContents[10].strip("\n").strip(" ")
            result.append({
                "price": price,
                "district": district,
                "bizCircle": bizCircle,
                "area": area,
                "direction": direction,
                "roomType": roomType,
                "url": url,
            })
        except:
            pass
    print(result)
    return result


def main():
    for district in districts:
        url = 'https://hz.lianjia.com/zufang/'+district+'/'
        html = get_page(url)
        size = int(parse_page_size(html) / 30)
        print(size)
        for page in range(1, size):
            print(page)
            try:
                url = 'http://hz.lianjia.com/zufang/' + \
                    district + '/pg' + str(page)
                html = get_page(url)
                result = parse_page(html)
                write_to_file(result)
                sleep(2)
            except:
                print("Caught it!")


if __name__ == '__main__':
    main()
