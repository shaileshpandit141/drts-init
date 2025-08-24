from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    """Rendering index.html template page."""

    template_name = "index.html"
