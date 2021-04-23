import pandas as pd

titles = pd.read_csv('titles_metadata.csv')
indices = pd.read_csv("indices_metadata.csv")
movie_link_md = pd.read_csv("movies_metadata.csv")

cosine_sim_keywords = pd.read_csv("cosine_similarity_matrix_metadata.csv", header = None)

def get_recommendations_keywords(title):
    print((indices['title'][indices['title']==title]).index[0])
    idx = (indices['title'][indices['title']==title]).index[0]
    # if idx.size > 1:
    #     idx = idx[0]
    sim_scores = list(enumerate(cosine_sim_keywords[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]
