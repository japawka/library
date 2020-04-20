from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from catalog.forms import RenewBookForm, RenewBookModelForm
from django.urls import reverse_lazy

def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available =  BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.all().count()
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_visits': num_visits
	}
	return render(request, 'index.html', context)


class BookListView(LoginRequiredMixin, generic.ListView):
	model = Book
	paginate_by = 10

class BookDetailView(generic.DetailView):
	model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
	model = Author
	paginate_by = 10

class AuthorDetailView(generic.DetailView):
	model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10
	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'catalog.can_mark_returned'
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)

	if request.method == 'POST':
		form = RenewBookModelForm(request.POST)

		if form.is_valid():
			book_instance.due_back = form.cleaned_data['due_back']
			book_instance.save()
			return redirect(reverse('all-borrowed'))

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

	context = {
		'form': form,
		'book_instance': book_instance,
	}

	return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	fields = '__all__'
	initial = {'date_of_death': '05/01/2000'}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.can_mark_returned'
	model = Author
	success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
	permission_required = 'catalog.can_mark_returned'
	model = Book
	fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.can_mark_returned'
	model = Book
	fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.can_mark_returned'
	model = Book
	success_url = reverse_lazy('books')

