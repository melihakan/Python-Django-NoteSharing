
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting,ContactFormu,ContactFormMessage

from content.models import Content, Category, Images, Comment

from home.forms import SearchForm


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
    comments = Comment.objects.filter(content_id=id,status='True')
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
            content = Content.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            context = {'content': content, #'query':query,
                       'category': category }
            return render(request, 'content_search.html', context)

    return HttpResponseRedirect('/')