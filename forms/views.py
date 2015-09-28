from django.shortcuts import render

# Create your views here.

def formfichestage(request):
    return render_to_response('forms/fichestageform.html')