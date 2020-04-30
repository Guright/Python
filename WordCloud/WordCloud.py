##### 爬取阶段
# 导入模块包
import requests
import re
import jieba
import wordcloud
import json
from bs4 import BeautifulSoup
from datetime import datetime
from imageio import imread

#获取500条新闻
newslist = ['https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=1',
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=2',
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=3',
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=4',
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD%20%E4%B8%AD%E5%9B%BD%E6%8A%97%E7%96%AB%20%E6%96%B0%E5%86%A0%20%E8%82%BA%E7%82%8E&c=news&range=all&num=10',
            'https://search.sina.com.cn/?q=抗疫%20中国%20中国抗疫%20新冠%20肺炎&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=2',
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB+%E4%B8%AD%E5%9B%BD&range=all&c=news&sort=time'
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=2'
            'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page=3']
for i in range(4,45):
    web = 'https://search.sina.com.cn/?q=%E6%8A%97%E7%96%AB%20%E4%B8%AD%E5%9B%BD&c=news&from=&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page='
    web += str(i)
    newslist.append(web)
    

def getnewsdetail(newsurl):                                        #获得单页的新闻内容
    res=requests.get(newsurl)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')
    article=[]                                    #获取文章内容
    for p in soup.select('#artibody p')[:-1]:
        article.append(p.text.strip())
    articleall=' '.join(article)
    return articleall



#获取所有新闻的内容
article_str = ""
for url in newslist:
    res = requests.get(url)#模拟get
    #请求获取链接返回的内容
    res.encoding = 'utf-8'#设置编码格式为utf-8
    soup = BeautifulSoup(res.text, 'html.parser')#前面已经介绍将html文档格式化为一个树形结构，每个节点都是一个对python对象，方便获取节点内容
    for new in soup.select('.box-result'):#BeautifulSoup提供的方法通过select选择想要的html节点类名，标签等，获取到的内容会被放到列表中
        if len(new.select('h2')) > 0:
            #加[0]是因为select获取内容后是放在list列表中[内容,],text可以获取标签中的内容
            article_str += (getnewsdetail(new.select('a')[0]['href']))


##### 词频统计
# 创建一个字典用来统计词语
article_dict = {}
# 对词语首次进行分割
article_jieba = jieba.lcut(article_str)
nouse = ['我们','一个','联想','服务','他们','表示','自己']
# 分割之后加循环，去除一些无用的数据，同时对词语数量进行统计
for data in article_jieba:
    if len(data) == 1 or data in nouse:
        continue
    if data not in article_dict:
        article_dict[data] = 1
    else:
        article_dict[data] += 1
# 定义函数，保存字典中的数字数据
def num(i):
    return i[1]
# 把统计好后的字典数据转换成列表
article_list = list(article_dict.items())
# 对列表中的数据进行排序
article_list.sort(key=num, reverse=True)
# 取出列表中出现最多的二十个词
most = []
for i in article_list[:20]:
    most.append(i)
    print(i)


##### 词云制作阶段
# 定义一个变量用来存放要做词云的字符
cloud_data = ''
# 把爬出来的字符放到该变量中
for word in article_list:
    if word in most:
        cloud_data += word[0] + ' '
# 创建一个词云的面板
# 设置词语图片
mask = imread(r'E:\Users\13196\Documents\课\Python课程设计基础\timg.jpg')
w = wordcloud.WordCloud(font_path = r"E:\Users\13196\Documents\课\Python课程设计基础\simsunttc\simsun.ttc",  mask=mask, width=800, height=600, background_color="black")
# 将字符写入到词云面板里面
# w.generate(shoe_name_jieba)
w.generate(cloud_data)
# 输出制作好的词云
w.to_file(r"E:\Users\13196\Documents\课\Python课程设计基础\词云.png")
