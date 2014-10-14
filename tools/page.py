#coding=utf-8
#
import json

__author__ = u'王健'
#import os,webapp2
import os,webapp2,jinja2
#from django.template import loader
from setting import TEMPLATE_DIR
from google.appengine.api import memcache
#from google.appengine.ext.webapp import template


class Page(webapp2.RequestHandler):
    def render(self, template_file, template_value):
        jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
        template = jinja_environment.get_template(template_file)
        self.response.out.write(template.render(template_value))

#        path = os.path.join(TEMPLATE_DIR, template_file)
#        self.response.out.write(template.render(path,template_value))

    def flush(self,jsonobj):
        if isinstance(jsonobj,(str,unicode)):
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
        map = {'success': success, 'message': message, 'status_code': status_code, 'dialog':dialog}
        if result:
            map['result'] = result
        jsonstr = json.dumps(map)
        if cachename:
            memcache.set(cachename, jsonstr, 3600)
        self.response.out.write(jsonstr)
