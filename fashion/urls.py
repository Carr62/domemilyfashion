from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Dress Upload & Management (Dashboard)
    path('dashboard/upload-dress/', views.upload_dress, name='upload_dress'),
    path('dashboard/manage-dresses/', views.manage_dresses, name='manage_dresses'),
    path('dashboard/edit-dress/<int:product_id>/', views.edit_dress, name='edit_dress'),
    path('dashboard/toggle-dress/<int:product_id>/', views.toggle_dress, name='toggle_dress'),
    path('dashboard/delete-dress/<int:product_id>/', views.delete_dress, name='delete_dress'),

    # API
    path('api/products/', views.ProductListAPIView.as_view(), name='api-product-list'),
    path('api/contact/', views.ContactCreateAPIView.as_view(), name='api-contact-create'),
]