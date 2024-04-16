import os

import requests
import streamlit as st
from langchain_openai import OpenAIEmbeddings
import snowflake.connector
from datetime import date

st.title('Register a new Case')


BASE_URL = "http://localhost:8000/cypher"

def execute_sql_query(sql, parameters=None):
    conn = snowflake.connector.connect(
        user='manideepak13',
        password='',
        account='rs13501.us-east4.gcp',
        warehouse='CAP_WH',
        database='CAP',
        schema='DEV'
    )
    cursor = conn.cursor()

    cursor.execute(sql, parameters)
    results = cursor.fetchall()
    # st.write(results[0][0])
    cursor.close()
    conn.close()

def main():
    with st.form("case_form"):
        st.subheader("Case")
        case_id = st.text_input("Case ID", value="1155802")
        case_name = st.text_input("Case Name", value = "JANE DOE v. GREENWOOD MEDICAL CENTER")
        decision_date = st.date_input("Decision Date", value = date(2023,9,20))
        citation = st.text_input("Citation", value="335 S.E 271")
        cites_to = st.text_input("Cases this case cites to", value = "8525983")
        cites_to_list = [x.strip() for x in cites_to.split(",")]
        st.subheader("Opinion")
        author = st.text_input("Author", "SMITH, Justice.")
        opinion = st.text_area("Opinion", value = "SMITH, Justice.\nOn September 10, 2021, plaintiff Jane Doe initiated a medical malpractice action against Greenwood Medical Center for personal injuries she sustained during a surgical procedure. Plaintiff alleges that Greenwood Medical Center, through its staff and physicians, negligently performed the surgery, resulting in severe complications and permanent damage to her health.\nDuring the trial proceedings, plaintiff presented evidence demonstrating instances of medical negligence, including improper pre-operative assessments and inadequate post-operative care. Plaintiff's expert witnesses testified to the deviations from the standard of care and the resulting harm suffered by the plaintiff.\nGreenwood Medical Center argued that they followed standard medical procedures and that the complications were unforeseeable. They presented expert testimony to refute the claims of negligence.\nThe trial court, after considering the evidence and testimony presented by both parties, ruled in favor of the plaintiff, finding Greenwood Medical Center liable for medical malpractice. The court awarded damages to the plaintiff for medical expenses, pain and suffering, and loss of income.\nGreenwood Medical Center appealed the decision, contesting the findings of negligence and the awarded damages. The Court of Appeals upheld the trial court's decision, concluding that there was sufficient evidence to support the verdict and the awarded damages.\nOn appeal to the Supreme Court of Greenwood, the court affirmed the decision of the lower courts, emphasizing the importance of adhering to the standard of care in medical procedures and holding Greenwood Medical Center accountable for the negligence that led to the plaintiff's injuries.\nOPINION\nThe evidence presented during the trial clearly demonstrated instances of medical negligence on the part of Greenwood Medical Center. The deviations from the standard of care were substantial, and the resulting harm to the plaintiff was significant. Therefore, we affirm the decision of the lower courts and uphold the verdict in favor of the plaintiff.")
        st.subheader("Court")
        court_name = st.selectbox(label= "Court Name", options=['Supreme Court of North Carolina', 'Court of Appeals of North Carolina', 'North Carolina Court of Appeals'] )
        st.subheader("Category")
        category = st.text_input("Category", value="Medical Malpractice Case")

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        cypher_query = """
        CREATE (c:Case {case_id: $case_id, case_name: $case_name, citation: $citation, decision_date: $decision_date})
        CREATE (o:Opinion {author: $author, opinion: $opinion})
        CREATE (c)-[:has_opinion]->(o)
        WITH c,o
        MATCH (t:Court {court_name: $court_name})
        MATCH (cat:Category {category: $category})
        CREATE (c)-[:belongs_to]->(t)
        CREATE (c)-[:is_a]->(cat)
        WITH c
        MATCH (cc:Case {case_id: $cites_to})
        CREATE (c)-[:cites_to]->(cc)
        """
        payload = {'query': cypher_query, 'params': {'case_id': case_id, "case_name": case_name, "decision_date": decision_date.strftime("%Y-%m-%d"), "citation": citation, "court_name": court_name, "author": author, "opinion": opinion, "category": category, "cites_to": cites_to}}
        res = requests.post(BASE_URL, json=payload)
        if res.status_code == 200:
            ans = res.json()
            ans = ans['answer']

        embeddings_model = OpenAIEmbeddings(openai_api_key = os.environ.get("OPENAI_API_KEY"))
        embedded_query = embeddings_model.embed_query(opinion)
        cypher_query2 = """
        MATCH (o:Opinion {author: $author})
        SET o.embedding = $embedded_query
        """

        payload2 = {'query': cypher_query2, 'params': {'author': author, 'embedded_query': embedded_query}}
        res2 = requests.post(BASE_URL, json = payload2)
        if res2.status_code == 200:
            ans = res2.json()




        #TODO - show the most similar case and also how similar - how???? - don't know (may be path similarity?)

if __name__ == "__main__":
    main()