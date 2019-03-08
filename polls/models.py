from django.db import models
# Create your models here.


class Author(models.Model):
    aid = models.BigAutoField(primary_key=True)
    afnamech = models.CharField(max_length=1000)
    alnamech = models.CharField(max_length=1000)
    anamech = models.CharField(max_length=1000)
    afnameen = models.CharField(max_length=1000)
    alnameen = models.CharField(max_length=1000)
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

