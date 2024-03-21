from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from .models import User, Product, Cart, Order, OrderDetail, Discount,Discount_User, ProductKind
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from .vnpay import vnpay



# Hiển thị trang chính
def index(request,id = None):
    template = loader.get_template('main.html')
    context = {
                'users': User.objects.all(),
                'products': Product.objects.all(),
                'kinds': ProductKind.objects.all()
                }
    if id:
        context['products'] = Product.objects.filter(kind=id)
    return HttpResponse(template.render(context, request))

# Hiển thị trang đăng ký
def createUserGet(request):
    template = loader.get_template('register.html')
    context = {'users': User.objects.all()}
    return HttpResponse(template.render(context, request))

def send_email(email, otp):
    # Thiết lập thông tin email của bạn
    sender_email = "kioyshi2003@gmail.com"
    sender_password = "nnns rczm zifc egbl"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Tạo đối tượng MIMEMultipart
    msg = MIMEMultipart()

    # Định dạng nội dung email
    message = f"""
    Xin chào,
    
    Mã OTP của bạn là: {otp}
    
    Trân trọng,
    Đội ngũ quản trị viên
    """

    # Thêm thông tin vào đối tượng MIMEMultipart
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Xác nhận OTP"

    # Thêm nội dung vào email
    msg.attach(MIMEText(message, 'plain'))

    # Gửi email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
    
def createUserPost(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = 'user'
        
        # Lưu thông tin người dùng vào session
        request.session['userName'] = username
        request.session['password'] = password
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['role'] = role
    

        # Kiểm tra xem mật khẩu đã nhập lại chính xác hay không
        if password != confirm_password:
            return HttpResponse('Mật khẩu không khớp!')

        # Kiểm tra xem người dùng đã tồn tại hay chưa
        if User.objects.filter(username=username).exists():
            return HttpResponse('Người dùng đã tồn tại!')

        if User.objects.filter(email=email).exists():
            return HttpResponse('Email đã tồn tại!')
        
        # Tạo OTP ngẫu nhiên
        otp = ''.join(random.choices('0123456789', k=6))

        # Gửi email chứa OTP
        send_email(email, otp)

        # Lưu OTP và thời gian hết hạn vào session
        request.session['otp'] = otp
        request.session['otp_expires'] = str(timezone.now() + timedelta(seconds=120))
        

        # Hiển thị form xác nhận OTP
        return render(request, 'otp_confirmation.html')
    else:
        return HttpResponse('Phương thức không hợp lệ!')

def confirmOTP(request):
    if request.method == 'POST':
        # Lấy mã OTP mà người dùng nhập vào từ form
        user_otp = request.POST.get('otp')

        # Lấy mã OTP và thời gian hết hạn từ session
        session_otp = request.session.get('otp')
        otp_expires = request.session.get('otp_expires')

        # Chuyển đổi chuỗi thời gian hết hạn thành đối tượng datetime
        otp_expires = datetime.strptime(otp_expires, '%Y-%m-%d %H:%M:%S.%f%z')

        # Kiểm tra xem mã OTP có khớp không và thời gian hết hạn
        if user_otp == session_otp and timezone.now() < otp_expires:
            # Mã OTP đúng và còn hiệu lực, có thể tạo người dùng mới ở đây
            # Code tạo người dùng mới ...
            session_user = User(username=request.session.get('userName'), password=request.session.get('password'), email=request.session.get('email'), phone=request.session.get('phone'), role=request.session.get('role'))
            # Xóa thông tin về OTP sau khi đã sử dụng
            del request.session['otp']
            del request.session['otp_expires']
            session_user.save()
            return HttpResponse('Xác nhận mã OTP thành công và tạo người dùng mới!')
        else:
            return HttpResponse('Mã OTP không hợp lệ hoặc đã hết hạn!')

    else:
        return HttpResponse('Phương thức không hợp lệ!')

# Hiển thị trang đăng nhập
def loginGet(request):
    template = loader.get_template('login.html')
    context = {'users': User.objects.all()}
    return HttpResponse(template.render(context, request))

# Xử lý đăng nhập
def loginPost(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Kiểm tra xem người dùng có tồn tại và mật khẩu đúng không
        if User.objects.filter(username=username, password=password).exists():
            request.session['username'] = username
            
            # Nếu là admin, đặt session 'role' là 'admin'
            if User.objects.filter(username=username, role='admin').exists():
                request.session['role'] = 'admin'
            return redirect('/')
        else:
            return HttpResponse('Tên người dùng hoặc mật khẩu không đúng!')
    else:
        return HttpResponse('Phương thức không hợp lệ!')

# Định nghĩa decorator kiểm tra xác thực người dùng và quyền truy cập
def authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' in request.session:
            # Kiểm tra xem người dùng có phải là admin hay không
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')  # Chuyển hướng đến trang đăng nhập
    return wrapper

# Đăng xuất và xóa session
def logout(request):
    request.session.pop('username', None)
    request.session.pop('role', None)
    return redirect('/')

# Hiển thị trang thông tin người dùng
@authentication_required
def user(request):
    template = loader.get_template('user.html')
    session = request.session
    context = {
        'username': session.get('username'),
        'role': session.get('role'),
        "user": User.objects.get(username=session.get('username'))
    }
    return HttpResponse(template.render(context, request))

# Cập nhật thông tin người dùng
@authentication_required
def update_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Lấy thông tin người dùng hiện tại từ session
        user = User.objects.get(username=request.session.get('username'))
        user.username = username
        user.password = password
        user.email = email
        user.phone = phone
        user.save()
        return redirect('/')
    else:
        return redirect('/')
    
def add_to_cart (request, id):
    if 'username' in request.session:
        product = Product.objects.get(id=id)
        user = User.objects.get(username=request.session.get('username'))
        cart = Cart.objects.filter(user=user, product=product)
        if cart.exists():
            cart = cart[0]
            cart.quantity += 1
            cart.save()
        else:
            cart = Cart(user=user, product=product, quantity=1)
            cart.save()
        return redirect('/')
    else:
        return HttpResponseRedirect('/login')
    
@authentication_required
def cart(request):
    if 'username' in request.session:
        user = User.objects.get(username=request.session.get('username'))
        carts = Cart.objects.filter(user=user)
        total = 0
        for cart in carts:
            total += cart.product.price * cart.quantity
        context = {
            'carts': carts,
            'total': total
        }
        return render(request, 'cart.html', context)
    else:
        return HttpResponseRedirect('/login')
    
@authentication_required
def remove_cart(request, id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect('/cart')

@authentication_required
def add_cart(request, id):
    cart = Cart.objects.get(id=id)
    cart.quantity += 1
    cart.save()
    return redirect('/cart')

@authentication_required
def except_cart(request, id):
    cart = Cart.objects.get(id=id)
    cart.quantity -= 1
    if cart.quantity == 0:
        cart.delete()
    else:
        cart.save()
    return redirect('/cart')

@authentication_required

def checkout(request):
    total_price = request.POST.get('total_price')
    selected_products_string = request.POST.get('selected_products')
    
    # Tạo session lưu thông tin sản phẩm và số lượng
    request.session['total_price'] = total_price
    
    if request.method == 'POST':
        # Chuyển total_price thành int
        total_price = int(total_price)
        
        # Phân tích chuỗi selected_products để lấy id sản phẩm và số lượng
        selected_products_list = selected_products_string.split(',')
        products_quantity = {}
        for product_info in selected_products_list:
            product_id, quantity = product_info.split(':')
            products_quantity[int(product_id)] = int(quantity)
            
            request.session['products_quantity'] = products_quantity
            
        # Lưu thông tin sản phẩm và số lượng vào session
        # Lấy thông tin người dùng từ session
        # Tiếp tục xử lý và xây dựng URL thanh toán
        
        # Xử lý thanh toán với VNPay
        vnp = vnpay()
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_Command'] = 'pay'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_Amount'] =  total_price * 100
        vnp.requestData['vnp_CurrCode'] = 'VND'
        vnp.requestData['vnp_TxnRef'] = 'MC' + datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.requestData['vnp_OrderInfo'] = 'Thanh toan don hang'
        vnp.requestData['vnp_OrderType'] = 'billpayment'
        vnp.requestData['vnp_Locale'] = 'vn'
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.requestData['vnp_IpAddr'] = "13.160.92.202"
        vnp.requestData['vnp_ReturnUrl'] = "http://127.0.0.1:8000/vnpay-return"
        
        vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
        
        # Redirect to VNPAY
        return redirect(vnpay_payment_url)
    
    else:
        return render(request, 'checkout.html', {'title': 'Thanh toán'})

		
def vnpay_return(request):
    products_quantity = request.session.get('products_quantity', {})
    total_price = request.session.get('total_price')
    products = Product.objects.filter(id__in=products_quantity.keys())
    
    if request.method == 'GET':
        # Kiểm tra các tham số phản hồi từ VNPay để xác định xem thanh toán có thành công hay không
        vnp_ResponseCode = request.GET.get('vnp_ResponseCode')
        if vnp_ResponseCode == '00':
            # Thanh toán thành công
            Order.objects.create(user=User.objects.get(username=request.session.get('username')), total=total_price, date=timezone.now())
            number_of_iterations = len(products)
            for product in products:
                quantity = products_quantity.get(product.id)  # Lấy số lượng tương ứng với sản phẩm
                products_quantity_list = list(products_quantity.items())
                for i in range(number_of_iterations):
                    
                    if int(list(products_quantity_list)[i][0]) == int(product.id):
                        print("ok")
                        OrderDetail.objects.create(order=Order.objects.last(), product=product, quantity=products_quantity_list[i][1])
                        
                        Product.objects.filter(id=product.id).update(quantity=product.quantity - products_quantity_list[i][1])
                        
                        Cart.objects.filter(user=User.objects.get(username=request.session.get('username')), product=product).delete()
            return redirect('/')
        else:
            # Thanh toán không thành công
            return redirect('/')
    else:
        # Phản hồi không hợp lệ
        return HttpResponse(status=400)


@authentication_required
def discount(request):
    discount = Discount.objects.all()
    discount_save = Discount_User.objects.filter(user=User.objects.get(username=request.session.get('username')))
    context = {
        'discounts': discount,
        'discount_save': discount_save,
        'discount_save_id' : [d.discount.id for d in discount_save]
    }
    print([d.discount.id for d in discount_save])
    return render(request, 'DiscountUser.html', context)

@authentication_required
def save_discount(request, id):
    discount = Discount.objects.get(id=id)
    user = User.objects.get(username=request.session.get('username'))
    discount_user = Discount_User(user=user, discount=discount)
    discount_user.save()
    return redirect('/discount')

def remove_save_discount(request, id):
    discount_user = Discount_User.objects.get(id=id)
    discount_user.delete()
    return redirect('/discount')
