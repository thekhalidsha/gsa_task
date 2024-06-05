from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegistration

from .models import Todo
from .serializers import TodoSerializer


@api_view(["POST", "GET"])
def user_register(req):
    if req.method == "POST":
        username = req.data.get("username")
        password = req.data.get("password")
        if not username or not password:
            return JsonResponse({"error": "empty fields"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username Exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User Created Success"}, status=201)
    elif req.method == "GET":
        form = UserRegistration()
        return render(req, "register.html", {"forms": form})


@api_view(["POST", "GET"])
def user_login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                {
                    "message": "Login Successfully",
                    "username": username,
                },
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "message": "Login Error",
                    "username": username,
                },
                status=400,
            )
    elif request.method == 'GET':
        form = UserRegistration()
        return render(request, "login.html", {"forms": form})


# Create your views here.
# @login_required
@api_view(["GET"])
def get_all_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)
    # return HttpResponse("HelloWorld")


# @login_required
@api_view(["POST"])
def add_todo(request):
    if request.method == "POST":
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @login_required
@api_view(["PUT"])
def update_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @login_required
@api_view(["DELETE"])
def delete_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
