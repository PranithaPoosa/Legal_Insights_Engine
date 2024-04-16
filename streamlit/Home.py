import streamlit as st
import pandas as pd
import json
import requests

st.title('Hi, Welcome to Legal Insights Engine')

BASE_URL = "http://localhost:8000/cypher_gds"

def list_categories():
    query = """
    MATCH (n)
    WITH DISTINCT LABELS(n) AS node_types
    UNWIND node_types AS node_type
    RETURN DISTINCT node_type
    """
    payload = {'query': query}
    res = requests.post(BASE_URL, json=payload)
    data = {}
    if res.status_code == 200:
        data = res.json()
    return data['answer']


def cat_instances(node_name):
    query = """MATCH (n:""" + node_name + """)
            RETURN n {.*}
        """
    payload = {'query': query, 'params': {"nodeName": node_name}}
    res = requests.post(BASE_URL, json=payload)
    if res.status_code == 200:
        data = res.json()
    return data['answer']

def cat_details(cat_name):
    query = """
    match (c:Class { name: $name})
    optional match (c)-[:SCO*0..]->()<-[:DOMAIN]-(outgoing_rel:Relationship)-[:RANGE]->(related_cat:Class)
    with c, collect({ name: outgoing_rel.name, comment: coalesce(outgoing_rel.comment,''), other: related_cat.name }) as outgoing
    optional match (c)-[:SCO*0..]->()<-[:RANGE]-(incoming_rel:Relationship)-[:DOMAIN]->(related_cat:Class)    
    with c, [x in outgoing where x.name is not null| x]  as outgoing, collect({ name: incoming_rel.name, comment: coalesce(incoming_rel.comment,''), other: related_cat.name }) as incoming
    optional match (c)-[:SCO*0..]->()<-[:DOMAIN]-(prop:Property)-[:RANGE]->(datatype)    
    with c, outgoing, [x in incoming where x.name is not null| x] as incoming, collect({ name: prop.name, comment: coalesce(prop.comment,''), type: datatype.name }) as props
    return c.name as name, coalesce(c.comment,'') as def, outgoing, incoming, [x in props where x.name is not null| x] as props
    """
    payload = {'query': query, 'params': {"name": cat_name}}
    res = requests.post(BASE_URL, json=payload)
    if res.status_code == 200:
        data = res.json()
    return data['answer']

def parse_json(json_str):
    try:
        s1 = json.dumps(json_str, default=str)
        return json.loads(s1)
    except json.JSONDecodeError:
        return None

cats = list_categories()
if not cats:
    st.error("No ontology found")
else:
    node_types = [value for key, value in cats.items()]
    nodes_list = [value for key, value in node_types[0].items()]
    selected_class = st.radio(
        "In this DB you will find nodes of the following types",
        nodes_list,
        horizontal=True
    )
    if selected_class == 'Case':
        definition = "a civil or criminal proceeding at law"
        props = {'case_id': 'A unique identifier assigned to a legal case', 'case_name': 'The title or name given to a legal case, reflecting key details or parties involved', 'decision_date':' The date on which a legal decision or judgment was made by a court', 'court_name': 'The name or title of the court responsible for adjudicating a legal case', 'citation': 'A reference or notation providing information about the source and location of a legal case within legal literature'}
        rels = {'➡️ **:blue[has_opinion]**':'Connects a case with the opinion provided by the majority in that case',
                '➡️ **:blue[is_a]**': 'Connects a case with the category to which it belongs, indicating its classification',
                '➡️ **:blue[belongs_to]**': ' Connects a case with the court to which it belongs',
                '➡️ **:blue[cites_to]**': 'Connects a case with another case that the original case cites to, indicating a reference or citation relationship between cases'}


    elif selected_class == 'Opinion':
        definition = 'a formal written statement or document expressing the views, analysis, or decision of a judge'
        props = {'author': 'The individual or entity who authored or wrote the opinion expressed within the legal document',
                 'opinion': 'The written or expressed viewpoint, analysis, or decision rendered by a judge, panel, or legal authority regarding a specific legal issue or case'}
        rels = {'⬅️ **:blue[has_opinion]**': 'Connects a case with the opinion provided by the majority in that case'}

    elif selected_class == 'Court':
        definition = 'a judicial institution responsible for administering justice, adjudicating legal disputes, and interpreting and applying the law within a particular jurisdiction'
        props = {'court_name': 'the name or title of the court'}
        rels = {'⬅️ **:blue[belongs_to]**': ' Connects a case with the court to which it belongs'}
    else:
        definition = 'a classification of legal cases based on the legal issues'
        props = {'category': 'The category or classification assigned to a legal case'}
        rels ={'⬅️ **:blue[is_a]**': 'Connects a case with the category to which it belongs, indicating its classification'}

    with st.sidebar:
        st.markdown("# **:blue[" + selected_class + "]** ")
        st.markdown("_" + definition + "_")
        st.markdown("**Properties:**")
        for keyvalue in props.items():
            st.markdown("**:blue[" + keyvalue[0] + "]** : " + keyvalue[1])
        st.markdown("**Relationships:**")
        for rel in rels.items():
            st.markdown(rel[0] + ': ' + rel[1])

    st.markdown("### Instances of **:blue[" + selected_class + "]**:")

    data = cat_instances(selected_class)
    df = pd.DataFrame(data['n']).T
    st.dataframe(df)

