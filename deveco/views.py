from django.shortcuts import render_to_response , redirect , get_object_or_404


def Home(request):
    params = {}
    render_to_response("deveco/")
