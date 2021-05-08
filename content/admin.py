from django.contrib import admin



from content.models import Category,Content
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['status']
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title','category','status']
    list_filter = ['status','category']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Content,ContentAdmin)