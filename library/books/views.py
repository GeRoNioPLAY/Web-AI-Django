# from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .models import Book, Order, OrderItem
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


def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart_json = request.COOKIES.get('cart', '{}')

    try:
        cart = json.loads(cart_json)
    except json.JSONDecodeError:
        cart = {}

    book_id = str(book.pk)
    if book_id in cart:
        cart[book_id] = int(cart[book_id]) + 1
    else:
        cart[book_id] = 1
    
    response = HttpResponseRedirect(reverse('list'))
    response.set_cookie('cart', json.dumps(cart), max_age=60*60*24*14)
    return response


def cart(request):
    cart_json = request.COOKIES.get('cart', '{}')
    
    print(f"cart_json: {cart_json}, type: {type(cart_json)}")
    try:
        cart = json.loads(cart_json)
    except json.JSONDecodeError:
        cart = {}

    books = Book.objects.filter(pk__in=cart.keys())
    cart_items = []
    total_price = 0
    for book in books:
        quantity = int(cart[str(book.pk)])
        item_total = book.price * quantity
        total_price += item_total
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'total': item_total,
        })
    return render(request, 'books/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def create_order(request):
    cart_json = request.COOKIES.get('cart', '{}')
    try:
        cart = json.loads(cart_json)
    except json.JSONDecodeError:
        cart = {}

    if not cart:
        return redirect('cart')
    
    books = Book.objects.filter(pk__in=cart.keys())
    total_price = sum(book.price * int(cart[str(book.pk)]) for book in books)

    order = Order.objects.create(user=request.user, total_price=total_price)

    for book in books:
        quantity = int(cart[str(book.pk)])
        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=quantity,
            price=book.price * quantity
        )

    response = HttpResponseRedirect(reverse('orders'))
    response.delete_cookie('cart')
    return response

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'books/orders.html', {'orders': orders})

def clear_cart(request):
    if request.method == 'POST':
        response = HttpResponseRedirect(reverse('cart'))
        response.delete_cookie('cart')
        return response
    return HttpResponseRedirect(reverse('cart'))