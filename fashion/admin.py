from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ContactMessage


# Customize Admin Site Header
admin.site.site_header = "DOMEMILY Admin"
admin.site.site_title = "DOMEMILY Fashion"
admin.site.index_title = "Welcome to Domemily Dashboard"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Enhanced admin interface for managing products/dresses."""
    
    # List display columns
    list_display = ['image_preview', 'name', 'category', 'dress_type_display', 'formatted_price', 'is_available', 'created_at']
    list_display_links = ['image_preview', 'name']
    
    # Filtering and searching
    list_filter = ['category', 'dress_type', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    
    # Editable fields directly in list view
    list_editable = ['is_available']
    
    # Ordering
    ordering = ['-created_at']
    
    # Items per page
    list_per_page = 20
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'created_at'
    
    # Prepopulate slug from name
    prepopulated_fields = {'slug': ('name',)}
    
    # Organize fields into sections
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'category', 'dress_type', 'description'),
            'description': 'Enter the basic product details'
        }),
        ('Pricing', {
            'fields': ('price',),
            'description': 'Set the product price in Ghana Cedis (₵)'
        }),
        ('Image', {
            'fields': ('image', 'image_tag'),
            'description': 'Upload a high-quality product image (recommended: 800x1200px)'
        }),
        ('Availability', {
            'fields': ('is_available',),
            'description': 'Toggle to show/hide product on the website'
        }),
    )
    
    # Make image_tag read-only
    readonly_fields = ['image_tag', 'created_at']
    
    def dress_type_display(self, obj):
        """Display dress type or dash if not applicable."""
        if obj.dress_type:
            return obj.get_dress_type_display()
        return "-"
    dress_type_display.short_description = 'Dress Type'
    dress_type_display.admin_order_field = 'dress_type'
    
    # Custom methods for display
    def image_preview(self, obj):
        """Show small thumbnail in list view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 65px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Preview'
    
    def image_tag(self, obj):
        """Show larger image preview in detail view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 400px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999; font-style: italic;">No image uploaded yet</span>')
    image_tag.short_description = 'Image Preview'
    
    def formatted_price(self, obj):
        """Display price with currency symbol."""
        return format_html('<strong style="color: #8B4513;">₵{}</strong>', obj.price)
    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'
    
    # Custom actions
    actions = ['make_available', 'make_unavailable']
    
    @admin.action(description='✅ Mark selected products as available')
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} product(s) marked as available.')
    
    @admin.action(description='❌ Mark selected products as unavailable')
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} product(s) marked as unavailable.')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for viewing contact form submissions."""
    
    list_display = ['name', 'email', 'short_message', 'created_at', 'is_read']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    # Make messages read-only (they come from the contact form)
    readonly_fields = ['name', 'email', 'message', 'created_at']
    
    fieldsets = (
        ('Contact Details', {
            'fields': ('name', 'email')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def short_message(self, obj):
        """Truncate long messages in list view."""
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    short_message.short_description = 'Message'
    
    def is_read(self, obj):
        """Visual indicator (placeholder - could be extended with actual read tracking)."""
        return format_html('<span style="color: #28a745;">●</span> New')
    is_read.short_description = 'Status'
    
    # Disable add/edit since these come from the contact form
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
