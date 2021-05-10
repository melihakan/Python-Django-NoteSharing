from django.contrib import admin



from content.models import Category,Content,Images
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


class ContentImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin2(admin.ModelAdmin):
    list_display = ['title','status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Content,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Content,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title','category','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [ContentImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'content','image_tag']
    readonly_fields = ('image_tag',)



admin.site.register(Category,CategoryAdmin2)
admin.site.register(Content,ContentAdmin)
admin.site.register(Images,ImagesAdmin)