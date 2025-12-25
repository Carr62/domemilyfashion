from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework import generics
from .models import Product, ContactMessage
from .serializers import ProductSerializer, ContactMessageSerializer
import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
if CLOUDINARY_URL:
    cloudinary.config(cloudinary_url=CLOUDINARY_URL)


def upload_to_cloudinary(file):
    """Upload file to Cloudinary and return the URL."""
    if not CLOUDINARY_URL:
        return None
    try:
        result = cloudinary.uploader.upload(file, folder="domemily/products")
        return result.get('secure_url')
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None


def home(request):
    # Get latest 8 products for the collection grid
    latest_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    return render(request, "fashion/home.html", {
        "products": latest_products
    })

def about(request):
    return render(request, "fashion/about.html")

def contact(request):
    return render(request, "fashion/contact.html")

def product_detail(request, slug):
    """View for individual product detail page."""
    product = get_object_or_404(Product, slug=slug)
    
    # Get related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id).order_by('-created_at')[:4]
    
    return render(request, "fashion/product_detail.html", {
        "product": product,
        "related_products": related_products
    })


# --- DRESS UPLOAD & MANAGEMENT VIEWS ---

def upload_dress(request):
    """View for uploading new dresses."""
    context = {
        'dress_types': Product.DRESS_TYPE_CHOICES,
        'recent_products': Product.objects.filter(category='dresses').order_by('-created_at')[:4],
        'form_data': {},
    }
    
    if request.method == 'POST':
        errors = []
        
        # Get form data
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()
        dress_type = request.POST.get('dress_type', '').strip()
        is_available = request.POST.get('is_available') == 'on'
        image = request.FILES.get('image')
        
        # Store form data for repopulation
        context['form_data'] = {
            'name': name,
            'price': price,
            'description': description,
            'dress_type': dress_type,
        }
        
        # Validation
        if not name:
            errors.append('Dress name is required.')
        if not price:
            errors.append('Price is required.')
        else:
            try:
                price = float(price)
                if price < 0:
                    errors.append('Price must be a positive number.')
            except ValueError:
                errors.append('Invalid price format.')
        if not description:
            errors.append('Description is required.')
        if not dress_type:
            errors.append('Please select a dress type.')
        if not image:
            errors.append('Please upload an image.')
        
        if errors:
            context['errors'] = errors
        else:
            # Upload image to Cloudinary
            image_url = upload_to_cloudinary(image)
            
            if not image_url:
                errors.append('Failed to upload image. Please try again.')
                context['errors'] = errors
            else:
                # Create the product with Cloudinary URL
                product = Product(
                    name=name,
                    category='dresses',
                    dress_type=dress_type,
                    description=description,
                    price=price,
                    image_url=image_url,
                    is_available=is_available,
                )
                product.save()
                
                messages.success(request, f'"{name}" has been uploaded successfully!')
                return redirect('manage_dresses')
    
    return render(request, "fashion/upload_dress.html", context)


def manage_dresses(request):
    """View for managing all dresses."""
    products = Product.objects.filter(category='dresses').order_by('-created_at')
    
    # Filter by status
    current_filter = request.GET.get('filter', '')
    if current_filter == 'available':
        products = products.filter(is_available=True)
    elif current_filter == 'hidden':
        products = products.filter(is_available=False)
    
    # Search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Counts for filter tabs
    all_dresses = Product.objects.filter(category='dresses')
    
    context = {
        'products': products,
        'current_filter': current_filter,
        'search_query': search_query,
        'all_count': all_dresses.count(),
        'available_count': all_dresses.filter(is_available=True).count(),
        'hidden_count': all_dresses.filter(is_available=False).count(),
    }
    
    return render(request, "fashion/manage_dresses.html", context)


def edit_dress(request, product_id):
    """View for editing a dress."""
    product = get_object_or_404(Product, id=product_id, category='dresses')
    
    context = {
        'product': product,
        'dress_types': Product.DRESS_TYPE_CHOICES,
    }
    
    if request.method == 'POST':
        errors = []
        
        # Get form data
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        description = request.POST.get('description', '').strip()
        dress_type = request.POST.get('dress_type', '').strip()
        is_available = request.POST.get('is_available') == 'on'
        image = request.FILES.get('image')
        
        # Validation
        if not name:
            errors.append('Dress name is required.')
        if not price:
            errors.append('Price is required.')
        else:
            try:
                price = float(price)
                if price < 0:
                    errors.append('Price must be a positive number.')
            except ValueError:
                errors.append('Invalid price format.')
        if not description:
            errors.append('Description is required.')
        if not dress_type:
            errors.append('Please select a dress type.')
        
        if errors:
            context['errors'] = errors
        else:
            # Update the product
            product.name = name
            product.dress_type = dress_type
            product.description = description
            product.price = price
            product.is_available = is_available
            
            # Upload new image if provided
            if image:
                image_url = upload_to_cloudinary(image)
                if image_url:
                    product.image_url = image_url
            
            product.save()
            context['success'] = True
            context['product'] = product
    
    return render(request, "fashion/edit_dress.html", context)


def toggle_dress(request, product_id):
    """Toggle dress availability."""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.is_available = not product.is_available
        product.save()
        
        status = "visible" if product.is_available else "hidden"
        messages.success(request, f'"{product.name}" is now {status}.')
    
    return redirect('manage_dresses')


def delete_dress(request, product_id):
    """Delete a dress."""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" has been deleted.')
    
    return redirect('manage_dresses')


# --- API VIEWS ---

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer