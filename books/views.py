from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from books.forms import BookModelForm, AuthorModelForm
from books.models import *

def index(request):

    num_books = Book.objects.all().count()
    books = Book.objects.order_by('-rate')[:3]

    context = {
        'num_books': num_books,
        'books': books
    }
    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book

    context_object_name = 'book_list'
    template_name = 'book/list.html'
    paginate_by = 2

    def get_queryset(self):
        if 'genre_name' in self.kwargs:
            return Book.objects.filter(genres__name=self.kwargs['genre_name']).all() # Get 5 books containing the title war
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_books'] = len(self.get_queryset())
        if 'genre_name' in self.kwargs:
            context['view_title'] = f"Žánr: {self.kwargs['genre_name']}"
            context['view_head'] = f"Žánr knihy: {self.kwargs['genre_name']}"
        else:
            context['view_title'] = 'Knihy'
            context['view_head'] = 'Přehled knih'
        return context


class BookDetailView(DetailView):
    model = Book

    context_object_name = 'book_detail'
    template_name = 'book/detail.html'


def topten(request):
    return render(request, 'topten.html')


class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'plot', 'poster', 'genres', 'release_date', 'pages', 'rate']


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'books/book_bootstrap_form.html'
    form_class = BookModelForm


class BookDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('book_list')

class AuthorListView(ListView):
    model = Author

    context_object_name = 'author_list'
    template_name = 'author/list.html'
    paginate_by = 2

    def get_queryset(self):
        if 'author_name' in self.kwargs:
            return Author.objects.filter(
                author__name=self.kwargs['author_name']).all()  # Get 5 books containing the title war
        else:
            return Author.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_books'] = len(self.get_queryset())
        if 'author_name' in self.kwargs:
            context['view_title'] = f"Autor: {self.kwargs['author_name']}"
            context['view_head'] = f"Autor knihy: {self.kwargs['author_name']}"
        else:
            context['view_title'] = 'Autoři'
            context['view_head'] = 'Přehled autorů'
        return context


class AuthorDetailView(DetailView):
    model = Author

    context_object_name = 'author_detail'
    template_name = 'author/detail.html'

    #def get_queryset(self):
        #return Book.objects.filter(author=self.kwargs['pk']).order_by('-rate')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['best_books'] = Book.objects.filter(author=self.kwargs['pk']).order_by('-rate')
        return context


class AuthorCreateView(CreateView):
    model = Author
    fields = ['name', 'birth_date', 'description']


class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'authors/author_bootstrap_form.html'
    form_class = AuthorModelForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("author-detail", kwargs={"pk": pk})


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'authors/author_confirm_delete.html'
    success_url = reverse_lazy('author_list')