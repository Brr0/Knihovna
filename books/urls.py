from django.urls import path

from books import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/genres/<str:genre_name>/', views.BookListView.as_view(), name='book_genre'),
    path('topten', views.topten, name='topten'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
