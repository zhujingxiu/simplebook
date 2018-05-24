from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from management.models import Book, Publisher, Author, AuthorInfo
from django.conf import settings
from .utils import *
import os
import datetime


# Create your views here.


def book_list(request):
    '''
    图书列表
    :param request:
    :return:
    '''

    records = Book.objects.all()
    return render(request, 'index.html', {'records': records})


def book_check(request):
    '''
    图书姓名检查
    :param request:
    :return:
    '''

    name = request.GET.get('name', '')
    query = Book.objects.filter(name=name)
    entry_id = request.GET.get('id', 0)
    if int(entry_id):
        query = query.exclude(id=entry_id)
    return HttpResponse('false' if query.count() else 'true')


def book_ajax(request, entry_id):
    '''
    编辑图书信息
    :param request:
    :param entry_id:
    :return:
    '''
    if int(entry_id):
        book = Book.objects.get(id=entry_id)
        book_ids = book.author.values_list('id')
        book.author_ids = []
        if book_ids:
            book.author_ids = list(book_ids[0])
        title = '编辑图书 {}'.format(book.name)
    else:
        title = '添加图书'
        book = {}
    publishers = Publisher.objects.all()
    authors = Author.objects.all()
    return JsonResponse({'title': title, 'content': render_to_string('book_form.html',
                                                                     {'book': book, 'publishers': publishers,
                                                                      'authors': authors}, request=request)})


def book_save(request):
    '''
    保存图书
    :param request:
    :return:
    '''
    if request.method == 'POST':
        entry_id = request.POST.get('id', False)
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        number = request.POST.get('number', '')
        info = request.POST.get('info', '')
        authors = request.POST.getlist('authors', [])
        publisher = request.POST.get('publisher', 0)
        if entry_id:
            book = Book.objects.get(id=entry_id)
            book.name = name
            book.price = price
            book.info = info
            book.publisher_id = publisher
            book.save()
            if authors:
                book.author.clear()
                book.author.add(*authors)
        else:
            book = Book.objects.create(name=name, price=price, number=number, info=info, publisher_id=publisher)
            if authors:
                book.author.add(*authors)

        return JsonResponse({'code': 1, 'msg': '图书保存成功'})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def book_delete(request, entry_id):
    '''
    删除图书
    :param request:
    :param entry_id:
    :return:
    '''
    if int(entry_id):
        entry = Book.objects.get(id=entry_id)
        entry.delete()
        return JsonResponse({'code': 1, 'msg': '图书删除成功'})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def author_list(request):
    '''
    作者列表
    :param request:
    :return:
    '''
    records = Author.objects.all()
    return render(request, 'author.html', {'records': records})


def author_check(request):
    '''
    作者姓名检查
    :param request:
    :return:
    '''

    name = request.GET.get('name', '')
    query = Author.objects.filter(name=name)
    entry_id = request.GET.get('id', 0)
    if int(entry_id):
        query = query.exclude(id=entry_id)
    return HttpResponse('false' if query.count() else 'true')


def author_ajax(request, entry_id):
    '''
    编辑作者信息
    :param request:
    :param entry_id:
    :return:
    '''
    if int(entry_id):
        author = Author.objects.get(id=entry_id)
        title = '编辑作者 {}'.format(author.name)
    else:
        title = '添加作者'
        author = {}
    return JsonResponse({'title': title, 'content': render_to_string('author_form.html', {'author': author,
                                                                                          'dynasties': AuthorInfo.DYNASTY_CHOICES},
                                                                     request=request)})


def author_save(request):
    '''
    保存作者
    :param request:
    :return:
    '''
    if request.method == 'POST':
        entry_id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        status = request.POST.get('status', 0)
        info_fields = {
            'avatar': request.POST.get('avatar', ''),
            'birthday': request.POST.get('birthday', ''),
            'gender': request.POST.get('gender', 0),
            'native': request.POST.get('native', ''),
            'dynasty': request.POST.get('dynasty', 0),
        }
        if int(entry_id):
            entry = Author.objects.get(id=entry_id)
            entry.name = name
            entry.status = status
            entry.save()
            try:
                info = AuthorInfo.objects.filter(author_id=entry_id)
                if not info.count():
                    raise AuthorInfo.DoesNotExist
            except AuthorInfo.DoesNotExist:
                info_fields.update({'author': entry})
                print(info_fields)
                AuthorInfo.objects.create(**info_fields)
            else:
                info.update(**info_fields)
        else:
            entry = Author.objects.create(name=name, status=int(status))
            # info_fields.update({'author': entry})
            # AuthorInfo.objects.create(**info_fields)

        return JsonResponse({'code': 1, 'msg': '作者保存成功'})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def author_delete(request, entry_id):
    '''
    删除出版社
    :param request:
    :param entry_id:
    :return:
    '''
    if int(entry_id):
        entry = Author.objects.get(id=entry_id)
        if entry.book_authors.count():
            return JsonResponse({'code': 0, 'msg': '已出版图书，不可删除'})
        else:
            entry.delete()
        return JsonResponse({'code': 1, 'msg': '作者删除成功'})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def author_book_del(request, author_id, book_id):
    '''
    删除出版社
    :param request:
    :param author_id:
    :param book_id:
    :return:
    '''
    if int(author_id):
        entry = Author.objects.get(id=author_id)
        entry.book_authors.remove(book_id)
        return JsonResponse({'code': 1, 'msg': '作者{}图书删除成功'.format(entry.name)})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def publisher_list(request):
    '''
    出版社列表
    :param request:
    :return:
    '''
    records = Publisher.objects.all()
    return render(request, 'publisher.html', {'records': records})


def publisher_check(request):
    '''
    出版社名称检查
    :param request:
    :return:
    '''

    name = request.GET.get('name', '')
    query = Publisher.objects.filter(name=name)
    entry_id = request.GET.get('id', 0)
    if int(entry_id):
        query = query.exclude(id=entry_id)
    return HttpResponse('false' if query.count() else 'true')


def publisher_ajax(request, entry_id):
    '''
    编辑出版社信息
    :param request:
    :param entry_id:
    :return:
    '''
    if int(entry_id):
        publisher = Publisher.objects.get(id=entry_id)
        title = '编辑出版社 {}'.format(publisher.name)
    else:
        title = '添加出版社'
        publisher = {}
    return JsonResponse(
        {'title': title, 'content': render_to_string('publisher_form.html', {'publisher': publisher}, request=request)})


def publisher_save(request):
    '''
    保存出版社
    :param request:
    :return:
    '''
    if request.method == 'POST':
        entry_id = request.POST.get('id', False)
        name = request.POST.get('name', '')
        if int(entry_id):
            entry = Publisher.objects.get(id=entry_id)
            entry.name = name
            entry.save()
        else:
            Publisher.objects.create(name=name)

        return JsonResponse({'code': 1, 'msg': '出版社保存成功'})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def publisher_delete(request, entry_id):
    '''
    删除出版社
    :param request:
    :param entry_id:
    :return:
    '''
    if int(entry_id):
        entry = Publisher.objects.get(id=entry_id)
        if entry.book_publishers.count():
            return JsonResponse({'code': 0, 'msg': '已出版图书，不可删除'})
        else:
            entry.delete()
        return JsonResponse({'code': 1, 'msg': '出版社删除成功'})
    return JsonResponse({'code': 0, 'msg': '参数异常'})


def file_upload(request):
    '''
    文件上传
    :param request:
    :return:
    '''
    upload = request.FILES.get('uploads', None)
    if upload:
        date_now = datetime.datetime.now()
        date_path = '%s/%s/' % (date_now.year, date_now.month)
        new_path = ''.join([settings.BASE_DIR, settings.MEDIA_ROOT, date_path])
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        new_name = ''.join([random_str(10), upload.name[upload.name.rindex('.'):]])
        new_file = "%s/%s" % (new_path, new_name)
        with open(new_file, 'wb+') as _file:
            for chunk in upload.chunks():
                _file.write(chunk)
        return JsonResponse(
            {'code': 1, 'name': upload.name, 'path': ''.join([settings.MEDIA_URL, date_path, new_name])})
    return JsonResponse({'code': 0, 'msg': '上传参数异常'})
