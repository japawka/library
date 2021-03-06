from django.contrib import admin
from .models import Book, Genre, Author, Language, BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "display_genre"]
   # list_filter = ("title", "genre", "author")

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ("status", "due_back")
    fieldsets = (
        ('Data', {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

admin.site.register(Genre)
# admin.site.register(Author)
admin.site.register(Language)
