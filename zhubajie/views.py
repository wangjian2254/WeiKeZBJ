# coding=utf-8
# Date:2014/10/14
# Email:wangjian2254@gmail.com
import datetime
import logging
import urllib
from google.appengine.api import urlfetch
from tools.page import Page, setLogout, setLogin, login_required, get_current_user
from zhubajie.bajie import getOnePage
from zhubajie.models import Person, Subject, Task

__author__ = u'王健'


class Logout(Page):
    def get(self, *args):
        setLogout(self)
        self.redirect('/')


class Login(Page):
    def get(self, *args):
        fromurl = self.request.get('fromurl', '/')
        self.render('template/login.html', {'fromurl': fromurl})

    def post(self, *args):
        username = self.request.get('username')
        password = self.request.get('password')
        fromurl = self.request.get('fromurl', None)

        user = Person.all().filter('username =', username).filter('password =', password).fetch(1)
        if user:
            user = user[0]
            setLogin(self, user)
            self.redirect('/subjectlist')
        else:
            self.redirect('/')


class RegUser(Page):
    def get(self):
        person = {'start_time': '08:00', 'end_time': '21:00', 'space': 5}
        self.render('template/reg.html', {'person': person})

    def post(self):
        username = self.request.get('username').strip()
        password = self.request.get('password')
        email = self.request.get('email').strip()
        start_time = self.request.get('start_time').strip()
        end_time = self.request.get('end_time').strip()
        space = self.request.get('space').strip()
        if len(Person.all().filter('username =', username).fetch(1)) == 0:
            try:
                person = Person()
                person.username = username
                person.password = password
                person.email = email
                t = start_time.split(':')
                if len(t) == 1:
                    person.start_time = datetime.datetime(1, 1, 1, hour=int(t[0]))
                else:
                    person.start_time = datetime.datetime(1, 1, 1, hour=int(t[0]), minute=int(t[1]))
                t = end_time.split(':')
                if len(t) == 1:
                    person.end_time = datetime.datetime(1, 1, 1, hour=int(t[0]))
                else:
                    person.end_time = datetime.datetime(1, 1, 1, hour=int(t[0]), minute=int(t[1]))
                person.space = int(space)
                person.save()
                self.redirect('/subjectlist')
            except Exception, e:
                context = {'error': u'数据错误'}
                for k in self.request.POST.keys():
                    context[k] = self.request.get(k)
                self.render('template/reg.html', {'person': context})
        else:
            context = {'error': u'用户名重复'}
            for k in self.request.POST.keys():
                context[k] = self.request.get(k)
            self.render('template/reg.html', {'person': context})


class SubjectList(Page):
    @login_required
    def get(self):
        person = get_current_user(self)
        l = Subject.all().filter('person =', person.key().id())
        self.render('template/subjectlist.html', {'subjects': l})


class SubjectAdd(Page):
    @login_required
    def post(self):
        person = get_current_user(self)
        title = self.request.get('title').strip()
        price = self.request.get('price').strip()

        if title:
            subject = Subject()
            subject.person = person.key().id()
            subject.title = title
            try:
                subject.price = int(price)
            except:
                subject.price = 0
            subject.save()
        self.redirect('/subjectlist')


class SubjectDel(Page):
    @login_required
    def get(self):
        person = get_current_user(self)
        subjectid = self.request.get('subjectid')

        if subjectid:
            subject = Subject.get_by_id(int(subjectid))
            if subject.person == person.key().id():
                subject.delete()
        self.redirect('/subjectlist')


class TaskList(Page):
    @login_required
    def get(self):
        subjectid = self.request.get('subjectid')
        subject = Subject.get_by_id(int(subjectid))
        page = int(self.request.get('page', '0'))

        l = Task.all().filter('subject =', int(subjectid)).fetch(100, page)
        self.render('template/tasklist.html', {'tasklist': l, 'subject': subject})


class TaskSearch(Page):
    def get(self):
        url = 'http://search.zhubajie.com/t/s5.html?'
        keywords = []
        for subject in Subject.all():
            parms = {'kw': subject.title.encode('utf-8')}
            keywords.append((urllib.urlencode(parms), subject.key().id(), subject.person))
        self.searchTask(url, keywords)

    def searchTask(self, url, keywords):
        self.rpcs = []
        for key, subjectid, person in keywords:
            uri = '%s%s' % (url, key)
            rpc = urlfetch.create_rpc(deadline=60)
            rpc.callback = self.rpc_callback(rpc, uri, subjectid, person)
            urlfetch.make_fetch_call(rpc, uri, method='GET', follow_redirects=True)
            self.rpcs.append(rpc)
        for rpc in self.rpcs:
            rpc.wait()

    def rpc_callback(self, rpc, url, subjectid, person):
        return lambda: self.handle_result(rpc, url, subjectid, person)

    def handle_result(self, rpc, url, subjectid, person):
        try:
            result = rpc.get_result()
            # print result.status_code
            if result.status_code == 200:
                html = result.content
                taskList = getOnePage(html)
                for item in taskList:
                    if item.get('href', ''):
                        task = Task.get_by_key_name(item.get('href'))
                        if task and subjectid in task.subject:
                            continue
                        if not task:
                            task = Task(key_name=item.get('href'))
                            task.create_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
                            task.subject = [subjectid]
                        else:
                            task.subject.append(subjectid)
                        task.url = item.get('href')
                        task.title = item.get('title', '')
                        task.reward = item.get('reward', '')
                        task.desc = item.get('summary', '')
                        task.state = item.get('state', '')
                        task.participation = item.get('participation', '')
                        task.time_remaining = item.get('time_remaining', '')
                        task.put()

        except Exception, e:
            logging.error('0000' + str(e) + url)
