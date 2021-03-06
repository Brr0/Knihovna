from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.html import format_html


def attachment_path(instance, filename):
    return "book/" + str(instance.book.id) + "/attachments/" + filename


def poster_path(instance, filename):
    return "book/" + str(instance.id) + "/poster/" + filename


def author_path(instance, filename):
    return "author/" + str(instance.id) + "/photo/" + filename


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Name",
                            help_text='Enter a name of the author')
    birth_date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
                                  verbose_name="Date of birth")
    photo = models.ImageField(upload_to=poster_path, verbose_name="Photo")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def book_count(self, obj):
        return obj.book_set.count()


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Type name",
                            help_text='Enter a book type (e.g. epika, lyrika, drama)')

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Genre name",
                            help_text='Enter a book genre (e.g. sci-fi, comedy)')

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def book_count(self, obj):
        return obj.book_set.count()


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    plot = models.TextField(blank=True, null=True, verbose_name="Plot")
    release_date = models.DateField(blank=True, null=True,
                                    help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
                                    verbose_name="Release date")
    pages = models.IntegerField(blank=True, null=True,
                                  help_text="Please enter an integer value (number of pages)",
                                  verbose_name="Pages")
    rate = models.FloatField(default=5.0,
                             validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
                             null=True,
                             help_text="Please enter an float value (range 1.0 - 10.0)",
                             verbose_name="Rate")
    poster = models.ImageField(upload_to=poster_path, blank=True, null=True, verbose_name="Poster")
    genres = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    types = models.ManyToManyField(Type, help_text='Select a type of this book')

    class Meta:
        ordering = ["-release_date", "title"]

    # Methods
    def __str__(self):
        return f"{self.title}, year: {str(self.release_date.year)}, rate: {str(self.rate)}"

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def release_year(self):
        return self.release_date.year

    def rate_percent(self):
        return format_html("{} %", int(self.rate * 10))


class Attachment(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    last_update = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=attachment_path, null=True, verbose_name="File")

    TYPE_OF_ATTACHMENT = (
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('other', 'Other'),
    )

    type = models.CharField(max_length=5, choices=TYPE_OF_ATTACHMENT, blank=True, default='image',
                            help_text='Select allowed attachment type', verbose_name="Attachment type")
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'book'

    # Methods
    def __str__(self):
        return f"{self.title}, ({self.type})"

    @property
    def filesize(self):
        x = self.file.size
        y = 512000
        if x < y * 1000:
            value = round(x / 1024, 2)
            ext = ' KB'
        elif x < y * 1000 ** 2:
            value = round(x / 1024 ** 2, 2)
            ext = ' MB'
        else:
            value = round(x / 1024 ** 3, 2)
            ext = ' GB'
        return str(value) + ext
