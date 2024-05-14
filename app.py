import streamlit as st
import pandas as pd
import pickle

def load_data():
    df = pd.read_csv('data.csv')
    return df

def main():
    st.markdown("Web Mining Assignment 3")

    st.subheader("News articles")

    data = load_data()

    unique_clusters = data['Cluster'].unique()

    selected_cluster = st.sidebar.selectbox("Select Here", unique_clusters)

    st.success(f"Cluster {selected_cluster}")

    cluster_articles = data[data['Cluster'] == selected_cluster]

    for idx, row in cluster_articles.iterrows():
        st.markdown(f"*Title:* {row['Title']}")
        st.markdown(f"*Category:* {row['Category']}")
        st.markdown(f"*Source:* {row['Source']}")
        st.markdown(f"*URL:* {row['Link']}")
        st.write(" ")

# Running the app
if __name__ == "__main__":
    main()
