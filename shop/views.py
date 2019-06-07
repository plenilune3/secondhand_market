from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

# Create your views here.
from cart.cart import Cart
from cart.forms import AddProductForm
from .models import *


def product_in_category(request, category_slug=None):
    cart = Cart(request)
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'shop/list.html', {'cart':cart,
                                              'current_category': current_category,
                                              'categories': categories,
                                              'products': products})


def product_detail(request, id, product_slug=None):
    del_product = Product.objects.get(id=id)
    if request.method == 'POST' and request.POST["is_del"]=="del":
        del_product.delete()
        return HttpResponseRedirect('/')
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})

    return render(request, 'shop/detail.html', {'cart':cart,
                                                'product': product,
                                                'id' : id,
                                                'add_to_cart': add_to_cart})
def product_write(request):
    return render(request, 'shop/write.html')
def write_sub(request):
    if request.method == "POST":
        print(str(request.POST["name"]).replace(' ','-'))
        new_product = Product.objects.create(
            category=Category.objects.all()[1],
            name=request.POST["name"],
            slug=str(request.POST["name"]).replace(' ','-'),
            image=request.FILES.get("image"),
            description=request.POST["description"],
            meta_description=request.POST["meta_description"],
            price=request.POST["price"],
            stock=request.POST["stock"]
        )
        new_product.save()

        return HttpResponseRedirect('/')