import os

from django.contrib import admin
from django.template import Library
from django.template.loader import get_template

from ..models import Document


register = Library()


@register.simple_tag(takes_context=True)
def change_list_results(context):

    path = os.path.join(
        os.path.dirname(admin.__file__),
        "templates",
        "admin",
        "change_list_results.html"
    )

    if context["cl"].model == Document:
        path = "admin/documents/document/change_list_results.html"

    return get_template(path).render(context)
