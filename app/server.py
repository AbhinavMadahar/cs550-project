"""
Starts the server for the movie recommender.
To run it, you have to give the filepath where you keep the cosine similarity matrix and the filepath where you keep the cosine similarity matrix metadata.
You can optionally give a port; by default, it uses port 5000. 
    python server.py PATH_TO_COSINE_SIMILARITY_MATRIX PATH_TO_COSINE_SIMILARITY_MATRIX_METADATA [PORT]
"""

import math
import pandas as pd
import subprocess
from enum import Enum
from flask import Flask, redirect, request
from sys import argv

cosine_similarity_matrix = argv[1]
cosine_similarity_matrix_metadata = argv[2]
port = argv[3] if len(argv) > 3 else 5000

indices = pd.read_csv('indices.csv', dtype={'title': 'str', 'index': int})
indices_metadata = pd.read_csv('indices_metadata.csv', dtype={'title': 'str', 'index': int})

movie_link_metadata = pd.read_csv('movies_link_metadata.csv')

movie_to_index = {title:index for title, index in zip(indices['title'], indices['index'])}
movie_to_index_metadata = {title:index for title, index in zip(indices_metadata['title'], indices_metadata['index'])}

RecommendationTechniques = Enum('RecommendationTechniques', 'metadata popularity keyword')

def similar(movie: str, technique: RecommendationTechniques) -> [(str, float)]:
    """
    Find movies similar to a particular movie.
    
    Arguments:
        movie: The full name of the movie for which to search. 
        technique: The technique you want to use to find the recommendations.
    
    Returns:
        A list of 2-tuples where the first tuple is the name of the other movie and the second tuple is its cosine similarity with the query movie.
        The query movie is never in this list because it is obviously the most similar.
        Also, the list is sorted ascendingly by the cosine similarity so that the most similar movies are first the least similar are last.

    Raises:
        KeyError if the movie is not in the dataset. This also occurs if you misspell the name (e.g. you write Spoderman instead of Spiderman).
        ValueError if the recommendation technique is invalid.
    """

    if technique == RecommendationTechniques.popularity:
        index = movie_to_index[movie]
        command = f"sed '{index+2}!d;q' {cosine_similarity_matrix}"
        process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        similarity_scores = process.stdout.readline().split(b',')[1:]
        other_movies = sorted(list(zip(indices['title'], similarity_scores)), key=lambda pair: pair[1])[::-1][1:]

    elif technique == RecommendationTechniques.keyword:
        index = movie_to_index_metadata[movie]
        command = f"sed '{index+2}!d;q' {cosine_similarity_matrix_metadata}"
        process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        similarity_scores = process.stdout.readline().split(b',')[1:]
        other_movies = sorted(list(zip(indices_metadata['title'], similarity_scores)), key=lambda pair: pair[1])[::-1][1:]

    elif technique == RecommendationTechniques.metadata:
        top_n = 30  # after using the metadata cosine similarity matrix to sort the other movies, select this many to further investigate

        index = movie_to_index_metadata[movie]
        process = subprocess.Popen([f"sed '{index+2}d;' {cosine_similarity_matrix_metadata}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        similarity_scores = process.communicate()[0].split(b',')[1:]
        index_similar = [index for index, score in sorted(list(enumerate(similarity_scores)), key=lambda pair: pair[1])[:top_n]]

        # calculate the weighted ratings of similar movies.
        movies = movie_link_metadata.iloc[index_similar][['title', 'vote_count', 'vote_average', 'year']]
        vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
        C = vote_averages.mean()
        m = vote_counts.quantile(0.60)
        qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
        v = qualified['vote_count']
        R = qualified['vote_average']
        qualified['wr'] = (v/(v+m) * R) + (m/(m+v) * C)
        other_movies = qualified.sort_values('wr', ascending=False).head(10)

    else:
        raise ValueError(f'{technique} is not a valid recommendation technique.')
    
    return other_movies

app = Flask(__name__)

@app.route('/recommendation')
def recommendation():
    movie = request.args.get('movie')
    technique = request.args.get('technique')
    if movie == '' or technique == '':
        return '[]'
    try:
        return str(similar(movie, RecommendationTechniques[technique])[:10])
    except KeyError:
        return '[]'

@app.route('/')
def homepage():
    return redirect('/static/index.html', code=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
