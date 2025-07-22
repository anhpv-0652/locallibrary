from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from . import constants
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import permission_required

import datetime
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.forms import RenewBookForm

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
        'num_visits': num_visits,
    }

    # 3. Kết xuất (render) template HTML và gửi về cho người dùng
    return render(request, 'index.html', context=context)

class BookListView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = constants.BOOK_LIST_VIEW_PAGINATE
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    permission_required = 'catalog.can_see_all_books'

class BookDetailView(PermissionRequiredMixin,LoginRequiredMixin,generic.DetailView):
    model = Book
    permission_required = 'catalog.can_see_all_books'
    
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

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""

    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': constants.DEFAULT_DATE_OF_DEATH}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')