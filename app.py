import streamlit as st
import pandas as pd
import pickle

from keras-preprocessing import *

st.write("""
    # Web Content Mining
""")

st.write("""
    A web-based platform that displays a cluster and the URLs of related stories in that cluster, given a selected category based on 4 online newspapers.
""")

articles = pd.read_csv('News_Articles_Mining-Clustering/clustered_articles.csv')

# Get selected category
selected_category = st.selectbox("Select a category:", ['politics', 'business', 'culture', 'sports'])

st.write('Selected Category:', selected_category)

k_means = pickle.load(open('News_Articles_Mining-Clustering/kmeans_model.pkl', 'rb'))

# Filter articles by selected category
clustered_articles = articles[articles['category'] == selected_category]

# Get unique clusters for the selected category
clusters = clustered_articles['clusters'].unique()

# Get selected cluster from the user
selected_cluster = st.selectbox("Select a cluster:", clusters)

st.write('Selected Cluster:', selected_cluster)

# Filter articles by selected cluster
selected_cluster_articles = clustered_articles[clustered_articles['clusters'] == selected_cluster]

# Display URLs of articles in the selected cluster
st.write('Related Articles:')
st.write(selected_cluster_articles['url'])
