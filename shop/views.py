from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import CreateView, DeleteView, UpdateView

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

    return render(request, 'shop/list.html', {'current_category': current_category,
                                              'categories': categories,
                                              'cart': cart,
                                              'products': products})


def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})

    return render(request, 'shop/detail.html', {'product': product, 'add_to_cart': add_to_cart})


def product_write(request):
    return render(request, 'shop/write.html')


class ProductUploadView(CreateView):
    model = Product
    #fields = Category.objects.all()
    fields = ['category', 'name', 'slug', 'image', 'description', 'meta_description',
              'price', 'stock', 'available_display', 'available_order']
    template_name = 'shop/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'
    template_name = 'shop/delete.html'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'meta_description',
              'price', 'stock', 'available_display', 'available_order']
    template_name = 'shop/update.html'


