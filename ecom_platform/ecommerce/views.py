from django.shortcuts import render

from products.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import ContactForm




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

def submit_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Thank you for contacting us!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return render(request, "contact.html")
