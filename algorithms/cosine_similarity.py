#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate


import warnings; warnings.simplefilter('ignore')

cosine_similarity_matrix_destination_file = input('Where should I save the final cosine similarity matrix?')


# In[2]:


md = pd.read_csv('../data/movies_metadata.csv')
md.head()


# In[3]:


md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])


# In[4]:


md['genres']


# In[5]:


# ans = md['genres'].fillna('[]').apply(literal_eval)


# In[6]:


# ans[0]


# In[7]:


vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
C


# In[8]:


m = vote_counts.quantile(0.95)
m


# In[9]:


md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)


# In[10]:


md['year']


# In[11]:


qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')
qualified.shape


# In[12]:


def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)


# In[13]:


qualified['wr'] = qualified.apply(weighted_rating, axis = 1)
qualified = qualified.sort_values('wr', ascending=False).head(250)
qualified


# In[14]:


s = md.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genre'
gen_md = md.drop('genres', axis=1).join(s)


# In[15]:


gen_md


# In[16]:


def build_chart(genre, percentile=0.85):
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)
    
    return qualified


# In[17]:


ans = build_chart('Romance').head(15)


# In[18]:


ans


# In[19]:


links = pd.read_csv('../data/links.csv')
links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')


# In[20]:


links


# In[21]:


md = md.drop([19730, 29503, 35587])


# In[22]:


md['id'] = md['id'].astype('int')


# In[23]:


smd = md[md['id'].isin(links)]
smd.shape


# In[24]:


smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')


# In[25]:


smd['description'][1]


# In[26]:


tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])


# In[27]:


tfidf_matrix.shape


# In[28]:


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


# In[38]:


df = pd.DataFrame(cosine_sim)


# In[30]:


smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])


# In[31]:


def get_recommendations(title):
    idx = indices[title]
    if idx.size > 1:
        idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]


# In[32]:


get_recommendations('Avatar').head(30)


# In[44]:


get_recommendations('Avatar').head(10)


# In[34]:


indices["Avatar"]


# In[35]:


# sim_scores = list(enumerate(cosine_sim[12481]))


# In[36]:


# sim_scores


# In[37]:


# md[md["title"] == "Force Majeure"]


# In[39]:


df.to_csv(cosine_similarity_matrix_destination_file)


# In[42]:





# In[43]:





# In[ ]:



