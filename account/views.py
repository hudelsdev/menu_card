from django.shortcuts import render

# Create your views here.

def pay_now(request):
    return render(request,'account/pay_now.html')