"""simplebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from management import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^filemanager/upload/?$', views.file_upload,name='file_upload'),

    url(r'^book/?$', views.book_list, name='books'),
    url(r'^book/check_name/?$', views.book_check, name='book_check'),
    url(r'^book/save/$', views.book_save, name='book_save'),
    url(r'^book/form/?(\d+)?/?$', views.book_ajax),
    url(r'^book/delete/(\d+)/?$', views.book_delete),

    url(r'^author/?$', views.author_list, name='authors'),
    url(r'^author/check_name/?$', views.author_check, name='author_check'),
    url(r'^author/save/$', views.author_save, name='author_save'),
    url(r'^author/form/?(\d+)?/?$', views.author_ajax),
    url(r'^author/delete/(\d+)/?$', views.author_delete),
    url(r'^author/book_del/(?P<author_id>\d+)/(?P<book_id>\d+)/?$', views.author_book_del),

    url(r'^publisher/?$', views.publisher_list, name='publishers'),
    url(r'^publisher/check_name/?$', views.publisher_check, name='publisher_check'),
    url(r'^publisher/save/$', views.publisher_save, name='publisher_save'),
    url(r'^publisher/form/?(\d+)?/?$', views.publisher_ajax),
    url(r'^publisher/delete/(\d+)/?$', views.publisher_delete),
]