# from django.shortcuts import render

# Create your views here.

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

@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart = request.session.get('cart', {})

    book_id = str(book.pk)
    if book_id in cart:
        cart[book_id] += 1
    else:
        cart[book_id] = 1
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('list')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    books = Book.objects.filter(pk__in=cart.keys())
    cart_items = []
    total_price = 0
    for book in books:
        quantity = cart[str(book.pk)]
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
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    books = Book.objects.filter(pk__in=cart.keys())
    total_price = sum(book.price * cart[str(book.pk)] for book in books)

    order = Order.objects.create(user=request.user, total_price=total_price)

    for book in books:
        quantity = cart[str(book.pk)]
        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=quantity,
            price=book.price * quantity
        )

    request.session['cart'] = {}
    request.session.modified = True
    return redirect('orders')

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'books/orders.html', {'orders': orders})