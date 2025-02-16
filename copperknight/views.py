import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import User,Opus,FavoritedOpus
# Create your views here.

# Amount of posts shown in paginator
PAGIVALUE = 10

def index(request):
    # filter by newest and public
    opus = Opus.objects.filter(img_private=False).order_by('-created_at').first()
    context = {
        'opus': opus
    }
    return render(request, "copperknight/index.html", context)

def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "copperknight/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "copperknight/register.html", {
                "message": "Invalid email address."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "copperknight/register.html")

@csrf_protect
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "copperknight/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "copperknight/index.html", {
                "message": "Invalid username and/or password."
            })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def to_draw(request): # for drawing new pictures
    return render(request, "copperknight/draw.html")


def save_to_gallery(request):
    if request.method == 'POST':
        image_data = request.POST.get('imageData')
        title = request.POST.get('title')
        isPrivate = request.POST.get('isPrivate')

        # Turns 'true' to 'True' :/
        if isPrivate == 'true':
            img_private = True
        elif isPrivate == 'false':
            img_private = False
        else:
            print('PRIVATE ERROR') # just in case

        print(isPrivate)
        print("image got")
        created_by = request.user
        created_at = timezone.now()
        print("saving image")

        opus = Opus(title=title, base64_image=image_data, created_by=created_by, created_at=created_at,img_private=img_private)
        opus.save()
        print("image saved!")

        response_data = {
            'message': 'Image saved to gallery successfully!'
        }
        return JsonResponse(response_data)

    response_data = {
        'error': 'Invalid request!'
    }
    return JsonResponse(response_data, status=400)


def deleteopus(request):
    if request.method == 'POST':
        id = request.POST.get('id')

        try:
            opus = Opus.objects.get(id=id)
            opus.delete()

            return redirect('gallery')
        except Opus.DoesNotExist:
            response_data = {
                'error': 'Entry does not exist!'
            }
            return JsonResponse(response_data, status=400)

    response_data = {
        'error': 'Invalid request!'
    }
    return JsonResponse(response_data, status=400)


def gallery(request):
    opus_list = Opus.objects.filter(created_by=request.user).order_by('-created_at')

    paginator = Paginator(opus_list, PAGIVALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'copperknight/gallery.html', context)

def profile(request, created_by):
    user = User.objects.get(username=created_by)
    artist = user
    opus_list = Opus.objects.filter(created_by=user, img_private=False)

    paginator = Paginator(opus_list, PAGIVALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'artist': artist
    }

    return render(request, 'copperknight/profile.html', context)


def showcase(request):
    opus_list = Opus.objects.filter(img_private=False).order_by('-created_at')

    paginator = Paginator(opus_list, PAGIVALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'copperknight/showcase.html', context)


def saveopus(request):
    if request.method == 'POST':
        base64_image = request.POST.get('base64_Image')  # Note the uppercase 'I'
        user = request.user
        print(base64_image)
        print(user)

        opus_list = Opus.objects.filter(base64_image=base64_image)

        if opus_list.exists():
            opus = opus_list.first()
            favorited_opus = FavoritedOpus(user=user, opus=opus)
            favorited_opus.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Opus does not exist'})


    return JsonResponse({'success': False}, status=405)

def killopus(request): # unfavorites an Opus
    if request.method == 'POST':
        base64_image = request.POST.get('base64_Image')
        user = request.user
        print(base64_image)
        print(user)

        favorited_opus_list = FavoritedOpus.objects.filter(user=user, opus__base64_image=base64_image)

        if favorited_opus_list.exists():
            favorited_opus_list.delete()
            return redirect('favorited')

    return JsonResponse({'success': False}, status=405)


def favorited(request):
    favorited_opus_list = FavoritedOpus.objects.filter(user=request.user)
    opus_set = set()
    for favorited_opus in favorited_opus_list:
        opus_set.add(favorited_opus.opus)

    opus_list = list(opus_set)
    paginator = Paginator(opus_list, PAGIVALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'copperknight/favorited.html', context)

def searchopus(request):
    if request.method == 'GET':
        search_query = request.GET.get('artsearch')
        user = request.user

        opus_list = Opus.objects.filter(title__icontains=search_query, img_private=False).order_by('-created_at')

        paginator = Paginator(opus_list, PAGIVALUE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'search_query': search_query
        }

        return render(request, 'copperknight/search.html', context)

    return JsonResponse({'success': False}, status=405)


def follow(request, username):
    artist = get_object_or_404(User, username=username)
    user = request.user
    user.following.add(artist)
    print("follow success")
    return redirect("profile", artist)

def unfollow(request, username):
    artist = get_object_or_404(User, username=username)
    user = request.user
    user.following.remove(artist)
    print("unfollow success")
    return redirect("profile", artist)

def following(request):
    following = request.user.following.all()
    opus_list = Opus.objects.filter(created_by__in=following, img_private=False).order_by('-created_at')

    paginator = Paginator(opus_list, PAGIVALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'copperknight/following.html', context)