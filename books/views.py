from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from books.forms import BookModelForm
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
    fields = ['title', 'plot', 'poster', 'genres', 'release_date', 'runtime', 'rate']


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'books/book_bootstrap_form.html'
    form_class = BookModelForm


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('booj_list')