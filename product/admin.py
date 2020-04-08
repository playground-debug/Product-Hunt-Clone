from django.contrib import admin
from .models import Product, Comment, Upvote, Message

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Upvote)
admin.site.register(Message)
