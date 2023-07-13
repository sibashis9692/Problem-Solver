from django.urls import path
from Home import views
urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', views.admin, name="admin"),
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("views/<int:number>", views.views, name="views"),
    path("logout/", views.logout, name="logout"),
    path("addQuestion/", views.addQuestion, name="addQuestion"),
    path("questions/", views.questions, name="questions"),
    path("edit/<int:number>", views.edit, name="edit"),
    path("delete/<int:number>", views.delete, name="delete")
]
