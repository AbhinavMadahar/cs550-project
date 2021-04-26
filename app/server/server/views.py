from django.shortcuts import render
from .cosine_movie import get_recommendations
from .cosine_metadata import improved_recommendations
from .cosine_keywords import get_recommendations_keywords


def index(request):
    result = None
    if request.method == "GET":
    
        movie = request.GET.get("movie")
        
        recommendation = request.GET.get("recommendation")
        
        try:
            if movie:
                if recommendation == "movies":
                    result = get_recommendations(movie)
                elif recommendation == "popularity":
                    result = improved_recommendations(movie)
                elif recommendation == "keyword":
                    result = get_recommendations_keywords(movie)
                    
            else:
                result = ''
        except KeyError:
            result = 'Movie does not exist! Please check your movie spelling.'

    return render(request, 'index.html', {'result':result})
