from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from store.models import CartItem
from store.models import Product
from .models import Order, OrderProduct
from .forms import OrderForm
from .models import Payment

# for coupon
from store.models import Coupon, UsedCoupon
from store.forms import CouponForm, UsedCouponForm
import datetime
import json


def payments(request):
    body = json.loads(request.body)
    print(
        body
    )  # {'orderID': '0022092621', 'transID': '6JT072363T708401U', 'payment_method': 'PayPal', 'status':
    # 'COMPLETED'}
    # now store these details inside the payment model`
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=order.order_total,
        status=body["status"],
    )
    print(payment)
    payment.save()
    order.payment = payment  # we need to update the order model also.
    order.is_ordered = True
    order.save()  # now the order is successful
    # move the cart items to order Product table,
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = (
            OrderProduct()
        )  # we have created an object of this model and assign these values to it.
        order_product.order_id = (
            order.id
        )  # order is a foreign object of OrderProduct model.
        order_product.payment = (
            payment  # which is the object that we just created above
        )
        order_product.user_id = request.user.id
        order_product.product_id = (
            item.product_id
        )  # this field must be created by the database.
        order_product.quantity = item.quantity
        order_product.product_price = (
            item.product.price
        )  # product is a foreign key of CartItem model
        order_product.ordered = True  # by this time product must have been ordered
        order_product.save()
        # making the changes to product variations
        # we cannot directly assign values to many to many fields
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(
            id=order_product.id
        )  # the above save have alredy generatedt id for OrderProduct
        order_product.variations.set(product_variation)
        order_product.save()
        # reduce the quantity of the stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # clear the cart
    CartItem.objects.filter(user=request.user).delete()
    # sent order received message to customer
    # this part is for later
    # sent order number and  translation id -> sentData() via JsonResponse
    data = {
        "order_number": order.order_number,
        "transID": payment.payment_id,
    }
    return JsonResponse(
        data
    )  # this data wil go to the place where it came from { in html sentData()


def orders(request):
    return render(request, "order_complete.html")


# Create your views here
# first need to check if the user have an item in caret, if not redirect them back to store page.


def place_order(request, total=0, quantity=0):
    discount = 0
    if "coupon_code" in request.session:
        print(request.session["coupon_code"])
        coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
        discount = coupon.amount
    print("we are inside the place order section \n\n\n")
    instance_user = request.user
    #  if the cart count  is less-than or equal to zero, he doesn't have any cart item.
    cart_items = CartItem.objects.filter(user=instance_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")
    # actual code 1, store the post request inside the order model and generate the order number.
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (18 * total) / 100
    total_price = total + tax
    grand_total = (total + tax) - discount
    if request.method == "POST":
        print("request.post", request.POST)
        print("a post method received \n\n\n")
        form = OrderForm(request.POST)
        print(form)
        print("now form is validating \n\n")
        if form.is_valid():
            print("the form is valid \n\n")
            # store the date to -> Order model
            data = Order()  # creating an instance of the model
            data.user = instance_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.email = form.cleaned_data["email"]
            data.phone = form.cleaned_data["phone"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line2 = form.cleaned_data["address_line_2"]
            data.landmark = form.cleaned_data["landmark"]
            data.city = form.cleaned_data["city"]
            data.pincode = form.cleaned_data["pincode"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.order_note = form.cleaned_data["order_note"]
            # calculated datas
            data.discount = discount
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")  # this will give you the user ip.
            data.save()  # it will create a primary key which can be used to create order id
            print("basic details saved \n\n\n")
            # generate order number
            yr = int(datetime.date.today().strftime("%y"))  # year
            dt = int(datetime.date.today().strftime("%d"))  # date
            mt = int(datetime.date.today().strftime("%m"))  # month
            d = datetime.date(yr, mt, dt)  # stored here
            current_date = d.strftime(
                "%Y%m%d"
            )  # -> 20220923  now concatenate it with order number
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=instance_user, is_ordered=False, order_number=order_number
            )
            context = {
                "order": order,
                "discount": discount,
                "cart_items": cart_items,
                "total_price": total_price,
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
            }
            request.session["order_id"] = order.order_number
            print("order number : ", order.order_number)
            return render(request, "payments.html", context)
        else:
            print("form is failed to validate \n\n\n")
            return redirect("checkout")

    return HttpResponse("place order page under development")


def order_complete(request):
    mode_of_payment = None  # for cod payment
    print("inside the order completed function")
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")
    if "trans_id" in request.session:
        transID = request.session["trans_id"]
        print("cod", transID)
    print("transID", transID)
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        print("transID before context ", transID)
        if "tans_id" in request.session:
            del request.session["trans_id"]
            mode_of_payment = "COD"
        else:
            payment = Payment.objects.get(payment_id=transID)
        print("payment object obtained", payment)
        print("mode of payment", mode_of_payment)
        context = {
            "order": order,
            "mode_of_payment": mode_of_payment,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "transID": payment.payment_id,
            "payment": payment,
            "sub_total": sub_total,
            "discount": order.discount,
        }
        return render(request, "order_complete.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        print(
            "\n\n entered inside the except block and skipped the payment rendering page"
        )
        return redirect("dashboard")


# needed further editing on the cod payment.
def cod_payment(request):
    instance_user = request.user
    print(request.session["order_id"])
    order_number = request.session["order_id"]
    print("order_number", order_number)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=order_number
    )
    print(order, "ordered list \n")
    payment = Payment(
        user=request.user,
        payment_method="cash on delivery",
        amount_paid=order.order_total,
        status="Pending",
    )
    payment.save()
    order.is_ordered = True
    # updating the order foreign key filed
    order.payment = payment
    order.satus = "Pending"
    order.save()
    cart_items = CartItem.objects.filter(user=request.user)
    for items in cart_items:
        order_product = OrderProduct()
        # print(order_id, "\n\n\n")
        order_product.order_id = order.id  # same for all the products
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = items.product.id
        order_product.quantity = items.quantity
        order_product.product_price = (
            items.product.price
        )  # product price is fetched from the foreign key of OrderProduct Model.
        order_product.ordered = True
        # order_product.created_at = request.
        order_product.save()  # saving the products one by one.
        cart_item = CartItem.objects.get(id=items.id)
        product_variation = cart_item.variations.all()  # getting all variations
        order_product = OrderProduct.objects.get(
            id=order_product.id
        )  # filtering the product based on
        order_product.variations.set(product_variation)
        order_product.save()
        #  reduce the quantity of the ordered product for the stock
        product = Product.objects.get(id=items.product_id)
        product.stock -= items.quantity
        product.save()
    #  after ordering clearing the cart items.
    CartItem.objects.filter(user=request.user).delete()
    # order = Order.objects.get(order_number=order_number, is_ordered=True) order_product =
    # OrderProduct.objects.filter(order_id=order.id) for cod translations   ---- ---  this code is not working so i
    # kind of used some adjustments to overcome this problem.
    param = "order_number=" + order.order_number + "&payment_id=" + payment.payment_id
    ################
    # capture the payee
    messages.success(request, "Payment Success")
    if "order_number" in request.session:
        print("\n\n order number in cod ", request.session["order_number"])
        del request.session["order_id"]
        print("order_id is deleted")
    # for COD am manually passing the order number through the session.
    request.session["trans_id"] = order_number
    redirect_url = reverse("order_complete")
    return redirect(f"{redirect_url}?{param}")
