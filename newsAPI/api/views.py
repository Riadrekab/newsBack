from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response


from eventregistry import *
er = EventRegistry(apiKey = '62fd2d2a-c90f-4cc1-9b72-ad5f85739368')


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'POST': 'api/users/token/'},
        {'POST': 'api/users/token/refresh/'},
    ]
    return Response(routes)


class getNews(APIView) : 

    def get(self, request):
        q = QueryArticlesIter(
        keywords = QueryItems.OR(["Elon Musk","Messi"]),
        keywordsLoc = "body",
        ignoreKeywords = "SpaceX",
        dateStart = '2023-01-01',
        dateEnd='2023-04-30',
        lang='fra',
        # lang = 'eng',
        )
        listAr = []
        listAr = [article for article in q.execQuery(er, sortBy="rel", returnInfo=ReturnInfo(articleInfo=ArticleInfoFlags(concepts=True, categories=True)), maxItems=50)]
        json_response = json.dumps(listAr, indent=4)

        return Response(json_response)

 