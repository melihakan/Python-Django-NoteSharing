import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting,ContactFormu,ContactFormMessage,UserProfile,FAQ

from content.models import Content, Category, Images, Comment

from home.forms import SearchForm,SignUpForm




def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Content.objects.all()[:4]
    category = Category.objects.all()
    daycontents = Content.objects.all()[:4]
    lastcontents = Content.objects.all().order_by('-id')[:4]
    randomcontents = Content.objects.all().order_by('?')[:4]
    context = {
        'setting': setting,
        'category': category,
        'page' : 'home',
        'sliderdata': sliderdata,
        'daycontents': daycontents,
        'lastcontents': lastcontents,
        'randomcontents': randomcontents

    }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               }
    return render(request, 'hakkimizda.html', context)
def referanslarimiz(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               }
    return render(request, 'referanslarimiz.html', context)
    #return HttpResponse("hello")
def iletisim(request):
    if request.method == 'POST': # check post
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request , "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'form': form
               }

    return render(request, 'iletisim.html', context)

def category_contents(request,id,slug):
    content = Content.objects.filter(category_id=id)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    context = {'content': content,
                'category': category,
                'categorydata': categorydata
               }
    return render(request,'notlar.html',context)

def content_detail(request,id,slug):
    category = Category.objects.all()
    content = Content.objects.get(pk=id)
    image = Images.objects.filter(content_id=id)
    comments = Comment.objects.filter(content_id=id, status='True')
    context = {'category': category,
               'content': content,
               'image': image,
               'comments': comments
               }
    return render(request,'content_detail.html',context)
def content_search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] # get form input data
            #catid = form.cleaned_data['catid']
            #if catid == 0:
            content = Content.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            #else:
                #content = Content.objects.filter(title__icontains=query, category_id=catid)
            context = {'content': content, 'query':query,
                       'category': category }
            return render(request, 'content_search.html', context)

    return HttpResponseRedirect('/')
def content_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        content = Content.objects.filter(title__icontains=q)
        results = []
        for rs in content:
            content_json = {}
            content_json = rs.title +" > " + rs.category.title
            results.append(content_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request , "Login Error")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Success.Welcome :)")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,'form': form}
    return render(request, 'signup.html', context)
def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by("number")
    context = {
        'faq': faq,
        'category': category
    }
    return render(request, 'faq.html', context)