import pandas as pd

# # titles = pd.read_csv('/Users/jainipatel/Spring2021/MDM/archive/titles_metadata.csv')
indices = pd.read_csv("/Users/jainipatel/Spring2021/MDM/archive/indices_metadata.csv")
# # movie_link_md = pd.read_csv("/Users/jainipatel/Spring2021/MDM/archive/movies_metadata.csv")

cosine_sim_metadata = "/Users/jainipatel/Downloads/temp.csv"

# # def weighted_rating(x):
# #     v = x['vote_count']
# #     R = x['vote_average']
# #     return (v/(v+m) * R) + (m/(m+v) * C)

def improved_recommendations(title):
    # print(title)
    idx = (indices['title'][indices['title']==title]).index[0]
    # print(idx)
    # if idx.size > 1:
    #     idx = idx[0]
    sim_scores = list(enumerate(cosine_sim_metadata[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = movie_link_md.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    v = qualified['vote_count']
    R = qualified['vote_average']
    #qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified['wr'] = (v/(v+m) * R) + (m/(m+v) * C)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    return qualified