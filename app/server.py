"""
Starts the server for the movie recommender.
To run it, you have to give the filepath where you keep the cosine similarity matrix, e.g.
    python server.py data/matrix.csv
"""

import math
import pandas as pd
import subprocess
from flask import Flask, request
from sys import argv

cosine_similarity_matrix = argv[1]
indices = pd.read_csv('indices.csv', dtype={'title': 'str', 'index': int})
movie_to_index = {title:index for title, index in zip(indices['title'], indices['index'])}

def similar(movie: str) -> [(str, float)]:
    """
    Find movies similar to a particular movie.
    
    Arguments:
        movie: The full name of the movie for which to search. 
    
    Returns:
        A list of 2-tuples where the first tuple is the name of the other movie and the second tuple is its cosine similarity with the query movie.
        Also, the list is sorted ascendingly by the cosine similarity so that the most similar movies are first the least similar are last.

    Raises:
        ValueError if the movie is not in the dataset. This also occurs if you misspell the name (e.g. you write Spoderman instead of Spiderman).
    """

    index = movie_to_index[movie]
    process = subprocess.Popen([f"sed -n '{index+2}p' {cosine_similarity_matrix}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    similarity_scores = [float(similarity) for similarity in process.communicate()[0].decode('utf-8').split(',')][1:]
    other_movies = sorted(list(zip(indices['title'], similarity_scores)), key=lambda pair: -pair[1])
    
    return other_movies  # we exclude the first movie because it's the query movie

app = Flask(__name__)

@app.route('/recommendation')
def recommendation():
    movie = request.args.get('movie')
    if movie == '':
        return '[]'
    try:
        return str(similar(movie)[:10])
    except KeyError:
        # the movie was not in the dataset,
        # so let's try to find a movie in the dataset whose name starts with the query
        for existing_movie in movie_to_index.keys():
            if (isinstance(existing_movie, str) or not math.isnan(existing_movie)) and existing_movie.startswith(movie):
                return str(similar(existing_movie)[:10])
        return '[]'

if __name__ == "__main__":
    app.run(debug=True)
