from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from . import constants
def index(request):
    """Hàm view cho trang chủ của trang web."""

    # 1. Lấy dữ liệu từ database
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    
    # Đếm số bản sao sách có sẵn (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact=constants.AVAILABLE).count()
    
    # Đếm số tác giả
    num_authors = Author.objects.count()  # .all() được ngầm định ở đây
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    # 2. Gói dữ liệu vào một "túi" (context)
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # 3. Kết xuất (render) template HTML và gửi về cho người dùng
    return render(request, 'index.html', context=context)
    