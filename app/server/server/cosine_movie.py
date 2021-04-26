import pandas as pd
import subprocess
from sys import argv

# cosine_similarity_matrix = argv[2]
# port = argv[3] if len(argv) > 2 else 5000

# indices file has all the movie titles and corresponding indicies.
cosine_similarity_matrix = "cosine_similarity_matrix.csv"
indices = pd.read_csv("indices.csv", dtype={'title': 'str', 'index': int})

# make a dictionary to store the movies and indices as key-value pairs
movie_to_index = {}
for title,index in zip(indices['title'], indices['index']):
    if title not in movie_to_index:
        movie_to_index[title]=index


def get_recommendations(movie):
    """
    This recommendation recommends the similar movies on the basis of the
    description and tagline of the movie. The description and the tagline columns
    are used to make the cosine similarity matrix.

    Arguments:
        movie: The full name of the movie for which to search. 
    
    Returns:
        A list of top 11 movies on the basis of their cosine similarity with respect to the query movie.
        Also, the list is sorted ascendingly by the cosine similarity so that the most similar movies are first the least similar are last.
    Raises:
        ValueError if the movie is not in the dataset. This also occurs if you misspell the name (e.g. you write Spoderman instead of Spiderman).
    """

    index = movie_to_index[movie]
    process = subprocess.Popen([f"sed -n '{index+2}p' {cosine_similarity_matrix}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    similarity_scores = process.communicate()[0].split(b',')[1:]
    other_movies = sorted(list(zip(indices['title'], similarity_scores)), key=lambda pair: pair[1])[::-1]
    movie_indices = [i[0] for i in other_movies]
    return movie_indices[1:12]
