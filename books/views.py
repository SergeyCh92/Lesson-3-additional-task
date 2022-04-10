from django.shortcuts import render
from books.models import Book
import datetime
from django.core.paginator import Paginator


def books_view(request):
    template = 'books/books_list.html'
    book_object = Book.objects.all()
    books = [book for book in book_object]
    context = {'books': books}
    return render(request, template, context)


def book_view_date(request, pub_date):
    template = 'books/books_list copy.html'
    pub_date = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
    # book_object = Book.objects.filter(pub_date=pub_date)
    book_object = Book.objects.all()
    books = [book for book in book_object]
    books.sort(key=lambda x: x.pub_date)
    date_list = [book.pub_date for book in Book.objects.all()]
    date_list.sort()
    number_page = int(request.GET.get('page', date_list.index(pub_date.date()) + 1))
    pagi = Paginator(books, 1)
    page = pagi.get_page(number_page)
    index_date = date_list.index(page.object_list[0].pub_date)
    try:
        last_date = date_list[index_date - 1]
        next_date = date_list[index_date + 1]
    except Exception:
        if last_date:
            context = {'page': page, 'last_date': last_date}
            return render(request, template, context)
        else:
            context = {'page': page, 'next_date': next_date}
            return render(request, template, context)
    context = {'page': page, 'last_date': last_date, 'next_date': next_date}
    return render(request, template, context)
