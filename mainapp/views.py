from django.shortcuts import render

# Create your views here.

def main(request):
    title = 'Social Media Analytics'
    data = {'title': title}
    return render(request, 'mainapp/base.html', context = data)