# -*- coding: utf-8 -*-

# Create your views here.
from annoying.decorators import render_to
from att_tech_app.models import *
import math
from django.shortcuts import get_object_or_404

def organize_in_lists(obj_list, l):    # return list of lists of l objects
    result = []
    for i in range(0, len(obj_list), l):
        el = list(obj_list)[i: i+l]  # (0, 1), (2, 3) and so on, for l=2
        result.append(el)
    return result


@render_to('index.html')
def index_page(request):
    index_pictures = IndexPicture.objects.all()
    index_text_blocks = IndexTextBlock.objects.all()[0:3]
    return {
        'index_pictures': index_pictures,
        'index_text_blocks': index_text_blocks,
    }


@render_to('basic_page.html')
def basic_page_view(request, location):
    article = BasicArticle.objects.get(location=location)
    pictures_list = list(article.files_list.all())
    files_list = organize_in_lists(pictures_list, 6)
    return {
        'article': BasicArticle.objects.get(location=location),
        'files_list': files_list,
    }


@render_to('page_with_docs.html')
def page_with_docs_view(request, location):
    article = ArticleWithDocuments.objects.get(location=location)
    return {
        'article': article,
    }


@render_to('employees_page.html')
def employees_page(request):
    discipline_types = map(lambda obj: obj.discipline_type, 
                            DisciplineType.objects.all())
    employees_lists = []
    for d_type in discipline_types:
        employees_lists.append(set([d.tutor for d in 
        Discipline.objects.filter(discipline_type__discipline_type=d_type)]))
    employees_info_block = EmployeesInfoBlock.objects.all()[0].text
    return {
        'discipline_types': discipline_types,
        'employees_lists': employees_lists,
        'employees_info_block': employees_info_block,
    }
    
    
@render_to('masters_page.html')
def masters_page(request):
    masters_list =  Person.objects.filter(master_status=True)
    return {
        'masters_list': masters_list,
    }


@render_to('profs_and_specs_page.html')
def profs_and_specs_page(request):
    pr = Profession.objects.filter(speciality=False)
    sp = Profession.objects.filter(speciality=True)
    return {
        'page_types': [u'Специальности', u'Профессии'],
        'page_items_list': [sp, pr],
    }


@render_to('contacts_page.html')
def contacts_page(request):
    contacts = Contacts.objects.all()[0].contacts
    return {'contacts': contacts,}


def paginate(cur_page, N):
    pages_list = []
    margin = 3
    min_gap = 2
    if N <= 20:
        return range(1, N + 1) 

    if (cur_page - margin) - (margin + 1) > min_gap:
        # first pages, gap and middle (or last) pages
        pages_list.extend(range(1, (margin + 1) + 1))
        pages_list.append(0)
        pages_list.extend(range(cur_page-margin, min((cur_page + margin) + 1,
            N + 1)))
    else:
         # very first pages
        pages_list.extend(range(1, (cur_page + margin) + 1))
    
    if (N - margin) - (cur_page + margin) > min_gap:
        # last pages after gap
        pages_list.append(0)
        pages_list.extend(range(N-margin, N + 1))
    else:
        # last pages without gap
        pages_list.extend(range(cur_page + margin + 1, N + 1))
        
    return pages_list


@render_to('news_page.html')
def news_page(request, page_type):
    news_per_page = 8
    try:
        # if someone trying to hack, page arg can be anytings,
        # so limit it to length 10. enough for page number
        cur_page = int(request.GET.get('page', '1')[:10])
    except:
        cur_page = 1
    if page_type == 'stud_life':
        is_event = True
        N = int(math.ceil(NewCounter.objects.get(id=0).events_number / 
            float(news_per_page)))
    else:
        is_event = False
        N = int(math.ceil(NewCounter.objects.get(id=0).news_number /
            float(news_per_page)))
    if cur_page > N: # can have db error if cur_page, somehow, is too large
        cur_page = N
    obj_list = New.objects.filter(is_event=is_event)
    lower, upper = ((cur_page - 1) * news_per_page, cur_page * news_per_page)
    obj_for_cur_page = obj_list[lower:upper]
    links_list = paginate(cur_page, N)
    return {
        'obj_list': obj_for_cur_page,
        'cur_page': cur_page,
        'is_event': is_event,
        'links_list': links_list,
    }


@render_to('exact_new.html')
def exact_new(request, page_type, new_id):
    new = get_object_or_404(New, pk=int(new_id))
    pictures_list = list(new.pictures_list.all())
    files_list = organize_in_lists(pictures_list, 6)
    return {
        'new': new,
        'files_list': files_list,
    }
