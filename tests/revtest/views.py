from django.http import HttpResponse

def test_view(request, x=None, y=None, z=None):
    return HttpResponse("Done")
