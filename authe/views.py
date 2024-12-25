from django.shortcuts import render

# Create your views here.
def Login_auth(request):
    return render(request, 'authenticate/login.html')

def Register_auth(request):
    return render(request, 'authenticate/register.html')