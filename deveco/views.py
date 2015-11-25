from django.shortcuts import render_to_response , redirect , get_object_or_404


def home(request):
    params = {}
    return render_to_response("deveco/home.html", params)


def home2(request):
    params = {}
    return render_to_response("deveco/home.html", params)


def home3(request):
    params = {}
    return render_to_response("deveco/home.html", params)