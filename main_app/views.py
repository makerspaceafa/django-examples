from django.shortcuts import render
from django.urls import get_resolver, URLResolver


# Create your views here.
def index(request):
    app_urls = []
    for url in get_resolver().url_patterns:

        path = str(url.pattern)

        # this is to exclude the main_app url path -> path('', main.index)
        if path:
            # url is a URLResolver in case of using include()
            if type(url) == URLResolver:
                app_urls.append((path, url.namespace))
            # else, it's a good 'ol URLPattern with a name field!
            else:
                app_urls.append((path, url.name))

    return render(request, 'main_app/index.html', {'app_urls': app_urls})
