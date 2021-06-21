from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from content.models import Category, Comment, Content, ContentImageForm, CImages
from django.contrib.auth.decorators import login_required

from user.forms import UserUpdateForm, ProfileUpdateForm, UserNotesForm

from home.models import UserProfile


def index(request):
    category = Category.objects.all()

    current_user = request.user
    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {'category': category,
               'profile': profile
               }
    return render(request,'user_profile.html',context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form,'category': category
                       })

def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request,'Comment Deleted..')
    return HttpResponseRedirect('/user/comments')
@login_required(login_url='login')
def notes(request):
     category = Category.objects.all()
     current_user = request.user
     #notes = Content.objects.filter(user_id = current_user.id)
     notes = Content.objects.all()
     #form = UserNotesForm()
     context = {
         'category': category,
         'notes': notes,
     }
     return render(request, 'user_notes.html', context)

@login_required(login_url='login')
def addnotes(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = UserNotesForm(request.POST,request.FILES) # request.user is user  data
        if form.is_valid():
            #current_user = request.user
            data = Content()
            #data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.detail = form.cleaned_data['detail']
            data.image = form.cleaned_data['image']
            data.file = form.cleaned_data['file']
            data.status= 'False'
            data.category = form.cleaned_data['category']
            data.save()
            return HttpResponseRedirect('/user/notes')
        else:
            return HttpResponseRedirect('/user/addnotes')
    else:
        category = Category.objects.all()
        current_user = request.user
        notes = Content.objects.all()
        form = UserNotesForm()
        context = {
            'category': category,
            'notes': notes,
            'form':form,
        }
        return render(request, 'user_addnotes.html', context)
@login_required(login_url='login')
def editnotes(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = UserNotesForm(request.POST,request.FILES,instance=content)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated')
            return HttpResponseRedirect('/user/notes')
        else:
            messages.success(request, 'ERROR')
            return HttpResponseRedirect('/user/editnotes')
    else:
        category = Category.objects.all()
        form = UserNotesForm(instance=content)
        context = {
            'category': category,
            'form':form,
        }
        return render(request,'user_editnotes.html',context)


@login_required(login_url='login')
def deletenotes(request,id):
    Content.objects.filter(id=id).delete()
    return HttpResponseRedirect('/user/notes')


def addimages(request,id):
    if request.method == 'POST':

        lasturl = request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST,request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request,'Uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request,'ERROR')
            return HttpResponseRedirect(lasturl)
    else:
        category = Category.objects.all()
        content = Content.objects.get(id=id)
        images=[]
        form = ContentImageForm()
        context = {
            'content': content,
            'images': images,
            'form': form,
            'category': category,
        }
        return render(request,'content_gallery.html',context)