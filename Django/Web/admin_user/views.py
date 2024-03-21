import hashlib
from django.shortcuts import render
from users.models import User, Product, ProductKind, Discount, Cart, Order, OrderDetail
from django.shortcuts import  redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime


def authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' in request.session:
            # Kiểm tra xem người dùng có phải là admin hay không
            if request.session.get('role') == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                request.session.pop('username', None)
                request.session.pop('role', None)
                return HttpResponseRedirect('/login')  # Chuyển hướng người dùng không phải là admin đến trang người dùng
        else:
            return HttpResponseRedirect('/login')  # Chuyển hướng đến trang đăng nhập
    return wrapper

@authentication_required
def index(request):
    session_usernames = request.session.get('username')
    users = User.objects.exclude(username=session_usernames)
    context={
        'users': users
    }
    return render(request, 'index.html', context)
@authentication_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'create.html', {'error': 'Username already exists'})
        else:
            if password != repassword:
                return render(request, 'create.html', {'error': 'Password and repassword are not the same'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'create.html', {'error': 'Email already exists'})
            else:
                user = User(username=username, email=email, password=password, phone=phone, role=role)
                user.save()
                content = {
                    'users': User.objects.all()
                }
        return redirect('/admin', content)
    return render(request, 'create.html')

@authentication_required
def update_user(request, id):
    User.objects.get(id=id)
    print(User.objects.get(id=id))
    content = {
        'user': User.objects.get(id=id)
    }
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        
        user=User.objects.get(id=id)
        user.username = username
        user.email = email
        user.phone = phone
        user.role = role
        user.save()
        if User.objects.filter(username=username).exists():
            contentupdate = {
                'user': User.objects.get(id=id),
                'error': 'Username already exists'
            }
            return render(request, 'update.html', contentupdate)
        elif User.objects.filter(email=email).exists():
            contentupdate = {
                'user': User.objects.get(id=id),
                'error': 'Email already exists'
            }
            return render(request, 'update.html', contentupdate)
        
        contentupdate = {
            'user': User.objects.get(id=id),
            'success': 'Update user successfully'
        }
        return render(request, 'update.html', contentupdate)
    return render(request, 'update.html', content)

@authentication_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    content = {
        'users': User.objects.all()
    }
    return redirect('/admin', content)


@authentication_required
def product(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'product.html', context)

@authentication_required
def create_product(request):
    context = {
            'products': Product.objects.all(),
            'kinds': ProductKind.objects.all()
        }
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        kind = request.POST.get('kind')
        
        img_name=request.FILES.get('image').name
        #mã hóa tên ảnh
        image = hashlib.md5(img_name.encode()).hexdigest()
        #lưu ảnh dưới đuôi .png
        image = image + '.png'
        with open('mystaticfiles/dist/img/products/'+image, 'wb+') as destination:
            for chunk in request.FILES.get('image').chunks():
                destination.write(chunk)
        
        image_name = image
        product = Product(name=name, price=price,quantity=quantity, description=description, image_name=image_name, kind_id=kind)
        product.save()
        
        context = {
            'products': Product.objects.all(),
            'kinds': ProductKind.objects.all()
        }
        return redirect('/admin/product', context)
    
    return render(request, 'create_product.html',context)

@authentication_required
def update_product(request, id):
    Product.objects.get(id=id)
    content = {
        'product': Product.objects.get(id=id),
        'kinds': ProductKind.objects.all()
    }
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        kind = request.POST.get('kind')
        
        if request.FILES.get('image') == None:
            product = Product.objects.get(id=id)
            product.name = name
            product.price = price
            product.quantity = quantity
            product.description = description
            product.kind_id = kind
            product.save()
            context = {
                'product': Product.objects.get(id=id),
                'success': 'Update product successfully'
            }
            return redirect('/admin/product', context)
        
        img=request.FILES.get('image')
        print(img)
        img_name=img.name
        
        product = Product.objects.get(id=id)
        product.name = name
        product.price = price
        product.quantity = quantity
        product.description = description
        
        #mã hóa tên ảnh
        image = hashlib.md5(img_name.encode()).hexdigest()
        #lưu ảnh dưới đuôi .png
        image = image + '.png'
        print(image)
        with open('mystaticfiles/dist/img/products/'+image, 'wb+') as destination:
            for chunk in request.FILES.get('image').chunks():
                destination.write(chunk)
        
        product.image_name = image
        
        
        product.save()
        
        context = {
            'product': Product.objects.get(id=id),
            'success': 'Update product successfully'
        }
        return redirect('/admin/product', context)

    return render(request, 'edit_product.html', content)

@authentication_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    context = {
        'products': Product.objects.all()
    }
    return redirect('/admin/product', context)

def kind(request):
    context = {
        'kinds': ProductKind.objects.all()
    }
    
    return render(request, 'kind.html', context)

@authentication_required
def add_kind(request):
    if request.method == "POST":
        name = request.POST.get('name')
        kind = ProductKind(name=name)
        kind.save()
        context = {
            'kinds': ProductKind.objects.all()
        }
        return redirect('/admin/kind', context)
    context = {
            'kinds': ProductKind.objects.all()
        }
    return render(request, 'kind.html',context)

@authentication_required
def edit_kind(request, id):
    ProductKind.objects.get(id=id)
    content = {
        'kind': ProductKind.objects.get(id=id)
    }
    if request.method == "POST":
        name = request.POST.get('name')
        kind = ProductKind.objects.get(id=id)
        kind.name = name
        kind.save()
        context = {
            'kind': ProductKind.objects.get(id=id),
            'success': 'Update kind successfully'
        }
        return redirect('/admin/kind', context)
    return render(request, 'edit_kind.html', content)

@authentication_required
def delete_kind(request, id):
    kind = ProductKind.objects.get(id=id)
    kind.delete()
    context = {
        'kinds': ProductKind.objects.all()
    }
    return redirect('/admin/kind', context)

@authentication_required
def discount_index(request):
    
    context = {
        'discounts': Discount.objects.all()
    }
    
    return render(request, 'discount.html', context)

@authentication_required
def create_discount(request):
    if request.method == "POST":
        code = request.POST.get('code')
        name = request.POST.get('name')
        condition = request.POST.get('condition')
        kind = request.POST.get('kind')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Chuyển đổi định dạng ngày và giờ từ biểu mẫu thành đối tượng DateTime
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        money = request.POST.get('money')
        quantity = request.POST.get('quantity')
        
        discount = Discount(code=code, name=name, condition=condition, kind_id=kind, start_date=start_date, end_date=end_date, money=money, quantity=quantity)
        discount.save()
        context = {
            'discounts': Discount.objects.all()
        }
        return redirect('/admin/discount', context)
    context = {
            'discounts': Discount.objects.all(),
            'kinds': ProductKind.objects.all()
        }
    return render(request, 'create_discount.html',context)

@authentication_required
def update_discount(request, id):
    content = {
        'discount': Discount.objects.get(id=id),
        'kinds': ProductKind.objects.all()
    }
    if request.method == "POST":
        code = request.POST.get('code')
        name = request.POST.get('name')
        condition = request.POST.get('condition')
        kind = request.POST.get('kind')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        money = request.POST.get('money')
        quantity = request.POST.get('quantity')
        
        # Kiểm tra nếu ngày none thì lấy ngày cũ
        if start_date == '':
            start_date = Discount.objects.get(id=id).start_date
        if end_date == '':
            end_date = Discount.objects.get(id=id).end_date
        
        # Chuyển đổi định dạng ngày và giờ từ biểu mẫu thành đối tượng DateTime
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        
        discount = Discount.objects.get(id=id)
        discount.code = code
        discount.name = name
        discount.condition = condition
        discount.kind_id = kind
        discount.start_date = start_date
        discount.end_date = end_date
        discount.money = money
        discount.quantity = quantity
        discount.save()
        context = {
            'discount': Discount.objects.get(id=id),
            'success': 'Update discount successfully'
        }
        return redirect('/admin/discount', context)
    return render(request, 'edit_discount.html', content)

@authentication_required
def delete_discount(request, id):
    discount = Discount.objects.get(id=id)
    discount.delete()
    context = {
        'discounts': Discount.objects.all()
    }
    return redirect('/admin/discount', context)

@authentication_required
def statistics(request):
    context = {
        'orders': Order.objects.all(),
        'orderdetails': OrderDetail.objects.all()
    }
    return render(request, 'statistics.html', context)

