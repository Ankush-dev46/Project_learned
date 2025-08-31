import pandas as pd
import numpy as np

movies = pd.read_csv('/content/sample_data/dataset.csv')
movies.head()
movies.columns
movies.info()
movies['tags']=movies['genre']+movies['overview']
movies.head()
new_df=movies[['id','title','genre','overview','tags']]
new_df = new_df.drop(columns=['genre','overview'])
new_df.head()
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=10000,stop_words='english')
vec = cv.fit_transform(new_df['tags'].values.astype('U')).toarray()
vec
vec.shape
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vec)
similarity
new_df[new_df['title'] == 'The Shawshank Redemption']
dist = sorted(list(enumerate(sim[0])),reverse=True,key=lambda vector:vector[1])
for i in dist[0:5]:
  print(new_df.iloc[i[0]].title)

def recommend(movie):
  index = new_df[new_df['title'] == movie].index[0]
  distance = sorted(list(enumerate(sim[index])),reverse=True,key=lambda vector:vector[1])
  for i in distance[0:5]:
    print(new_df.iloc[i[0]].title)

recommend('Batman')
