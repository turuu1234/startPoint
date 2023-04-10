from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("bus", views.bus, name="bus"),
    path("bus/<int:list_id>", views.list, name="list"),
    path("create", views.create, name="create"),
    path("profile", views.profile, name="profile"),
    path("nus", views.nus, name="nus"),
    path("hshuis", views.hshuis, name="hshuis"),
    path("bs", views.bs, name="bs"),
    path("ohnus", views.ohnus, name="ohnus"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("upload", views.upload, name="upload"),
    path('rate/<int:post_id>/<int:rating>/', views.rate),
]


