from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django import forms
from .Contract_Deployment import ContractDeployment
from .Wallet_Management import WalletManagement

# Create your views here.
from cart.cart import Cart
from cart.forms import AddProductForm
from .models import *





def product_in_category(request, category_slug=None):
    wallet = 0
    wallet_i = 0
    if request.user.is_authenticated:
        wallet = Wallet.objects.filter(user_id=request.user.username).count()

        wall = Wallet.objects.get(user_id=request.user.username)
        wm = WalletManagement()
        print(wall.wallet_adress)
        if wallet !=0:
            wallet_i = wm.getBalance(wall.wallet_adress)
    cart = Cart(request)
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'shop/list.html', {'cart':cart,
                                              'wallet':wallet,
                                              'current_category': current_category,
                                              'wallet_i':wallet_i,
                                              'categories': categories,
                                              'products': products})


def deploy_contract(request):
    s_id = request.POST["sell"]
    p_id = request.POST["id"]
    update_product = Product.objects.get(user_id=s_id, id=p_id)
    # if Wallet.objects.get(id = "update_product.user_id") == None:
    판매자지갑주소 = Wallet.objects.get(user_id=s_id).wallet_adress
    구매자지갑주소 = Wallet.objects.get(user_id=request.user.username).wallet_adress
    비밀번호 = request.POST["pw"]
    print("판매자지갑주소:",판매자지갑주소)

    print("구매자:", 구매자지갑주소)
    # 계약생성 (구매자 지갑주소, 판매자 지갑주소)
    contract = ContractDeployment(
        구매자지갑주소,
        판매자지갑주소,
        비밀번호,100)

    contract.unlockAccount()
    update_product.contract_adress=contract.deploy()
    update_product.product_state=1
    update_product.buyer = request.user.username

    update_product.save()
    return HttpResponseRedirect('/')

def make_wallet(request):
    wallet = WalletManagement()
    adress = wallet.createAccount(request.POST["pw"])
    new_wallet = Wallet.objects.create(
        user_id=request.POST["id"],
        wallet_adress = adress
    )
    new_wallet.save()
    return HttpResponseRedirect('/')

def buy_contract(request):
    p_id = request.POST["id"]
    s_id = request.POST["sell"]
    update_product = Product.objects.get(user_id=s_id, id = p_id)
    address = update_product.contract_adress
    판매자지갑주소 = Wallet.objects.get(user_id=s_id).wallet_adress
    구매자지갑주소 = Wallet.objects.get(user_id=request.user.username).wallet_adress
    비밀번호 = request.POST["pw"]
    print("판매자지갑주소:", 판매자지갑주소)
    print("구매자:", 구매자지갑주소)
    # 계약생성 (구매자 지갑주소, 판매자 지갑주소)
    contract = ContractDeployment(
        구매자지갑주소,
        판매자지갑주소,
        비밀번호, 100)
    contract.unlockAccount()
    contract.buy(address)
    update_product.product_state=2
    update_product.save()
    return HttpResponseRedirect('/')

def product_detail(request, id, product_slug=None):
    # print(test.unlockAccount())
    # test.deploy()
    del_product = Product.objects.get(id=id)
    if request.method == 'POST' and request.POST["is_del"]=="del":
        del_product.delete()
        return HttpResponseRedirect('/')
    wallet = 0
    wallet_i = 0
    if request.user.is_authenticated:
        wallet = Wallet.objects.filter(user_id=request.user.username).count()

        wall = Wallet.objects.get(user_id=request.user.username)
        wm = WalletManagement()
        print(wall.wallet_adress)
        if wallet !=0:
            wallet_i = wm.getBalance(wall.wallet_adress)
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    return render(request, 'shop/detail.html', {'cart':cart,
                                                'product': product,
                                                'wallet':wallet,
                                                'wallet_i':wallet_i,
                                                'id' : id,
                                                'add_to_cart': add_to_cart})
def product_write(request):
    category = Category.objects.all()
    print(category[1])
    return render(request, 'shop/write.html',{ 'category':category})

def product_update(request,id):
    # update_product= get_object_or_404(Product, id=id)
    update_product = Product.objects.get(id=id)
    wallet = 0
    wallet_i = 0
    if request.user.is_authenticated:
        wallet = Wallet.objects.filter(user_id=request.user.username).count()

        wall = Wallet.objects.get(user_id=request.user.username)
        wm = WalletManagement()
        print(wall.wallet_adress)
        if wallet !=0:
            wallet_i = wm.getBalance(wall.wallet_adress)
        print(wall.wallet_adress)
    # wallet_i = 0
    # if wallet !=0:
    #     wallet_i = WalletManagement.getBalance(str(wall.wallet_adress))
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
        'wallet':wallet,
        'wallet_i':wallet_i,
        'category': category})
        
def write_sub(request):
    if request.method == "POST":
        print(request.POST["user_id"])
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

        
#from Contract_Deployment import ContractDeployment
#test = ContractDeployment("0xCfd8cbE5Da3002B52c650cE1302E10c6d1BE644E","0x5B44b4E4052672b19CADEfC892b09488aEbBDDa6","pass0",100)
#test.unlockAccount()
#test.deploy()
#test.buy("컨트랙트 주소")
