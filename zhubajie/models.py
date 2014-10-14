# coding=utf-8
# Date:2014/10/14
#Email:wangjian2254@gmail.com
from google.appengine.ext import db

__author__ = u'王健'


class Person(db.Model):
    username = db.StringProperty()  #本站用户名
    password = db.StringProperty()  #本站用户名
    email = db.EmailProperty()  #电子邮件
    start_time = db.DateTimeProperty()  #通知的开始时段
    end_time = db.DateTimeProperty()  #通知的最后时段
    space = db.IntegerProperty(default=5)  #通知的间隔
    last_notice_time = db.DateTimeProperty()  #最后一次通知时间


class Subject(db.Model):
    person = db.IntegerProperty()  #person 的id
    title = db.StringProperty()  #订阅的关键字
    price = db.IntegerProperty(default=0)  #任务金额



class Task(db.Model):
    title = db.StringProperty()  #标题
    subject = db.ListProperty(item_type=int)  #subject id
    url = db.StringProperty()  #url
    reward = db.StringProperty()  #任务金额
    desc = db.StringProperty()  #任务摘要
    state = db.StringProperty()  #任务状态
    participation = db.StringProperty()  #参与
    time_remaining = db.StringProperty() #剩余时间
    create_time = db.DateTimeProperty()  #创建时间

