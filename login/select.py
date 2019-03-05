# _*_ coding: utf-8 _*_
from django.shortcuts import render,redirect
from django.db import connection
from django.http import HttpResponse
from login.models import account
from login.models import Author
from login.models import PaperAuthor
from login.models import Paper
from login.md5 import md5_key
from django.http import JsonResponse
import json

def select(umail):#通过登录时验证结果集的邮箱来查找
    amail_to_aid = Author.objects.get(amail = umail)
    if amail_to_aid:
    #如果找到了邮箱对应的ID则进行以下查找。
        SQL = "select * from paper where pid IN (SELECT pid FROM paper_author where aid=%d)"%(amail_to_aid.aid)
        cursor = connection.cursor()
        cursor.execute(SQL)
        #使用一个变量来接收查询到的数据，
        #fetchall（）返回查询到的所有数据
        RS = cursor.fetchall()#RS接收的是论文的具体信息
        ## 得到所有aid对应的pid，在pages表张找到所有pid的论文信息并返回给RS
        SQL1 = "SELECT pid FROM paper_author where aid=%d"%(amail_to_aid.aid)
        cursor1 = connection.cursor()
        cursor1.execute(SQL1)
        RS1 = cursor1.fetchall()#RS1用于接收所有aid所对应的pid
        ## 取出所有aid对应的pid
        i=0;
        RS3=[];tmp=[];

        while i<len(RS1):
            temp_SQL='select * from paper_author where pid=%d ORDER BY paorder'%(RS1[i])
            cursor2 = connection.cursor()
            cursor2.execute(temp_SQL)
            tmp = cursor2.fetchall()#tmp[] 接收对应aid(RS1[]中保存),的pid的所有作者信息，表并且通过 paorder排序
            
            if len(tmp)>0:#如果对应的RS1[i]有作者信息
                # j=i
                # while j<len(tmp):
                    # if len(RS1)==1:
                    #     temp_SQL='select anamech from login_useracc where aid in (select aid from login_relation where pid=%d ORDER BY paorder)'%(RS1[j])
                    # if len(RS1)>1:
                    temp_SQL='select anamech from author where aid in (select aid from paper_author where pid=%d ORDER BY paorder)'%(RS1[i])
                    cursor3 = connection.cursor()
                    cursor3.execute(temp_SQL)
                    RS3.append(cursor3.fetchall())
                    # j=j+1
            # if i==0:
            #     return HttpResponse(RS3)
            tmp = []
            i=i+1
        
        show = [[]]*len(RS)
        i=0
        temp = [];temp1 = ''
        
        while i<len(RS):
            temp.append(RS[i][1])#pagename文章名
            temp.append(RS[i][2])#pagepub出版社
            j=0
            while j<len(RS3[i]):
                if j==len(RS3[i])-1:
                    temp1 =  temp1+''+RS3[i][j][0]
                else:
                    temp1 =  temp1+''+RS3[i][j][0]+';&nbsp;&nbsp;'
                j=j+1
            temp.append(temp1) #作者
            show[i]=temp
            temp1 = ''
            temp = []
            i=i+1
        jsonlist = []
        i=0
        while i<len(RS):
            aa = {}
            aa['pages']=show[i][0]
            aa['pubs']=show[i][1]
            aa['account']=show[i][2]
            i=i+1;
            jsonlist.append(aa)
        cc={'test':jsonlist}
        return cc