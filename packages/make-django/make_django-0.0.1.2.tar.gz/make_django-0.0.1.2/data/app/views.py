from django.shortcuts import render


def index(request):
    context = {
    }
    return render(request, '%DM_PROJECT_NAME%/index.html', context)
