from django.http import JsonResponse


def getRoutes(request):

    routes = [
        {'POST': 'api/users/token/'},
        {'POST': 'api/users/token/refresh/'},
    ]
    return JsonResponse(routes, safe=False)
