from django.shortcuts import render




def home_page(request):
    context = {
        'message' : 'Home Page'
    }
    return render(request, "base.html",context)

def about_page(request):
    context = {
        'message' : 'About Us Page'
    }
    return render(request, "base.html",context)

def contact_page(request):
    context = {
        'message' : 'Contact Page'
    }
    return render(request, "base.html",context)

