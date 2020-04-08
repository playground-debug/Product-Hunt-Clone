from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/comment', views.comment, name='comment'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
    path('search', views.search, name='search'),
    path('profile', views.profile, name='profile'),
    path('message', views.message, name='message'),
    path('discard/<int:message_id>', views.discard, name='discard')
]
