from books.models import Genre

def genres(request):
    return {'genres': Genre.objects.all()}