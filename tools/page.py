# coding=utf-8
#
import json
import urllib
from zhubajie.models import Person

__author__ = u'王健'
import os, webapp2, jinja2
#from django.template import loader
from setting import TEMPLATE_DIR
from google.appengine.api import memcache

loginurl = '/login'


class Page(webapp2.RequestHandler):
    def render(self, template_file, template_value):
        jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
        template = jinja_environment.get_template(template_file)
        self.response.out.write(template.render(template_value))

    #        path = os.path.join(TEMPLATE_DIR, template_file)
    #        self.response.out.write(template.render(path,template_value))

    def flush(self, jsonobj):
        if isinstance(jsonobj, (str, unicode)):
            self.response.out.write(jsonobj)
        else:
            self.response.out.write(json.dumps(jsonobj))
        #


    def getResult(self, success, message, result=None, status_code=200, cachename=None, dialog='1'):
        '''
        200 正常返回 code
        201 用户名已经具有
        202 需要验证邮箱
        400 组织余额不足，需要充值后继续使用
        401 用户禁止使用
        402 用户离开了当前组织
        403 需要先选择当前的组织
        404 登录过期，需要重新登录

        dialog 客户端提示类型
        1： 红字 3秒 提示
        2：Alert 提示
        '''
        map = {'success': success, 'message': message, 'status_code': status_code, 'dialog': dialog}
        if result:
            map['result'] = result
        jsonstr = json.dumps(map)
        if cachename:
            memcache.set(cachename, jsonstr, 3600)
        self.response.out.write(jsonstr)



def login_required(fn):
    def auth(*arg):
        web = arg[0]
        user = get_current_user(web)
        if user:
            fn(*arg)
        else:
            #            web.redirect('/paper/234.html','post')
            if web.request.method == 'GET':
                web.redirect(loginurl + '?fromurl=' + web.request.path_url)
            else:
                web.redirect(loginurl + '?fromurl=' + web.request.environ['HTTP_REFERER'])
    return auth


def setLogin(web, user):
    setCookie = 'webusername=' + user.username.encode("utf-8") + ';'
    web.response.headers.add_header('Set-Cookie', setCookie + 'Max-Age = 3600000;path=/;')
    # if user.name:
    #     setCookie = 'webnickname=' + urllib.quote(user.name.encode("utf-8")) + ';'
    #     web.response.headers.add_header('Set-Cookie', setCookie + 'Max-Age = 3600000;path=/;')
    #setCookie=str(setCookie)
    web.response.headers.add_header('Set-Cookie', setCookie + 'Max-Age = 3600000;path=/;')


def setLogout(web):
    setCookie = 'webusername=;'
    web.response.headers.add_header('Set-Cookie', setCookie + 'Max-Age = 3600000;path=/;')
    setCookie = 'webnickname=;'
    web.response.headers.add_header('Set-Cookie', setCookie + 'Max-Age = 3600000;path=/;')
    setCookie = 'auth=;'
    web.response.headers.add_header('Set-Cookie', setCookie + 'Max-Age = 3600000;path=/;')


def get_current_user(web):
    guist = {}
    Cookies = {}  # tempBook Cookies
    Cookies['request_cookie_list'] = [{'key': cookie_key, 'value': cookie_value} for cookie_key, cookie_value in
                                      web.request.cookies.iteritems()]
    for c in Cookies['request_cookie_list']:
        if c['key'] == 'webusername':
            guist["username"] = c['value']
        if c['key'] == 'webnickname':
            guist["name"] = urllib.unquote(c['value'].encode("utf-8"))
        if c['key'] == 'auth':
            guist["auth"] = c['value']
    if guist and guist.has_key('username'):
        user = Person.all().filter('username =', guist['username']).fetch(1)
        if user:
            return user[0]
    return False
