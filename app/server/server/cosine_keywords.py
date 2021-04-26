import pandas as pd
import subprocess
from sys import argv

# indices_metadata file has all the movie titles and corresponding indicies.

indices = pd.read_csv("indices_metadata.csv", dtype={'title': 'str', 'index': int})
cosine_similarity_matrix_metadata = "cosine_similarity_matrix_metadata.csv"

# make a dictionary to store the movies and indices as key-value pairs
movie_to_index = {}
for title,index in zip(indices['title'], indices['index']):
    if title not in movie_to_index:
        movie_to_index[title]=index

def get_recommendations_keywords(movie: str) -> [int]:
    """
    This recommendation system recommends similar movies based on the movie
    metadata. The credits and the keywords are taken from the credits.csv,
    which has the details about the cast and crew, and keywords.csv, which has
    the movie plot as keywords. These files are then merged. The cosine
    similiarity matrix is found based on similar words in the keyowrds, cast
    and crew of the movie and the genre of the movie.

    Arguments:
        movie: The full name of the movie for which to search. 
    
    Returns:
        A list of the top 11 movies (giving their index, not their title) on the basis of their cosine similarity with respect to the query movie.
        Also, the list is sorted ascendingly by the cosine similarity so that the most similar movies are first the least similar are last.
    Raises:
        ValueError if the movie is not in the dataset. This also occurs if you misspell the name (e.g. you write Spoderman instead of Spiderman).
    """
    
    index = movie_to_index[movie]
    process = subprocess.Popen([f"sed -n '{index+2}p' {cosine_similarity_matrix_metadata}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    similarity_scores = process.communicate()[0].split(b',')[1:]
    other_movies = sorted(list(zip(indices['title'], similarity_scores)), key=lambda pair: pair[1])[::-1]
    movie_indices = [i[0] for i in other_movies]
    return movie_indices[1:12]
