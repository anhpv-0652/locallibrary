from django.contrib import admin

from .models import Author, Genre, Book, BookInstance




admin.site.register(Genre)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# Định nghĩa lớp admin

class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]



# Đăng ký lớp admin với model tương ứng

admin.site.register(Book, BookAdmin)



class AuthorAdmin(admin.ModelAdmin):

    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]



# Đăng ký lớp admin với model tương ứng

admin.site.register(Author, AuthorAdmin)



class BookInstanceAdmin(admin.ModelAdmin):

    list_filter = ('status', 'due_back')

    fieldsets = (

        (None, {

            'fields': ('book', 'imprint', 'id')

        }),

        ('Availability', {

            'fields': ('status', 'due_back')

        }),

    )



admin.site.register(BookInstance, BookInstanceAdmin)