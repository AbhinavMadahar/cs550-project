from django.shortcuts import render
from .cosine_movie import get_recommendations
from .cosine_metadata import improved_recommendations
from .cosine_keywords import get_recommendations_keywords
# Create your views here.

def index(request):
    result = None
    if request.method == "GET":
        # print("Before",request.POST)
        movie = request.GET.get("movie")
        # print(movie)
        recommendation = request.GET.get("recommendation")
        # print(recommendation)
        if movie:
            if recommendation == "movies":
                result = get_recommendations(movie)
            elif recommendation == "popularity":
                result = improved_recommendations(movie)
                result = list(result['title'])
            elif recommendation == "keyword":
                result = get_recommendations_keywords(movie)
                # result = list(result['title'])
        else:
            result = ''
        # print(result)

    return render(request, 'index.html', {'result':result})
