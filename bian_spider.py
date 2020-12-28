# 基于requests、xpath、threading进行多线程爬虫
import requests
import os
from lxml import etree


URL = "http://pic.netbian.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41 "
}


class mySpider(object):
    """
    一个简单的爬虫类，方法有获取url的文本，以及根据xpath表达式查找页面元素
    """

    def __init__(self, url) -> None:
        self._url = url  #_url为目的url
        self._count = 0  #_count为已爬取图片的计数器

    def get_url(self):
        return self._url

    def get_count(self):
        return self._count

    def update_count(self):
        self._count = self._count + 1

    def change_url(self, new_url):
        self._url = new_url

    def getContent(self):
        response = requests.get(url=self._url, headers=headers)
        content = response.content
        return content

    def getPage_text(self):
        response = requests.get(url=self._url, headers=headers)
        response.encoding = 'utf-8'
        page_text = response.text
        return page_text

    def getXpath_emelents(self, xpath_str):
        text = self.getPage_text()
        tree = etree.HTML(text)
        return tree.xpath(xpath_str)

spider = mySpider(URL)

category = {
    '0': '4kdongwu',
    '1': '4kfengjing',
    '2': '4kmeinv',
    '3': '4kyouxi',
    '4': '4kbeijing',
    '5': '4kdongman',
    '6': '4kyingshi',
    '7': '4kmingxing',
    '8': '4kqiche',
    '9': '4krenwu',
    'a': '4kmeishi',
    'A': '4kmeishi',
}


def get_imgurl(url):
    imgurl_list = []
    spider.change_url(url)
    a_list = spider.getXpath_emelents('//*[@id="main"]/div[3]/ul/li/a[1]/@href')
    for a in a_list:
        try:
            imgurl = URL + a
            imgurl_list.append(imgurl)
        except Exception as IndexError:
            print("出小差啦！！！")
            pass
    return imgurl_list

def get_dwldurl(imgurl_list):
    dwldurl_list = []

    for imgurl in imgurl_list:
        try:
            spider.change_url(imgurl)
            dwldurl = URL + spider.getXpath_emelents('//*[@id="img"]/img/@src')[0]
            # print(spider.getPage_text())
            dwldurl_list.append(dwldurl)
        except Exception as IndexError:
            print('出错了')
            pass

    return dwldurl_list


def download(dwldurl_list, dir_name):
    if not os.path.exists('%s' %(dir_name)):
        os.mkdir('./%s' % (dir_name))
    for dwldurl in dwldurl_list:
        spider.change_url(dwldurl)
        with open('./%s/%d.jpg' % (dir_name, spider.get_count()), 'wb') as fp:
            fp.write(spider.getContent())
        print('第%d张照片下载完成' % (spider.get_count()))
        spider.update_count()


# 主函数
if __name__ == '__main__':
    #分区页面的url
    cate_url = ''
    #分区要爬取页的url数组
    url_list = []
    while True:
        os.system("cls")
        print('              -------欢迎打开彼岸图网爬虫软件-------')
        print('               -作者博客地址:https://zhiqin.xyz -')
        print('                       0.爬取动物壁纸')
        print('                       1.爬取风景壁纸')
        print('                       2.爬取美女壁纸')
        print('                       3.爬取游戏壁纸')
        print('                       4.爬取背景壁纸')
        print('                       5.爬取动漫壁纸')
        print('                       6.爬取影视壁纸')
        print('                       7.爬取明星壁纸')
        print('                       8.爬取汽车壁纸')
        print('                       9.爬取人物壁纸')
        print('                       A.爬取美食壁纸')
        print('                       Z.退出')
        print('              --本软件仅供学习分享     by:肤浅的羊--')
        action = input("请输入您的指令：")
        num = 0
        try:
            action = action[0]
        except Exception as IndexError:
            pass
        if (action == 'z') or (action == 'Z'):
            exit()
        elif action:
            try:
                cate_url = URL + category[action]
                print(cate_url)
                url_list.append(cate_url)
                spider.change_url(cate_url)
                print('该分区有' + spider.getXpath_emelents('//*[@id="main"]/div[4]/a[7]/text()')[0] + '页')
                num = input('请输入要爬取多少页：')
                num = int(num)

            except Exception as KeyError:
                print('输入错误，请重新输入')
                os.system("pause")

            if num > 1:
                for i in range(2, num + 1):
                    url_list.append(cate_url + '/index_%d.html' % (i))
            for url in url_list:
                imgurl_list = get_imgurl(url)
                dwldurl_list = get_dwldurl(imgurl_list)
                download(dwldurl_list, category[action])
            os.system("pause")
        else:
            print('输入错误，请重新输入')
            os.system("pause")
