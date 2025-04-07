import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from zoo_store.models import CheckoutInfo, Profile
from django.utils import timezone


def index(request):
    return render(request, "index.html")


def fish_page(request):
    return render(request, "fish.html")


def dog_page(request):
    return render(request, "dogs.html")


def cat_page(request):
    return render(request, "cats.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"""
        New message from contact form:

        Name: {name}
        Email: {email}
        Phone: {phone}

        Subject: {subject}

        Message:
        {message}
        """

        email_message = EmailMessage(
            subject=f"Contact Form: {subject}",
            body=full_message,
            from_email="petpalsservice1@gmail.com",
            to=["petpalsservice1@gmail.com"],
            reply_to=[email],
        )

        email_message.send(fail_silently=False)

        messages.success(request, "Message sent successfully!")
        return render(request, "index.html")

    return render(request, "contact.html")


def bird_page(request):
    return render(request, "birds.html")


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import CheckoutInfo
from django.utils import timezone


def cart_page(request):
    cart = request.session.get("cart", {})
    return render(request, "cart.html", {"cart": cart})


def checkout(request):
    print("🐾 SESSION CART DURING CHECKOUT:", request.session.get("cart"))

    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    for item in cart.values():
        item_total = item["price"] * item["quantity"]
        total_price += item_total
        cart_items.append({
            "name": item["name"],
            "image": item["image"],
            "price": item["price"],
            "quantity": item["quantity"],
            "total": item_total
        })

    if request.method == "POST":
        data = request.POST

        CheckoutInfo.objects.create(
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            email=data.get("email"),
            phone_num=data.get("phone"),
            street_address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            zip_code=data.get("zip"),
            country=data.get("country"),
            name_on_card=data.get("cardName"),
            payment_token=data.get("cardNumber"),
            expiration_date=data.get("expDate"),
            cvv=data.get("cvv"),
            created_at=timezone.now()
        )

        item_lines = "\n".join(
            f"- {item['name']} x{item['quantity']} = ${item['total']:.2f}" for item in cart_items
        ) if cart_items else "No items found in your cart."

        message_body = f"""Hi {data.get('firstName')},

    Thank you for your order! 🐾

    Here’s what you purchased:

    {item_lines}

    Total: ${total_price:.2f}

    We'll begin processing your order shortly.

    – PetPals Team"""

        send_mail(
            subject="Your Order Confirmation 🐾",
            message=message_body,
            from_email=None,
            recipient_list=[data.get("email")],
            fail_silently=False,
        )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("index")

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })


@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)

        product_id = data.get("product_id")
        name = data.get("name")
        price = float(data.get("price"))
        image = data.get("image")

        if not product_id:
            return JsonResponse({"error": "Missing product ID"}, status=400)

        if "cart" not in request.session:
            request.session["cart"] = {}

        cart = request.session["cart"]

        if product_id in cart:
            cart[product_id]["quantity"] += 1
        else:
            cart[product_id] = {
                "name": name,
                "price": price,
                "image": image,
                "quantity": 1
            }

        request.session.modified = True

        return JsonResponse({"message": "Added to cart", "cart": cart})

    return JsonResponse({"error": "POST required"}, status=405)


@csrf_protect
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        print("✅ Subscribed with:", email)  # DEBUG CHECK

        send_mail(
            subject="🐾 Welcome to the PetPals Newsletter!",
            message="Thanks for joining! You'll now receive pet care tips, offers, and more 🐕‍🦺",
            from_email="petpalsservice1@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        return render(request, "index.html", {"subscribed": True})

    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # or wherever you want to go
        else:
            # Optional: pass a message to the template
            return render(request, "login_register.html", {"error": "Invalid credentials"})

    return render(request, "login_register.html")


def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Generate unique username
        base_username = slugify(full_name)  # e.g. chris-jord
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}-{get_random_string(4)}"

        # Create Django user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create Profile
        Profile.objects.create(
            username=user,
            full_name=full_name,
            email=email
        )

        # Log user in
        login(request, user)

        # Send welcome email
        send_mail(
            subject="Welcome to PetPals!",
            message=f"Hi {full_name}, thanks for registering with PetPals!",
            from_email="petpalsservice1@gmail.com",
            recipient_list=[email],
            fail_silently=True
        )

        return redirect('index')

    return render(request, "login_register.html")


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def account_view(request):
    return render(request, 'account.html')
