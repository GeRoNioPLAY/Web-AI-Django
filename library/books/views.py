# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .forms import BookForm
from django.core.paginator import Paginator

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.role == 'admin', login_url=login_url)

def list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/list.html', {'page_obj': page_obj})


@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = BookForm()
    return render(request, 'books/edit_book.html', {'form': form})


@login_required
@admin_required(login_url='list')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})

@login_required
@admin_required(login_url='list')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('list')