# _*_ coding: utf-8 _*_
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from login.models import account
from login.models import Author
from login.models import PaperAuthor
from login.models import Paper
from login.models import Company
from login.models import AuthorCompany
from login.md5 import md5_key
from login.select import select
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    pass
    return redirect('/tables/')

def basic(request):
    if request.session.get('is_login', None) == None:
        return redirect('/login/')
    else:
        return render(request, 'login/basic-form.html')

def finished(request):
    if request.session.get('is_login', None) == None:
        return redirect('/login/')
    else:
        return render(request, 'login/finish.html')

def changepwd(request):
    if request.session.get('is_login', None) == None:
        return redirect('/login/')
    else:
        return render(request, 'login/changepwd.html')
@csrf_exempt
def updatepwd1(request):
    username=request.session.get('user_name')
    inmail = request.POST.get('inmail')
    inqq = request.POST.get('inqq')
    inphone = request.POST.get('inphone')
    if request.session.get('is_login', None) == None:
        message = {'message':'非法','suc':'timeout'}
    else:
        lookfor = account.objects.filter(uaccount = username,umail=inmail,uqq=inqq,uphone=inphone)
        if lookfor:
            message = {'message':'有','suc':'yes'}
        else:
            message = {'message':'请核实您的信息是否正确','suc':'no'}
    return JsonResponse(message)
@csrf_exempt
def updatepwd2(request):
    username=request.session.get('user_name')
    oldpwd = request.POST.get('oldpwd')
    newpwd = request.POST.get('newpwd')
    oldpwd = md5_key(oldpwd)
    newpwd = md5_key(newpwd)
    if request.session.get('is_login', None) == None:
        message = {'message':'非法','suc':'timeout'}
    else:
        lookfor = account.objects.filter(uaccount = username,upassword=oldpwd)
        if lookfor:
            account.objects.filter(uaccount = username).update(upassword=newpwd)
            message = {'message':'修改密码成功，请重新登陆','suc':'yes'}
        else:
            message = {'message':'您输入的旧密码有误，请核实','suc':'no'}
    return JsonResponse(message)

@csrf_exempt
def finish(request):
    usermail=request.session.get('user_mail')
    cnamech1 = request.POST.get('cnamech1')
    cnameeg1 = request.POST.get('cnameeg1')
    cnamech2 = request.POST.get('cnamech2')
    cnameeg2 = request.POST.get('cnameeg2')
    addressen = request.POST.get('addressen')
    addressch = request.POST.get('addressch')
    czipcode = request.POST.get('czipcode')
    if request.session.get('is_login', None) == None:
        message = {'message':'非法','suc':'timeout'}
    else:
        try:
            lookfor = Company.objects.filter(cnamech1=cnamech1,cnamech2=cnamech2,cnameeg1=cnameeg1,cnameeg2=cnameeg2,addressch=addressch,addressen=addressen,czipcode=czipcode)
            if lookfor:
                lookfor1 = Company.objects.get(cnamech1=cnamech1,cnamech2=cnamech2,cnameeg1=cnameeg1,cnameeg2=cnameeg2,addressch=addressch,addressen=addressen,czipcode=czipcode)
                findaid = Author.objects.get(amail = usermail)
                new_ac = AuthorCompany(acorder=1,accurrent=True,author=findaid,company=lookfor1)
                new_ac.save()
                account.objects.filter(umail = usermail).update(uall = True)
                request.session['uall'] = True
                message = {'message':'已有插入成功','suc':'yes'}
            else:
                new_com = Company(cnamech1=cnamech1,cnamech2=cnamech2,cnameeg1=cnameeg1,cnameeg2=cnameeg2,addressch=addressch,addressen=addressen,czipcode=czipcode)
                new_com.save()
                findcid = Company.objects.get(cnamech1=cnamech1,cnamech2=cnamech2,cnameeg1=cnameeg1,cnameeg2=cnameeg2,addressch=addressch,addressen=addressen,czipcode=czipcode)
                findaid = Author.objects.get(amail = usermail)
                new_ac = AuthorCompany(acorder=1,accurrent=True,author=findaid,company=findcid)
                new_ac.save()
                account.objects.filter(umail = usermail).update(uall = True)
                request.session['uall'] = True
                message = {'message':'新建插入成功','suc':'yes'}
        except:
            message = {'message':'服务器内部错误','suc':'no'}
    return JsonResponse(message)


def test1(request):
    pass
    return render(request, 'login/table_1.html')

def tables(request):
    if request.session.get('is_login', None) == None:
        return redirect('/login/')
    else:
        return render(request, 'login/tables.html')

def root(request):
    return HttpResponse("hello world")
@csrf_exempt
def check(request):
    dealtype = request.POST.get("deal_type")
    dealname = request.POST.get("deal_name")
    message=''
    if dealtype == 'username':
        try:
            lookfor = account.objects.get(uaccount=dealname)
            if lookfor:
                message = '用户名已存在'
        except:
            message = ''
    if dealtype == 'umail':
        try:
            lookfor = account.objects.get(umail=dealname)
            if lookfor:
                message = '邮箱已经被注册'
        except:
            message = ''
    if dealtype == 'uphone':
        try:
            lookfor = account.objects.get(uphone=dealname)
            if lookfor:
                message = '手机号已经被注册'
        except:
            message = ''
    if dealtype == 'uqq':
        try:
            lookfor = account.objects.get(uqq=dealname)
            if lookfor:
                message = 'QQ号已经被注册'
        except:
            message = ''
    ret = {'message':message}
    return JsonResponse(ret)



def test(request):
    if request.session.get('is_login', None) == None:
        return redirect('/login/')
    else:
        username = request.session.get('user_name')
        try:
            acc = account.objects.get(uaccount=username)
            if acc.uaccount == username:
                show = select(acc.umail)
            else:
                request.session.flush()
                return render(request, 'login/login.html', {"message": '不安全操作，请重新登陆'})
        except:
            request.session.flush()
            return render(request, 'login/login.html', {"message": '不安全操作，请重新登陆'})
    return JsonResponse(show)


# def test1(request):
#     return render(request,'login/ui-timeline.html')

def login(request):
    if request.session.get('is_login', None) != None:
        return redirect('/tables/')
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if password != None:
            password = md5_key(password)
        message = "用户名密码不能为空"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
        try:
            acc = account.objects.get(uaccount=username)
            if acc.upassword == password:
                # 开始查找论文
                request.session['is_login'] = True
                request.session['user_id'] = acc.uid
                request.session['user_name'] = acc.uaccount
                request.session['user_mail'] = acc.umail
                request.session['namech'] = acc.unamech
                request.session['uall'] = acc.uall
                request.session.set_expiry(60 * 15)
                # return render(request,'login/tables.html',{'RS':RS})
                return redirect('/tables/')
            else:
                message = "密码不正确！"
        except:
            message = "用户名不存在"
        return render(request, 'login/login.html', {"message": message})
    return render(request, 'login/login.html')


def register(request):
    if request.session.get('is_login', None) != None:
        return redirect('/tables/')
    return render(request, 'login/regist.html')

@csrf_exempt
def regist(request):
    if request.session.get('is_login', None) != None:
        return redirect('/tables/')
    # 登录状态下不允许注册
    username = request.POST.get('username', None)
    password = request.POST.get('upassword', None)
    ufnamech = request.POST.get('ufnamech', None)
    ulnamech = request.POST.get('ulnamech', None)
    ufnameen = request.POST.get('ufnameen', None)
    ulnameen = request.POST.get('ulnameen', None)
    umail = request.POST.get('umail', None)
    uphone = request.POST.get('uphone', None)
    uqq = request.POST.get('uqq', None)
    unamech = ufnamech+ulnamech
    unameen = ufnameen+ulnameen
    if password != None:
        password = md5_key(password)
    if not (username and password and umail and unamech and unameen and uphone and uqq):
        message = {'message':'badmess','succ':'您的信息有误，请检查'}
        return JsonResponse(message)
    else:
        user = account.objects.filter(uaccount=username)
        if user:
            message = {'message':'badmess','succ':'用户名重复'}
            return JsonResponse(message)
        mail = account.objects.filter(umail=umail)
        if mail:
            message = {'message':'badmess','succ':'邮箱重复'}
            return JsonResponse(message)
        uph = account.objects.filter(uphone=uphone)
        if uph:
            message = {'message':'badmess','succ':'手机号重复'}
            return JsonResponse(message)
        uq = account.objects.filter(uqq=uqq)
        if uq:
            message = {'message':'badmess','succ':'qq号重复'}
            return JsonResponse(message)
        new_test = account(uaccount=username, unamech=unamech, unameen=unameen, upassword=password,umail=umail ,uphone=uphone, uqq=uqq,uall=False)
        new_test.save()
        # 保存到uaccount的作者表中
        new_uacc = Author(afnamech = ufnamech, alnamech = ulnamech, anamech=unamech, afnameen=ufnameen, alnameen=ulnameen, anameen=unameen, amail=umail)
        new_uacc.save()
        message={'message':'注册成功','succ':'no'}
        return JsonResponse(message)


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/tables/")
    request.session.flush()
    return redirect('/login/')
