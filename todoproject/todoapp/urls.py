from django.urls import path
# imported os accidentally instead of django.urls
from . import views


urlpatterns = [
    path('register/', views.user_register, name='register_user'),
    path('login/', views.user_login, name='login_user'),
    path('todos/', views.get_all_todos, name='get_all_todos'),
    path('todos/add/', views.add_todo, name='add_todo'),
    path('todos/update/<int:pk>', views.update_todo, name='update_todo'),
    path('todos/delete/<int:pk>', views.delete_todo, name='delete_todo'),
]