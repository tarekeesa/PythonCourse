from django.shortcuts import render




def home_page(request):
    context = {
        'message' : 'Hello world from context'
    }
    return render(request, "home_page.html",context)
