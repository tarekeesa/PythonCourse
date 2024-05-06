from django.shortcuts import render

from products.models import Product




def home_page(request):
    product_list = Product.objects.filter(active=True).order_by('-id')[0:10]
    featured_product_list = Product.objects.filter(active=True, featured=True).order_by('-id')[0:10]
    context = {
        'products' : product_list,
        'featured_product_list':featured_product_list,
        'message' : 'Home Page'
    }
    return render(request, "home_page.html",context)

def about_page(request):
    context = {
        'message' : 'About Us Page'
    }
    return render(request, "home_page.html",context)

def contact_page(request):
    context = {
        'message' : 'Contact Page'
    }
    return render(request, "home_page.html",context)

