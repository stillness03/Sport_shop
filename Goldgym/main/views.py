from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
from cart.forms import CartAddProductForm
from django.shortcuts import render

def popular_list(request):
    products = Product.objects.filter(available=True)[:3]
    return render(request,
                  'main/index/index.html',
                  {
                      'products': products,
                      'is_index_page': True
                   })


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm
    return render(request,
                  'main/product/detail.html',
                  {
                      'product': product,
                      'cart_product_form': cart_product_form,
                      'is_index_page': False
                   })


def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        paginator = Paginator(products.filter(category=category), 10)
        current_page = paginator.page(int(page))
    return render(request,
                  'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': current_page,
                   'slug_url': category_slug,
                   'is_index_page': False
                   })


def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)


def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)