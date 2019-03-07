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


def regist(request):
    if request.session.get('is_login', None) != None:
        return redirect('/tables/')
    # 登录状态下不允许注册
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    umail = request.POST.get('umail', None)
    unamech = request.POST.get('unamech', None)
    unameen = request.POST.get('unameen', None)
    uphone = request.POST.get('uphone', None)
    uqq = request.POST.get('uqq', None)
    uwechat = request.POST.get('uwechat', None)
    cnamech1 = request.POST.get('cnamech1', None)
    cnameeg1 = request.POST.get('cnameeg1', None)
    cnamech2 = request.POST.get('cnamech2', None)
    cnameeg2 = request.POST.get('cnameeg2', None)
    czipcode = request.POST.get('czipcode', None)
    addressch = request.POST.get('addressch', None)
    addressen = request.POST.get('addressen', None)
    message = ''
    if password != None:
        password = md5_key(password)
    if not (
            username and password and umail and unamech and unameen and uphone and uqq and uwechat and cnamech1 and cnameeg1 and cnamech2 and cnameeg2 and czipcode and addressch and addressen):
        if request.session.get('is_login', None) == None:
            return render(request, 'login/regist.html', {"message": message})
        message = '请全部填写'
        return render(request, 'login/regist.html', {"message": message})
    else:
        acc = account.objects.filter(uaccount=username)
        uma = account.objects.filter(umail=umail)
        uq = account.objects.filter(uqq=uqq)
        uwe = account.objects.filter(uwechat=uwechat)
        ch1 = Company.objects.filter(cnamech1=cnamech1, cnameeg1=cnameeg1, cnamech2=cnamech2, cnameeg2=cnameeg2,
                                     czipcode=czipcode, addressch=addressch, addressen=addressen)
        if acc:
            message = "用户已经存在"
            return render(request, 'login/regist.html', {"message": message})
        if uma:
            message = "邮箱已经被注册"
            return render(request, 'login/regist.html', {"message": message})
        if uq:
            message = "qq已经被注册"
            return render(request, 'login/regist.html', {"message": message})
        if uwe:
            message = "微信已经被注册"
            return render(request, 'login/regist.html', {"message": message})
        if ch1:
            pass
        else:
            new_company = Company(cnamech1=cnamech1, cnameeg1=cnameeg1, cnamech2=cnamech2, cnameeg2=cnameeg2,
                                  czipcode=czipcode, addressch=addressch, addressen=addressen)
            new_company.save()

        # 保存到account的用户表中
        new_test = account(uaccount=username, unamech=unamech, unameen=unameen, umail=umail, upassword=password,
                           uphone=uphone, uqq=uqq, uwechat=uwechat)
        new_test.save()
        # 保存到uaccount的作者表中
        new_uacc = Author(anamech=unamech, anameen=unameen, amail=umail)
        new_uacc.save()
        find_aid = Author.objects.get(amail=umail)
        find_cid = Company.objects.get(cnamech1=cnamech1, cnameeg1=cnameeg1, cnamech2=cnamech2, cnameeg2=cnameeg2,
                                       czipcode=czipcode, addressch=addressch, addressen=addressen)
        find_aid1 = Author.objects.get(aid=find_aid.aid)
        find_cid1 = Company.objects.get(cid=find_cid.cid)
        new_find = AuthorCompany(acorder=0, accurrent=0, company=find_cid1, author=find_aid1)
        new_find.save()
        return redirect('/login/')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/tables/")
    request.session.flush()
    return redirect('/login/')
