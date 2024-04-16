import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
from bokeh.transform import factor_cmap
from bokeh.palettes import Category20
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import requests
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource

st.set_option('deprecation.showPyplotGlobalUse', False)
BASE_URL='http://localhost:8000/cypher'

def run_query(query):
    payload = {'query': query}
    res = requests.post(BASE_URL, json=payload)
    if res.status_code == 200:
        ans = res.json()
        ans = ans['answer']
    return pd.DataFrame(ans)

def plot_heatmap_court_case():
    query = """
    MATCH (c:Case)-[:belongs_to]->(ct:Court), (c)-[:is_a]->(cat:Category)
    RETURN ct.court_name AS Court, cat.category AS Category, COUNT(c) AS CaseCount
    """
    st.title('Case Distribution by Court and Category')
    case_distribution_df = run_query(query)
    pivot_df = case_distribution_df.pivot(index='Court', columns='Category', values='CaseCount')
    # st.write(pivot_df)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df, cmap='coolwarm', annot=True, fmt='.0f')
    plt.title('Case Distribution by Court and Category')
    plt.xlabel('Category')
    plt.ylabel('Court')
    plt.tight_layout()
    plt.show()

    st.pyplot(plt)

def plot_opinion_embeddings(df):
    embeddings_array = np.array(df['embedding'].tolist())
    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings_array)
    bokeh_df = pd.DataFrame(embeddings_2d, columns=['x', 'y'])
    bokeh_df['case_id'] = df['case_id']
    bokeh_df['category'] = df['category']

    source = ColumnDataSource(bokeh_df)

    categories = bokeh_df['category'].unique()
    colors = Category20[len(categories)]

    if len(categories) > len(colors):
        raise ValueError("Number of categories exceeds the number of available colors")

    p = figure(title='Opinion Embeddings in 2D Space', width=800, height=600)
    p.scatter('x', 'y', size=10, source=source, legend_field='category',fill_color=factor_cmap('category', palette=colors, factors=categories))

    hover = HoverTool(tooltips=[("case_id", "@case_id")])
    p.add_tools(hover)

    p.title.text_font_size = '16px'
    p.legend.title = 'Category'

    st.bokeh_chart(p)


def plot_horizontal_bar_chart_category_distribution():
    query = """
    MATCH (c:Case)-[:is_a]->(cat:Category)
    RETURN cat.category AS Category, COUNT(c) AS CaseCount
    ORDER BY CaseCount DESC
    """
    st.title('Distribution of Cases Across Different Categories')
    category_distribution_df = run_query(query)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='CaseCount', y='Category', data=category_distribution_df, palette='viridis')
    plt.title('Distribution of Cases Across Different Categories')
    plt.xlabel('Number of Cases')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.show()

    st.pyplot(plt)

def opinion_embedding_2d():
    st.title('Opinion Embedding Visualization')
    query = """
        MATCH (c:Case)-[:has_opinion]->(o:Opinion)
        OPTIONAL MATCH (c)-[:is_a]->(cat:Category)
        WHERE o.embedding is not null
        RETURN o.embedding AS embedding, c.case_id as case_id, cat.category as category
        """
    opinion_embeddings_df = run_query(query)
    plot_opinion_embeddings(opinion_embeddings_df)

if __name__ == '__main__':
    query = """
        MATCH (c:Case)
        RETURN count(c) AS NumberOfCases
        """
    result = run_query(query)

    if result.any().item():
        num_cases= result.iloc[0,0]
        st.title(f'Total number of cases analyzed: **:blue[{num_cases}]**')
    plot_heatmap_court_case()
    opinion_embedding_2d()
    plot_horizontal_bar_chart_category_distribution()
