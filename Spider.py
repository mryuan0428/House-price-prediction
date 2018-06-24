# coding=utf8
# 用于爬取房源信息
import requests
from bs4 import BeautifulSoup
import os
import multiprocessing
import json
import re

# 爬虫函数，爬取单个区域所有房源信息
# areaName 区域名称
# url 区域url
def Spider(areaName, url):
    host = "https://sh.lianjia.com"
    # labels = ['ID', '标题', '副标题', '总价', '总价单位', '均价', '小区名称', '所在区域', '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型',
    #           '房屋朝向', '建筑结构', '装修情况', '梯户比例', '配备电梯', '产权年限', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息',
    #           '房本备件', '房源标签', '税费解析', '交通出行', '核心卖点', '别墅类型', '售房详情', '周边配套', '小区介绍', '户型介绍', '装修描述', '权属抵押', '适宜人群',
    #           '投资分析']
    # file = open('data/' + areaName + '.csv', 'w', newline='')
    # writer = csv.writer(file)
    # writer.writerow(labels)
    # file.close()

    saUrl = url
    # 打开当前区域列表
    tmpMain = requests.get(host + saUrl).text
    tmpMainSoup = BeautifulSoup(tmpMain)
    # 获得总页数total
    total = eval(tmpMainSoup.select(
        'div[class="page-box house-lst-page-box"]'
    )[0].get("page-data"))['totalPage']

    print("Reading %s" % areaName)
    # 打开所写入的文件
    with open('data/' + areaName + '.json', 'w') as File:
        houses = []
        # 遍历列表每一页
        for i in range(1, total + 1):
            print("area", areaName, "page", str(i), "in", str(total))
            # writer = csv.writer(csvFile)
            listPageUrl = host + saUrl + "/pg%d/" % i
            # 获得网页html
            listPage = BeautifulSoup(requests.get(listPageUrl).text)
            # 获得本页中所有房源详细信息页面url
            singlePageUrls = listPage.select('div[class="title"] > a')
            for j in singlePageUrls:
                # 爬取网页中所有信息
                house = {}
                url = j.get('href')
                house['ID'] = re.findall('https://sh.lianjia.com/ershoufang/(\d*).html', url)[0]
                singlePage = BeautifulSoup(requests.get(url).text)

                overview = singlePage.select('div[class="overview"]')[0]
                house["标题"] = singlePage.select('div[class="title"] > h1')[0].string
                house["副标题"] = singlePage.select('div[class="title"] > div')[0].string
                house["总价"] = overview.select('span[class="total"]')[0].string
                house["总价单位"] = overview.select('span[class="unit"] > span')[0].string
                house["均价"] = overview.select('div[class="unitPrice"]')[0].text
                house["小区名称"] = overview.select('div[class="communityName"] > a[target="_blank"]')[0].string
                house["所在区域"] = overview.select('div[class="areaName"] > span[class="info"]')[0].text.replace('\xa0',
                                                                                                              ' ')
                # 基本信息
                base = singlePage.select('div[class="base"] > div[class="content"] > ul > li')
                for node in base:
                    name, value = node.contents
                    name = name.string
                    # if name not in labels:
                    #     labels.append(name)
                    house[name] = value

                # 交易信息
                transaction = singlePage.select('div[class="transaction"] > div[class="content"] > ul > li')
                for node in transaction:
                    name, value = node.select('span')
                    name, value = name.string, value.string.strip()
                    # if name not in labels:
                    #     labels.append(name)
                    house[name] = value

                # 房源优势
                features = singlePage.find_all('div', class_=["tags", "baseattribute"])
                for node in features:
                    name = node.select('div[class="name"]')[0].string
                    value = node.select('div[class="content"]')[0].text.strip()
                    # if name not in labels:
                    #     labels.append(name)
                    house[name] = value

                # writeRow = []
                # for key in labels:
                #     if key in house:
                #         writeRow.append(house[key])
                #     else:
                #         writeRow.append('')
                houses.append(house)
        # 写入文件
        json.dump(houses, File)


if __name__ == '__main__':
    # mainUrl = "/ershoufang/"
    # mainPage = requests.get(host+mainUrl).text
    # mainPageSoup = BeautifulSoup(mainPage)
    # largeAreas = mainPageSoup.select('div[data-role="ershoufang"] > div')[0].select('a')
    # smallAreas = {}
    # for la in largeAreas:
    #     print("读取%s地区" % la.string)
    #     laUrl = la.get('href')
    #     urlList = BeautifulSoup(requests.get(host+laUrl).text).select('div[data-role="ershoufang"] > div')[1].select('a')
    #     for sa in urlList:
    #         smallAreas[sa.string] = sa.get('href')
    exist = [x[:-5] for x in os.listdir("data/")]
    urlFile = open('url.txt', 'r')
    smallAreas = json.load(urlFile)
    urlFile.close()
    # Spider("虹桥", smallAreas["虹桥"])

    p = multiprocessing.Pool()
    for a in smallAreas:
        if a not in exist:
            p.apply_async(Spider, args=(a, smallAreas[a]))
    p.close()
    p.join()
    print('finish')
