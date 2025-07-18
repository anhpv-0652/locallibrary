from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from . import constants
from django.views import generic
from django.shortcuts import get_object_or_404
def index(request):
    """Hàm view cho trang chủ của trang web."""

    # 1. Lấy dữ liệu từ database
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    
    # Đếm số bản sao sách có sẵn (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact=constants.AVAILABLE).count()
    
    # Đếm số tác giả
    num_authors = Author.objects.count()  # .all() được ngầm định ở đây

    # 2. Gói dữ liệu vào một "túi" (context)
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # 3. Kết xuất (render) template HTML và gửi về cho người dùng
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = constants.BOOK_LIST_VIEW_PAGINATE
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['copies'] = book.bookinstance_set.all()
        context['STATUS_AVAILABLE'] = constants.AVAILABLE
        context['STATUS_MAINTENANCE'] = constants.MAINTENANCE
        context['status_labels'] = dict(constants.LOAN_STATUS)
        return context

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})