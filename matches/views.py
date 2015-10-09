from django.shortcuts import render, get_object_or_404
from matches.models import Match, Result


def detail(request, match_pk):
    match = get_object_or_404(Match, pk=match_pk)
    if request.method == "POST":
        pass
    else:
        pass