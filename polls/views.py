import json
import re

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .forms import AuthorForm, PaperStep1Form
from .models import Author, Company
from .models import AuthorCompany
from .models import Paper, PaperAuthor
from . import util


# Create your views here.


def add_step1(request):
    if request.method == 'POST':
        form = PaperStep1Form(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            request.session['paper'] = values
            flag = True

            if values['pifpub'] == 'true':
                try:
                    if re.match(r'^\s+$', values['pplace']):
                        flag = False
                    if re.match(r'^\s+$', values['ppub']):
                        flag = False
                    if re.match(r'^\s+$', str(values['pyear'])):
                        flag = False
                    if re.match(r'^\s+$', str(values['ppage'])):
                        flag = False
                    if re.match(r'^\s+$', values['ppath']):
                        flag = False
                except:
                    flag = False

            if flag:
                return HttpResponseRedirect(reverse('polls:add_step2'))
    else:
        paper = request.session.get('paper', {})
        form = PaperStep1Form(initial={
            'pname': paper.get('pname', ''),
            'ptype': paper.get('ptype', ''),
            'pplace': paper.get('pplace', ''),
            'ppub': paper.get('ppub', ''),
            'pyear': paper.get('pyear', ''),
            'ppage': paper.get('ppage', ''),
            'ppath': paper.get('ppath', ''),
        })
    return render(request, 'polls/add-step1.html', {'form': form})


def add_step2(request):
    if request.session.get('paper', None) is None:
        raise Http404()

    authors = request.session.get('authors', [])

    return render(request, 'polls/add-step2.html', {'authors': json.dumps(authors)})


def add_step3(request):
    return render(request, 'polls/add-step3.html', {
        'paper': request.session['paper'],
        'authors': request.session['authors']
    })


def save_paper(request):
    _paper = request.session['paper']
    _paper['pifpub'] = (_paper['pifpub'] == 'true')
    authors = request.session['authors']
    if _paper['pyear'] is None:
        _paper['pyear'] = 0
    if _paper['ppage'] is None:
        _paper['ppage'] = 0
    paper = Paper(**_paper)
    paper.save()

    for i, a in enumerate(authors):
        author = Author.objects.get(amail=a['amail'])
        company = Company.objects.filter(cnamech1=a['cnamech1'], cnamech2=a['cnamech2'])[0]
        pa = PaperAuthor(
            author=author,
            company=company,
            paper=paper,
            paorder=i+1,
            pacommunication=a.get('isComm', False),
            pacorder=a.get('commOrder', 0)
        )
        pa.save()
    del request.session['paper']
    del request.session['authors']
    return HttpResponseRedirect(reverse('login:tables'))


def get_author(request):
    if request.method != 'GET':
        raise Http404()
    name = request.GET.get('name', '')
    if re.match(r'^\s*$', name):
        return JsonResponse({
            'success': False,
            'message': '名字不能为空',
        })
    try:
        author = Author.objects.get(anamech=name)
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '不存在该作者，请添加'
        })

    try:
        ac = AuthorCompany.objects.get(author=author)
        return JsonResponse({
            'success': True,
            'val': {
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
                'cnamech1': ac.company.cnamech1,
                'cnamech2': ac.company.cnamech2,
            }
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': True,
            'val': {
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
            }
        })


def author_list(request):
    if request.method != 'GET':
        raise Http404()
    prefix = request.GET.get('prefix', '')
    if prefix == '':
        raise Http404()
    authors = Author.objects.filter(anamech__startswith=prefix)
    result = []
    for author in authors:
        try:
            ac = AuthorCompany.objects.get(author_id=author.aid)
            result.append({
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
                'cnamech1': ac.company.cnamech1,
                'cnamech2': ac.company.cnamech2,
            })
        except:
            result.append({
                'anamech': author.anamech,
                'anameen': author.anameen,
                'amail': author.amail,
            })
    return HttpResponse(json.dumps(list(result)), content_type="application/json")


@csrf_exempt
def add_authors(request):
    authors = json.loads(request.body.decode('utf-8'))
    if len(authors) == 0:
        return HttpResponse(json.dumps({'success': False, 'message': '至少添加一位作者'}), content_type="application/json")
    tmp = {}
    for a in authors:
        tmp[a['amail']] = a
    if len(tmp) != len(authors):
        return HttpResponse(json.dumps({'success': False, 'message': '添加了重复的作者'}), content_type="application/json")
    if not util.check_comm(authors):
        return HttpResponse(json.dumps({'success': False, 'message': '通信作者顺序有误'}), content_type="application/json")
    request.session['authors'] = authors
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def new_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            try:
                author = Author(
                    anamech=values['anamech'],
                    anameen=values['anameen'],
                    amail=values['amail'],
                )
                author.save()
            except:
                return render(request, 'polls/new-author.html', {'form': form, 'err_msg': '%s已被其他作者占用' % values['amail']})

            try:
                company = Company.objects.get(
                    cnamech1=values['cnamech1'], cnamech2=values['cnamech2']
                )
            except Company.DoesNotExist:
                company = Company(
                    cnamech1=values['cnamech1'],
                    cnameeg1=values['cnameeg1'],
                    cnamech2=values['cnamech2'],
                    cnameeg2=values['cnameeg2'],
                    czipcode=values['czipcode'],
                    addressch=values['addressch'],
                    addressen=values['addressen'],
                )
                company.save()
            ac = AuthorCompany(
                author=author,
                company=company,
                acorder=1,
                accurrent=True,
            )
            ac.save()
            return HttpResponseRedirect(reverse('polls:add_step2'))
    else:
        form = AuthorForm()

    return render(request, 'polls/new-author.html', {'form': form})
