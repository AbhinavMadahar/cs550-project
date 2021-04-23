import pandas as pd

cosine_similarity_matrix = pd.read_csv('cosine_similarity_matrix.csv')
movies_metadata = pd.read_csv('movies_metadata.csv')

def similar(movie: str) -> [(str, float)]:
    """
    Find movies similar to a particular movie.
    
    Arguments:
        movie: The full name of the movie for which to search. 
               This is case insensitive.
    
    Returns:
        A list of 2-tuples where the first tuple is the name of the other movie and the second tuple is its cosine similarity with the query movie.
        Note that the query movie is never in this list.
        Also, the list is sorted ascendingly by the cosine similarity so that the most similar movies are first the least similar are last.

    Raises:
        ValueError if the movie is not in the dataset. This also occurs if you misspell the name (e.g. you write Spoderman instead of Spiderman).
    """
    
    raise NotImplementedError