import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import requests

BASE_URL='http://localhost:8000/cypher'

st.header("Explore the cases")
node_types = ['Case', 'Opinion', 'Court', 'Category']

params = st.experimental_get_query_params()
case_id = params.get("case_id", [""])[0]

st.subheader('Filters')
if case_id:
    case_id = st.text_input(label="Case_id", placeholder="Enter a case_id", value=case_id)
    selected_nodes = st.multiselect('Node Types', node_types, default=node_types)

else:
    case_id = st.text_input(label="Case_id", placeholder="Enter a case_id")
    selected_nodes = st.multiselect('Node Types', node_types, default=None)




def create_nodes_and_edges(data):
    nodes = []
    edges = []
    case_id = str(data[0]["c"]["case_id"])
    nodes.append(Node(id=case_id, label=f"Case: {case_id}"))

    if 'q' in data[0].keys() and data[0].get("q", []):
        opinions = data[0].get("q", [])
        opinions.pop(0)
        opinions.pop(0)
        for opinion in opinions:
            opinion_author = opinion["author"]
            nodes.append(Node(id=opinion_author, label=f"Author: {opinion_author}", color="green"))
            edges.append(Edge(source=case_id, target=opinion_author, label="has_opinion"))

    if 'r' in data[0].keys() and data[0].get("r", []):
        courts = data[0].get("r", [])
        courts.pop(0)
        courts.pop(0)
        for court in courts:
            court_name = court['court_name']
            nodes.append(Node(id=court_name, label=f"Court: {court_name}", color="pink"))
            edges.append(Edge(source=case_id, target=court_name, label="belongs_to"))

    if 's' in data[0].keys() and data[0].get("s", []):
        categories = data[0].get("s", [])
        categories.pop(0)
        categories.pop(0)
        for category in categories:
            category_value = category['category']
            nodes.append(Node(id=category_value, label=f"Category: {category_value}", color='orange'))
            edges.append(Edge(source=case_id, target=category_value, label="is_a"))

    for item in data:
        if 'p' in item.keys() and item.get("p", []):
            cited_cases = item.get("p", [])
            cited_cases.pop(0)
            cited_cases.pop(0)
            for cited_case in cited_cases:
                cited_case_id = str(cited_case["case_id"])
                nodes.append(Node(id=cited_case_id, label=f"Case: {cited_case_id}", color = "black"))
                edges.append(Edge(source=case_id, target=cited_case_id, label="cites_to"))

    return nodes, edges

if st.button("Submit"):
    cypher_query = "MATCH (c: Case {case_id: '" + case_id + "'})"

    if "Case" in selected_nodes:
        cypher_query += " OPTIONAL MATCH p = (c)-[: cites_to]->()"
    if "Opinion" in selected_nodes:
        cypher_query += "  OPTIONAL MATCH q= (c)-[: has_opinion]->()"
    if "Court" in selected_nodes:
        cypher_query += " OPTIONAL MATCH r= (c)-[: belongs_to]->(court: Court)"
    if "Category" in selected_nodes:
        cypher_query += " OPTIONAL MATCH s= (c)-[: is_a]->(category: Category)"

    return_statement = "RETURN c"

    if "Case" in selected_nodes:
        return_statement += ", p"
    if "Opinion" in selected_nodes:
        return_statement += ", q"
    if "Court" in selected_nodes:
        return_statement += ", r"
    if "Category" in selected_nodes:
        return_statement += ", s"

    cypher_query += " " + return_statement

    payload = {'query': cypher_query}
    res = requests.post(BASE_URL, json=payload)
    if res.status_code == 200:
        ans = res.json()
        ans = ans['answer']
    nodes, edges = create_nodes_and_edges(ans)
    config = Config(width=1000,
                    height=700,
                    directed=True,
                    physics=False,
                    hierarchical=False,
                    )

    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)

    cypher_query2 = f"MATCH (c:Case) -[r]->(o:Opinion) where c.case_id = '{case_id}' return o.opinion"
    payload = {'query': cypher_query2}
    res = requests.post(BASE_URL, json=payload)
    if res.status_code == 200:
        ans = res.json()
        ans = ans['answer']
    st.markdown("# Majority Opinion: ")
    st.markdown(f"### {ans[0]['o.opinion']}")



