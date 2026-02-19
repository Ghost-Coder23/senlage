from django.contrib import admin
from django.utils.html import format_html

from .models import Product

admin.site.site_header = "Senlage Investments Administration"
admin.site.site_title = "Senlage Investments Admin"
admin.site.index_title = "Dashboard"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_thumb', 'title', 'subtitle', 'price', 'is_active', 'updated_at')
    list_display_links = ('title',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'subtitle', 'description')
    ordering = ('-updated_at', '-created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20
    readonly_fields = ('image_preview', 'created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'is_active'),
        }),
        ('Pricing & Media', {
            'fields': ('price', 'image', 'image_preview'),
        }),
        ('Description & Features', {
            'fields': ('description', 'features'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Image')
    def image_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="width:44px;height:44px;object-fit:cover;border-radius:10px;border:1px solid #d9e3f1;" />',
                obj.image.url,
                obj.title,
            )
        return '—'

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="max-width:260px;max-height:180px;border-radius:12px;border:1px solid #d9e3f1;" />',
                obj.image.url,
                obj.title,
            )
        return 'No image uploaded'

    class Media:
        css = {
            'all': ('css/admin-product.css',)
        }
