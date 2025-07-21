from django.urls import path
from . import views

urlpatterns = [
    # Trang chủ
    path('', views.index, name='index'),

    # Danh sách & chi tiết sách
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Danh sách sách mà user đang mượn
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # CRUD tác giả
    path('author/create/', views.AuthorCreate.as_view(),   name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),

    # Gia hạn sách (thủ thư)
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

