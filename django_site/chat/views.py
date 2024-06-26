from django.shortcuts import render, redirect
from django.contrib.auth import login as login_
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Room,Message
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def index(request):
    users = User.objects.all().exclude(username= request.user)

    context = {
        'users':users,
    }
    return render(request, "index.html",context)

@login_required(login_url="login")
def room(request, room_name):
    users = User.objects.all().exclude(username= request.user)
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)

    if request.user != room.first_user:
        if request.user!=room.second_user:
            return redirect("index")

    context = {
        'users':users,
        'room_name':room_name,
        'room':room,
        'messages':messages
    }
    return render(request, "room_v2.html",context)



@login_required(login_url="login")
def video(request,room_name):
    room=Room.objects.get(id=room_name)
    if request.user != room.first_user:
        if request.user!=room.second_user:
            return redirect("index")
    return render(request,"video_chat.html",{"room":room})


@login_required(login_url="login")
def start_chat(request,username):
    second_user=User.objects.get(username=username)
    try:
        room=Room.objects.get(first_user=request.user,second_user=second_user)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user, first_user=second_user)
        except Room.DoesNotExist:

            room=Room.objects.create(first_user=request.user,second_user=second_user)
    return redirect("room",room.id)



def login(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            login_(request, user)
            return redirect("index")
        else:
            return render(request, "login.html")


    return render (request, "login.html")