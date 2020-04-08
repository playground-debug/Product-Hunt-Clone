from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    body = models.TextField()
    product = models.IntegerField()

    def __str__(self):
        return f"{self.body} by {self.author}"


class Product(models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField()
    time = models.DateTimeField()
    votes_total = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField()
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:200]

    def date(self):
        return self.time.strftime('%b %e, %Y')


class Upvote(models.Model):
    username = models.CharField(max_length=200)
    product_id = models.IntegerField()

    def __str__(self):
        return f"Product {self.product_id} by {self.username}"


class Message(models.Model):
    body = models.TextField()
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    time = models.DateTimeField()
    product_info = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
