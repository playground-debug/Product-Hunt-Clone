from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Product, Comment, Upvote, Message
from django.utils import timezone


def homepage(request):
    products = Product.objects
    return render(request, 'products/homepage.html', {'products': products})


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']

            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.time = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'Fill all required fields'})
    else:
        return render(request, 'products/create.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comment = Comment.objects.filter(
        product=product_id).all().order_by('-date')
    return render(request, 'products/detail.html', {'product': product, 'comments': comment})


@login_required(login_url="/accounts/signup")
def comment(request, product_id):
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user
        comment.date = timezone.datetime.now()
        comment.body = request.POST['comment']
        comment.product = int(product_id)
        comment.save()
        product = get_object_or_404(Product, pk=product_id)
        message = Message()
        message.body = "Commented on your Product ~ " + request.POST['comment']
        message.sender = request.user
        message.receiver = product.hunter
        message.time = timezone.datetime.now()
        message.product_info = product
        message.save()
        comment = Comment.objects.filter(
            product=product_id).all().order_by('-date')
        return render(request, 'products/detail.html', {'product': product, 'comments': comment})


@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        try:
            upvote = Upvote.objects.get(
                product_id=product_id, username=request.user)
            product = get_object_or_404(Product, pk=product_id)
            return redirect('/products/' + str(product.id))
        except Upvote.DoesNotExist:
            product = get_object_or_404(Product, pk=product_id)
            product.votes_total += 1
            product.save()
            upvote = Upvote()
            upvote.username = request.user
            upvote.product_id = product_id
            upvote.save()
            message = Message()
            message.body = "Upvoted your Product"
            message.sender = request.user
            message.receiver = product.hunter
            message.time = timezone.datetime.now()
            message.product_info = product
            message.save()
            return redirect('/products/' + str(product.id))


def search(request):
    if request.method == 'GET':
        return render(request, 'products/search.html')

    else:
        if request.POST.get('category') == 'hunter':
            hunter = request.POST['data']
            product = Product.objects.filter(
                hunter__username__icontains=hunter).all()
            return render(request, 'products/search.html', {'products': product})

        if request.POST.get('category') == 'title':
            title = request.POST['data']
            product = Product.objects.filter(title__icontains=title).all()
            return render(request, 'products/search.html', {'products': product})


@login_required(login_url="/accounts/signup")
def profile(request):
    product = Product.objects.filter(hunter=request.user).all()
    context = {
        "products": product,
        "messages": Message.objects.filter(receiver=request.user).count()
    }
    return render(request, 'products/profile.html', context)


@login_required(login_url="/accounts/signup")
def message(request):
    context = {
        "messages": Message.objects.filter(receiver=request.user).all().order_by('-time')
    }
    return render(request, 'products/message.html', context)


@login_required
def discard(request, message_id):
    product = get_object_or_404(
        Message, pk=message_id, receiver=request.user)
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('message'))
