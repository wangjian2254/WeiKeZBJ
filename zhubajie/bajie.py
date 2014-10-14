# coding=utf-8
import urllib
import httplib,urllib
from bs4 import BeautifulSoup

__author__ = 'fanjunwei003'


def getHtml(url):

    f=urllib.urlopen(url)
    html=f.read()
    return html
def getTaskList(keyword):
    parms={
        'kw':keyword
    }
    url='http://search.zhubajie.com/t/s5.html?'+urllib.urlencode(parms)
    taskList=[]
    while url:
        html=getHtml(url)
        url=None
        #获取下一页链接
        taskList.append(getOnePage(html))
        soup = BeautifulSoup(html)
        links=soup.find_all('a')
        for i in links:
            if i.get_text() == u"»":
                url=i.get('href').encode('utf8')
                break




def getOnePage(html):
    soup = BeautifulSoup(html)
    tables=soup.find_all('table')
    count = len(tables)
    taskList=[]
    for t in tables:
        cssClass = t.get('class')
        if cssClass and cssClass[0]=='list-task':
            tableRows=t.find_all('tr')
            for row in tableRows:
                print '==================================='
                taskItem={}
                tags=row.find_all()
                for i in tags:
                    cssClass = i.get('class')
                    if cssClass and cssClass[0]=='list-task-reward':
                        #金额
                        taskItem['reward']=i.get_text()
                        print i.get_text()
                    if cssClass and cssClass[0]=='list-task-title':
                        #标题
                        taskItem['title']=i.get_text()
                        taskItem['href']=i.get('href')
                        print i.get_text()
                        print taskItem['href']
                    if cssClass and cssClass[0]=='list-task-ctn':
                        #摘要
                        taskItem['summary']=i.get_text()
                        print i.get_text()
                    if cssClass and cssClass[0]=='list-task-trusteeship':
                        #状态
                        taskItem['state']=i.get_text()
                        print i.get_text()

                tds=row.find_all('td')

                #参与
                taskItem['participation']= tds[2].get_text()
                print tds[2].get_text()

                #剩余时间
                taskItem['time_remaining']= tds[3].get_text()
                print tds[3].get_text()


                taskList.append(taskItem)
    return taskList


def main():

    print getTaskList('微信')

main()