#coding:utf-8
'''
code by Stu.
公众号：安全黑板报
'''

from threading import Timer
from wxpy import *
import requests,re
import feedparser
from bs4 import BeautifulSoup


bot = Bot(console_qr=2)#windows运行console_qr设置为0
links= ""

#secwiki 源
def secwiki():
    global links
    try:
        secwiki= "https://www.sec-wiki.com/news/rss"
        rs1 = feedparser.parse(secwiki)
        html = rs1.entries[0]["summary_detail"]["value"]
        soup = BeautifulSoup(html, 'html.parser')
        for k in soup.find_all('a'):
            if "SecWiki" == k.string:
                pass
            else:
                link1 = (k.string)+":"+k['href']+"\n"
                links += link1
        return "ok"
    except:
        return "secwiki is no ok"

#52bug 爬取一页
def bug52():
    global links
    try:
        bug52_url ="http://www.52bug.cn/sec"
        link2_url = requests.get(bug52_url).text
        reg_url = r'<a href="(.*?)html" title="'
        reg_tit = r'<a href=".*?html" title="(.*?)"'
        pattern= re.compile(reg_url)
        tags_url= re.findall(pattern, link2_url)

        pattern= re.compile(reg_tit)
        tags_tit= re.findall(pattern, link2_url)
        for x in range(len(tags_url)):
            link2 = tags_tit[x]+":"+tags_url[x]+"\n"
            links += link2
        return "ok"
    except :
        return "bug52 is no ok"

#wiki.inio
def wikiinio():
    global links
    try:
        url ="http://wiki.ioin.in/"
        link3_url = requests.get(url).text
        reg_url = r'<a href="(.*?)" class="visit-color"'
        reg_tit = r'visit-color" target="_blank">(.*?)</a>'
        pattern= re.compile(reg_url)
        tags_url= re.findall(pattern, link3_url)
        pattern= re.compile(reg_tit,re.DOTALL)#re.DOTALL,可以让正则表达式中的点（.）匹配包括换行符在内的任意字符。
        tags_tit= re.findall(pattern, link3_url)
        for x in range(len(tags_url)):
            link3 = tags_tit[x].strip()+":"+"http://wiki.ioin.in"+tags_url[x]+"\n"
            links += link3
        return "ok"
    except :
        return "wikiinio is no ok"

# freebuf 源
def freebuf():
    global links
    try:
        freebuf= "https://www.freebuf.com/feed"
        rs1 = feedparser.parse(freebuf)
        l = len(rs1.entries)
        for buf in range(l):
            try:
                url_f = rs1.entries[buf]["link"]
                title_f = rs1.entries[buf]["title_detail"]["value"]
                link4 = title_f+":"+url_f+"\n"
                links += link4
            except:
                break
        return "ok"
    except :
        return "freebuf is no ok"

def send_news():
    try:
        secwiki()
        bug52()
        wikiinio()
        freebuf()

        # 给指定人发送将微信昵称(不是备注、不是微信号)换成需要发送的人即可
        # my_friend = bot.friends().search(u'微信昵称')[0]
        # my_friend.send(links)
        
        my_group = bot.groups().search(u'安全黑板报')[0]
        my_group.send(links)
        
        # 每86400秒(=1天)发送1次
        t = Timer(86400, send_news)
        t.start()
    except Exception, e:
        my_friend = bot.friends().search(u'stu')[0]#发送失败时微信提示Stu，该处也是微信昵称
        my_friend.send(u"今天消息发送失败了")

if __name__ == "__main__":
    send_news()
