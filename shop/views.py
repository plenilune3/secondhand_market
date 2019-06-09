from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django import forms
from .Contract_Deployment import ContractDeployment

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
def deploy_contract(request,id):
    update_product = Product.objects.get(id=id)
    update_product.product_state=1
    update_product.save()
    #이거 뭐하는건지 물어봐야댐
    test = ContractDeployment(
        "0xCfd8cbE5Da3002B52c650cE1302E10c6d1BE644E",
        "0x5B44b4E4052672b19CADEfC892b09488aEbBDDa6",
        "pass0",100)
    test.deploy()

def buy_contract(request,id):
    update_product = Product.objects.get(id=id)
    update_product.product_state=2
    update_product.save()
    #매번하는수밖에없는지?
    test = ContractDeployment(
        "0xCfd8cbE5Da3002B52c650cE1302E10c6d1BE644E",
        "0x5B44b4E4052672b19CADEfC892b09488aEbBDDa6",
        "pass0",100)
    test.buy()

def product_detail(request, id, product_slug=None):
    test = ContractDeployment(
        "0xCfd8cbE5Da3002B52c650cE1302E10c6d1BE644E",
        "0x5B44b4E4052672b19CADEfC892b09488aEbBDDa6",
        "pass0",100)
    # print(test.unlockAccount())
    # test.deploy()
    del_product = Product.objects.get(id=id)
    if request.method == 'POST' and request.POST["is_del"]=="del":
        del_product.delete()
        return HttpResponseRedirect('/')
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    id = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'cart':cart,
                                                'product': product,
                                                'id' : id,
                                                'user_id':id.user_id,
                                                'add_to_cart': add_to_cart})
def product_write(request):
    category = Category.objects.all()
    print(category[1])
    return render(request, 'shop/write.html',{ 'category':category})

def product_update(request,id):
    # update_product= get_object_or_404(Product, id=id)
    update_product = Product.objects.get(id=id)
    category = Category.objects.all()
    if request.method == "POST":
        # update_product.category=Category.objects.all()[]
        update_product.name = request.POST['name']
        update_product.slug = request.POST['name']
        update_product.image = request.FILES.get('image')
        update_product.description = request.POST['description']
        update_product.price = request.POST['price']
        update_product.stock = request.POST['stock']
        update_product.save()
        return HttpResponseRedirect('/')
    return render(request, 'shop/update.html' ,{ 
        'update_product': update_product,
        'category': category})
        
def write_sub(request):
    if request.method == "POST":
        # print(str(request.POST["name"]).replace(' ','-'))
        new_product = Product.objects.create(
            category=Category.objects.get(name=request.POST["category"]),
            name=request.POST["name"],
            slug=str(request.POST["name"]).replace(' ','-'),
            image=request.FILES.get("image"),
            description=request.POST["description"],
            user_id=request.POST["user_id"],
            meta_description=request.POST["meta_description"],
            price=request.POST["price"],
            stock=request.POST["stock"]
        )
        new_product.save()

        return HttpResponseRedirect('/')