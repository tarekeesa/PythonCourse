from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


def user_login(request):
    if request.user:
        # return redirect('products:list')
        pass

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print('email',email,password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('products:list')  # Redirect after successful login
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'users/login.html', {'error': 'Passwords do not match'})

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'users/login.html', {'error': e.messages})

        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            # login(request, user)  # Optionally log the user in directly
            return render(request, 'users/login.html', {'success': 'Successful Registrations'})
        except Exception as e:
            return render(request, 'users/login.html', {'error': str(e)})

    return render(request, 'users/login.html')


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/account_detail.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user