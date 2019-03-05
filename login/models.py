# _*_ coding: utf-8 _*_
from django.db import models

""" 1.我的models只创建了4个与功能有关的表，可能名字不太相同
    2.由于在models中设置自增，就无法设置老板要求的格式，所以先创建models，满足字段类型的要求，再生出数据库以及对应表，
    然后在数据库中修改自增属性。
    3.我连接的是我电脑本地的mySQL数据库，但是字段名是一样的
"""
#创建定长的char方法，但是数据库报错没有使用
class MyCharField(models.Field):
    """
    自定义的 char 类型的字段
    """
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(MyCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length

#用户表
class account(models.Model):
    '''用户表'''
    uid = models.BigAutoField(primary_key=True)  # 要在数据库中设置字段自增
    uaccount = models.CharField(max_length=100, unique=True)
    unamech = models.CharField(max_length=100)
    unameen = models.CharField(max_length=100)
    upassword = models.CharField(max_length=100)
    umail = models.CharField(max_length=100, unique=True)
    uphone = MyCharField(max_length=11)
    uqq = models.CharField(max_length=100, unique=True)
    uwechat = models.CharField(max_length=100, unique=True)
    # c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'
    # class Meta:
    #     ordering = ['c_time']
    #     verbose_name = '用户'
    #     verbose_name_plural = '用户'



# Create your models here.
#作者表
class Author(models.Model):
    aid = models.BigAutoField(primary_key=True)
    anamech = models.CharField(max_length=1000)
    anameen = models.CharField(max_length=1000)
    amail = models.EmailField(max_length=100, unique=True)

    class Meta:
        db_table = 'author'


class Company(models.Model):
    cid = models.BigAutoField(primary_key=True)
    cnamech1 = models.CharField(max_length=1000)
    cnameeg1 = models.CharField(max_length=1000)
    cnamech2 = models.CharField(max_length=1000)
    cnameeg2 = models.CharField(max_length=1000)
    czipcode = models.CharField(max_length=1000)
    addressch = models.CharField(max_length=1000)
    addressen = models.CharField(max_length=1000)

    class Meta:
        db_table = 'company'


class AuthorCompany(models.Model):
    acid = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='aid')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='cid')
    acorder = models.SmallIntegerField()
    accurrent = models.BooleanField()

    class Meta:
        db_table = 'author_company'


class Paper(models.Model):
    pid = models.BigAutoField(primary_key=True)
    pname = models.CharField(max_length=1000)
    ptype = models.CharField(max_length=10)
    pifpub = models.BooleanField()
    pplace = models.CharField(max_length=1000)
    ppub = models.CharField(max_length=1000)
    pyear = models.IntegerField()
    ppage = models.BigIntegerField()
    ppath = models.CharField(max_length=1000)

    class Meta:
        db_table = 'paper'


class PaperAuthor(models.Model):
    paid = models.BigAutoField(primary_key=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, db_column='pid')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='aid')
    paorder = models.SmallIntegerField()
    pacommunication = models.BooleanField()
    pacorder = models.SmallIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'paper_author'