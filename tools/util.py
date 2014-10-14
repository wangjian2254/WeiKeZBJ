#coding=utf-8
import re
import string
from jinja2 import filters
from jinja2.filters import environmentfilter

from setting import IsPassword

__author__ = 'wangjian2254'
c='\n'
schar='s'
fchar='-'
lchar='10'
def replaceStr(strs,s=None):
    if strs and strs.find(c)>-1:
        strs,n=re.subn('[\n]+',s or '',strs.replace('\r','').replace(s,c).lstrip(c))
        return strs
    else:
        return strs

    
def getLevelByCode(strs):
    if strs:
        l=strs.split(schar)
        if len(l)==1:
            return str(len(l[0].split(fchar)))
        else:
            return lchar+str(len(l[1].split(fchar))-1)
    else:
        return '1'

def AutoCode(father,prev,next):
    numlist=['0','1','2','3','4','5','6','7','8','9']
    if prev and  prev[-1] not in numlist:
        prev=prev[:-1]
    if next and next[-1] not in numlist:
        next=next[:-1]
    prevLength = int(getLevelByCode(prev))
    nextLength = int(getLevelByCode(next))
    if (prevLength == 1 and nextLength == 1 and father==''):
      #说明是父类层
      if (prev =='' and next ==''):
        #说明目前没有父类层的资讯,maincode 为空
        newAddCode = 'a4'
        return newAddCode;
      elif (prev=='' and next !=''):
        prev_Part_Str = PartingString(next)
        next_Part_Str = NextString(next)
        is_Special_Point = isSpecialPoint(next_Part_Str)
        no_Letter_Part = isContainLetter(next_Part_Str)
        newCode = Rule(prev,no_Letter_Part)
        if (is_Special_Point==0):
          return (prev_Part_Str+'a'+newCode)
        elif (is_Special_Point==1):
          return (prev_Part_Str+'s'+newCode)
        else:
          return (prev_Part_Str+newCode)
      elif (prev!='' and next ==''):
        prev_Part_Str = PartingString(prev)
        next_Part_Str = NextString(prev)
        is_Special_Point = isSpecialPoint(next_Part_Str)
        no_Letter_Part = isContainLetter(next_Part_Str)
        newCode = Rule(no_Letter_Part,next)
        if (is_Special_Point==0):
          return (prev_Part_Str+'a'+newCode)
        elif (is_Special_Point==1):
          return (prev_Part_Str+'s'+newCode)
        else:
          return (prev_Part_Str+newCode)
      else:
        prev_Part_Str_1 = PartingString(prev)
        next_Part_Str_1 = NextString(prev)
        is_Special_Point_1 = isSpecialPoint(next_Part_Str_1)
        no_Letter_Part_1 = isContainLetter(next_Part_Str_1)
        prev_Part_Str_2 = PartingString(next)
        next_Part_Str_2 = NextString(next)
        is_Special_Point_2 = isSpecialPoint(next_Part_Str_2)
        no_Letter_Part_2 = isContainLetter(next_Part_Str_2)
        newCode = Rule(no_Letter_Part_1,no_Letter_Part_2)
        if (is_Special_Point_2==0):
          return (prev_Part_Str_2+'a'+newCode)
        elif (is_Special_Point_2==1):
          return (prev_Part_Str_2+'s'+newCode)
        else:
          return (prev_Part_Str_2+newCode)
    else:
      fatherLength = int(getLevelByCode(father))
      if (prev =='' and next ==''):
        #说明目前没有父类层的资讯,maincode 为空
        newAddCode = father+'-4'
        return newAddCode;
      elif (prev=='' and next !=''):
        prev_Part_Str = PartingString(next)
        next_Part_Str = NextString(next)
        is_Special_Point = isSpecialPoint(next_Part_Str)
        no_Letter_Part = isContainLetter(next_Part_Str)
        newCode = Rule(prev,no_Letter_Part)
        if (is_Special_Point==0):
          return (prev_Part_Str+'a'+newCode)
        elif (is_Special_Point==1):
          return (prev_Part_Str+'s'+newCode)
        else:
          return (prev_Part_Str+newCode)
      elif (prev!='' and next ==''):
        prev_Part_Str = PartingString(prev)
        next_Part_Str = NextString(prev)
        is_Special_Point = isSpecialPoint(next_Part_Str)
        no_Letter_Part = isContainLetter(next_Part_Str)
        newCode = Rule(no_Letter_Part,next)
        if (is_Special_Point==0):
          return (prev_Part_Str+'a'+newCode)
        elif (is_Special_Point==1):
          return (prev_Part_Str+'s'+newCode)
        else:
          return (prev_Part_Str+newCode)
      else:
        prev_Part_Str_1 = PartingString(prev)
        next_Part_Str_1 = NextString(prev)
        is_Special_Point_1 = isSpecialPoint(next_Part_Str_1)
        no_Letter_Part_1 = isContainLetter(next_Part_Str_1)
        prev_Part_Str_2 = PartingString(next)
        next_Part_Str_2 = NextString(next)
        is_Special_Point_2 = isSpecialPoint(next_Part_Str_2)
        no_Letter_Part_2 = isContainLetter(next_Part_Str_2)
        newCode = Rule(no_Letter_Part_1,no_Letter_Part_2)
        if (is_Special_Point_2==0):
          return (prev_Part_Str_2+'a'+newCode)
        elif (is_Special_Point_2==1):
          return (prev_Part_Str_2+'s'+newCode)
        else:
          return (prev_Part_Str_2+newCode)

def Rule(prev,next):
    if (prev==''):
      prev = '0'
    if (next==''):
      next = '9'

    if (len(prev)>len(next)):
      for i in range(len(prev)-len(next)):
        next = next+'0'
      length = len(next)
    elif (len(prev)<len(next)):
      for i in range(len(next)-len(prev)):
        prev = prev+'0'
        length = len(next)
    elif(len(prev)==len(next)):
        length = len(next)

    prev = string.atoi(prev)
    next = string.atoi(next)

    if ( length>len(str(next))):
      #说明next数字部分是以0开头的，要特殊处理
        if (prev ==0 and next == 1):
            code = isRide10(prev,next)
            for i in range(length):
                code = '0'+code
            return code
        else:
            length_next = length - len(str(next))
            code = isRide10(prev,next)
            for i in range(length_next):
                code = '0'+code
            return code
    else:
        if (prev ==0 and next == 1):
            code = isRide10(prev,next)
            for i in range(length):
                code = '0'+code
            return code
        else:
            if ((next-prev)==1):#等于1，两数相加后除2时，会有小数，应乘以10
                code = isRide10(prev,next)
                for i in range(length-len(str(prev))):
                    code = '0'+code
                return code
            else:
                code = isRide10(prev,next)
                for i in range(length-len(code)):
                    code = '0'+code
                return code

#是否要乘以10
def isRide10(prev,next):
    if((next-prev)==1):
      code = str(((next+prev)*10)/2)
    else:
      code = str((next+prev)/2)
    return code


def PartingString(strName):
    strlist = strName.split('-')
    sameStr = ''
    listLength = len(strlist)
    for i in range(listLength-1):
      sameStr = sameStr + strlist[i]+"-"
    return sameStr

def NextString(strName):
    strlist = strName.split('-')
    sameStr = ''
    listLength = len(strlist)
    sameStr =strlist[listLength-1]
    return sameStr

#是否包含字母
def isContainLetter(next_Part_Str):
    isA = next_Part_Str.find('a')
    if (isA==0):#存在a开头的字符
      a = next_Part_Str[1:]
    elif (isA==-1):
      isS = next_Part_Str.find('s')#特殊节点
      if (isS == 0):
        a = next_Part_Str[1:]
      elif (isS == -1):
        a = next_Part_Str
    return a

def isSpecialPoint(next_Part_Str):
    isA = next_Part_Str.find('a')
    if (isA==0):
      return 0
    elif(next_Part_Str.find('s')==0):
      return 1
    else:
      return -1

def getMainCode(code):
    codelist = code.split('-')
    return codelist[0]

#特殊节点
#将code再分解，确定是否要加's'标记
def getReplyCode(code):
    codeStr = ''
    codelist = code.split('-')
    codeLength = len(codelist)
    for i in range(codeLength):
      if (codelist[i].find('s')==0):
        codeStr = code
        return codeStr
      else:
        if(i==(codeLength-1)):
          codeStr = codeStr +('s'+codelist[i])
        else:
          if(i==(codeLength-1)):
            codeStr = codeStr + codelist[i]
          else:
            codeStr = codeStr + codelist[i]+"-"
    return codeStr

def getPageing(index,page=0):
    s="/%s"
    if page==0:
        if index==16:return (None,"/1")
        else:return (None,None)
    if index==16:
        return ("/",s%(page+1)) if page==1 else (s %(page-1),s%(page+1))
    return ("/",None) if page==1 else (s %(page-1),None)

# def checkUser(self):#验证是否具有这个用户
#     if not IsPassword:
#         return True
#     username=self.request.get('UserName')
#     password=self.request.get('UserPwd')
#     if not username or not password:
#         return False
# #    greetings = db.GqlQuery("SELECT * FROM User where userName=:1 and passWord=:2",UserName,UserPwd)
#     if 1== User.all().filter('userName =',username).filter('passWord =',password).count():
#         return True
#     else:
#         return False


def getResult(result,success=True,message=u''):
    return {'result':result,'success':success,'message':message}


def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)


filters.FILTERS['datetimeformat'] = datetimeformat
