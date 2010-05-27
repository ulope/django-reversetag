from django.template import Library

register = Library()

@register.inclusion_tag("revtest_dummy.html")
def revtest_dummy(view):
    return {'view': view}
