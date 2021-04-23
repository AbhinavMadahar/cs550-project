from django.shortcuts import render
from .cosine_movie import get_recommendations
from .cosine_metadata import improved_recommendations
from .cosine_keywords import get_recommendations_keywords
# Create your views here.

def index(request):
    result = None
    if request.method == "POST":
        # print("Before",request.POST)
        movie = request.POST.get("movie")
        # print(movie)
        recommendation = request.POST.get("recommendation")
        # print(recommendation)
        if movie:
            if recommendation == "movies": 
                result = get_recommendations(movie).head(10)
                result = list(result['title'])
            elif recommendation == "popularity":
                result = improved_recommendations(movie)
                result = list(result['title'])
            elif recommendation == "keyword":
                result = get_recommendations_keywords(movie).head(10)
                result = list(result['title'])
        else:
            result = "Please Enter Valid Movie Name!"
        # print(result)

    return render(request, 'index.html', {'result':result})
    
