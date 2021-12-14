from django.urls import path

import wiki

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<slug:title>", views.encyclopedia_entry, name="entry"),
    path("new", views.new_entry, name="newentry"),
    path("edit/<slug:title>", views.edit_entry, name="edit")
]
