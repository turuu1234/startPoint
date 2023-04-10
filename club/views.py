from audioop import avg
from ctypes import cast
from django.forms import FloatField
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from point import settings
from .models import User, branch_school, Listing, Img, Rating
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.functions import Coalesce
from django.db.models import Avg, ExpressionWrapper, FloatField

from club import models

# Create your views here.
def index(request):
    listings = Listing.objects.all().annotate(avg_rating=ExpressionWrapper(Avg('rating__rating'), output_field=FloatField())).order_by('-avg_rating')
    return render(request, "club/index.html", {
        "mydatas":listings
    })

def listing(request, id):
    listingData = Listing.objects.get(id=id)
    name = listingData.title
    datas = Listing.objects.filter(title = name)
    return render(request, "club/listing.html", {
        "data":listingData, 
        "datas":datas
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "club/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "club/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "club/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "club/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "club/register.html")




def create(request):
    category = branch_school.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        s_desc = request.POST["s_desc"]
        desc = request.POST["desc"]
        img = request.FILES["uploaded_file"]
        option1 = request.POST["option1"]
        fb_url = request.POST["fb_url"]
        ig_url = request.POST["ig_url"]
        form_link = request.POST["form_url"]
        option = branch_school.objects.get(school_name = option1)
        new = Listing(
            title=title,
            desc_short=s_desc,
            desc_detail=desc,
            image=img,
            fb_link=fb_url,
            ig_link=ig_url,
            category = option,
            owner = request.user,
            form_link=form_link
            # watchlist = request.user
        )
        new.save()
        fs = FileSystemStorage()

        fs.save(img.name, img)
        # message yvuulna
        messages.success(request, 'File uploaded')
    return render(request, "club/create.html",{
                  "categories": category})
def list(request, list_id):
    list = Listing.objects.get(id=list_id)
    return render(request, "club/list.html", {
        "list": list
    })

def profile(request):
    user = request.user
    img = Img.objects.filter(user=user).first() # Get the user's profile picture
    return render(request, 'profile.html', {'user': user, 'img': img})



# def profile(request):
#     if request.method == 'POST' and request.FILES['profile-picture']:
#         img_file = request.FILES['profile-picture']
#         try:
#             img = request.user.img_user
#             img.image = SimpleUploadedFile(img_file.name, img_file.read(), content_type='image/jpeg')
#             img.save()
#         except Img.DoesNotExist:
#             Img.objects.create(image=SimpleUploadedFile(img_file.name, img_file.read(), content_type='image/jpeg'), user=request.user)
#     return redirect('profile')




def bus(request):
    about = branch_school.objects.get(school_name="Шинжлэх ухааны сургууль")
    cards = Listing.objects.filter(category=about)
    listings = cards.annotate(avg_rating=ExpressionWrapper(Avg('rating__rating'), output_field=FloatField())).order_by('-avg_rating')
    
    return render(request, "club/bus.html", {
        "title": about,
        "cards":cards,
        "mydatas":listings
    })


def nus(request):
    about = branch_school.objects.get(school_name="Нийгмийн ухааны сургууль")
    cards = Listing.objects.filter(category=about)
    listings = cards.annotate(avg_rating=ExpressionWrapper(Avg('rating__rating'), output_field=FloatField())).order_by('-avg_rating')
    return render(request, "club/nus.html", {
        "title": about,
        "cards":cards,
        "mydatas":listings
    })

def hshuis(request):
    about = branch_school.objects.get(school_name="Хэрэглээний шинжлэх ухаан инженерчилэлийн сургууль")
    cards = Listing.objects.filter(category=about)
    listings = cards.annotate(avg_rating=ExpressionWrapper(Avg('rating__rating'), output_field=FloatField())).order_by('-avg_rating')
    return render(request, "club/hshuis.html", {
        "title": about,
        "cards":cards,
        "mydatas":listings
    })

def bs(request):
    about = branch_school.objects.get(school_name="Бизнесийн сургууль")
    cards = Listing.objects.filter(category=about)
    listings = cards.annotate(avg_rating=ExpressionWrapper(Avg('rating__rating'), output_field=FloatField())).order_by('-avg_rating')
    return render(request, "club/bs.html", {
        "title": about,
        "cards":cards,
        "mydatas":listings
    })

def ohnus(request):
    about = branch_school.objects.get(school_name="Олон улсын харилцаа, нийтийн удирдлагын сургууль")
    cards = Listing.objects.filter(category=about)
    listings = cards.annotate(avg_rating=ExpressionWrapper(Avg('rating__rating'), output_field=FloatField())).order_by('-avg_rating')
    return render(request, "club/ohnus.html", {
        "title": about,
        "cards":cards,
        "mydatas":listings
    })

def upload(request):
    if request.method == "POST":
        img1 = request.FILES["img"]
        user1 = request.user
        try:
            searched = Img.objects.get(user=user1)
            searched.image = img1
            searched.save()
        except Img.DoesNotExist:
            new = Img(
                image=img1,
                user=user1
            )
            new.save()
        fs = FileSystemStorage()
        fs.save(img1.name, img1)
        return render(request, "club/profile.html")
    

def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    post = Listing.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating, branch= post.category)
    return index(request)

