from django.http import JsonResponse
from django.views.generic import TemplateView


def custom_404_apiview(request, exception=None) -> JsonResponse:
    """Custom 404 error handler that returns a JSON response when a
    page/endpoint is not found.
    """
    return JsonResponse(
        {"detail": "The requested endpoint could not be found."},
        status=404,
    )


class IndexTemplateView(TemplateView):
    """View for rendering the main index.html template
    for index page.
    """

    template_name = "index.html"
