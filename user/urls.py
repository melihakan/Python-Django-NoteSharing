from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('addnotes/', views.addnotes, name='addnotes'),
    path('notes/', views.notes, name='notes'),
    path('editnotes/<int:id>', views.editnotes, name='editnotes'),
    path('deletenotes/<int:id>', views.deletenotes, name='deletenotes'),

    #path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/

    ]