import pandas as pd
import subprocess
from sys import argv

'''indices_metadata file has all the movie titles and corresponding indicies.
movie_link_md file has detailed information about the movie.'''

indices = pd.read_csv("indices_metadata.csv", dtype={'title': 'str', 'index': int})
movie_link_md = pd.read_csv("movies_link_metadata.csv")

cosine_similarity_matrix_metadata = "cosine_similarity_matrix_metadata.csv"

'''make a dictionary to store the movies and indices as key-value pairs'''
movie_to_index = {}
for title,index in zip(indices['title'], indices['index']):
    if title not in movie_to_index:
        movie_to_index[title]=index

'''This recommendation recommends the similar movies on the basis of the keywords and popularity and ratings of
the movie. The vote counts and average number of votes are obtained from the metadata and weighted ratings are calculated.
The keywords and the cast and crew of the movies are considered to find the cosine similarity matrix.
And top 30 similar movies found using cosine matrix are then sorted on the basis of the weighted ratings and top 10 movies are then recommended to the user.'''


def improved_recommendations(title):
    """
    Arguments:
        movie: The full name of the movie for which to search. 
    
    Returns:
        A list of top 10 movies on the basis of their cosine similarity with respect to the query movie and the popularity and ratings of the movies.
        Also, the list is sorted ascendingly by the cosine similarity so that the most similar movies are first the least similar are last.
    Raises:
        ValueError if the movie is not in the dataset. This also occurs if you misspell the name (e.g. you write Spoderman instead of Spiderman).
    """
    
    index = movie_to_index[title]
    process = subprocess.Popen([f"sed -n '{index+2}p' {cosine_similarity_matrix_metadata}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    similarity_scores = process.communicate()[0].split(b',')[1:]
    other_movies = sorted(list(zip(indices['title'], similarity_scores)), key=lambda pair: pair[1])[::-1]
    other_movies = other_movies[1:30]
    movie_indices = [i[0] for i in other_movies]
    index_similar = [movie_to_index[i] for i in movie_indices]
    #returns indices of the most similar movies found using the cosine matrix.

    #calculating the weighted ratings of similar movies.
    movies = movie_link_md.iloc[index_similar][['title', 'vote_count', 'vote_average', 'year']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
    v = qualified['vote_count']
    R = qualified['vote_average']
    qualified['wr'] = (v/(v+m) * R) + (m/(m+v) * C)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    return list(qualified['title'])
