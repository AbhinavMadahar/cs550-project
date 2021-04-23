import pandas as pd

titles = pd.read_csv('titles.csv')
indices = pd.read_csv("indices.csv")
cosine_sim = pd.read_csv("cosine_similarity_matrix.csv", header = None)

def get_recommendations(title):
    print((indices['title'][indices['title']==title]).index[0])
    idx = (indices['title'][indices['title']==title]).index[0]
    # if idx.size > 1:
    #     idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]
