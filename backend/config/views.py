from typing import Callable
from django.http.response import HttpResponse, HttpResponseBase
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.generic.base import RedirectView


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def get_favicon() -> Callable[..., HttpResponseBase]:
    return RedirectView.as_view(
        url="/static/favicon.ico",
        permanent=True,
    )
