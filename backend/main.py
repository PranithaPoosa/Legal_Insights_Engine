import os

from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Dict, Any

from Neo4jUtils import Neo4jUtils

load_dotenv()
url = os.environ.get("NEO4J_URL")
url_gds = os.environ.get("NEO4J_URL_GDS")
username = os.environ.get("NEO4J_USER")
password= os.environ.get("NEO4J_PASSWORD")
db = os.environ.get("NEO4J_DB")
openai_api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

neo4j_utils = Neo4jUtils(openai_api_key, url, url_gds, username, password, db)

@app.post("/graph_query")
def query_chain(query_params: Dict[str, Any]):
    question = query_params.get("question")
    if not question:
        return {"error": "Question parameter is required"}

    try:
        chain = neo4j_utils.get_CypherQA_chain()
        answer = chain(question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.post("/semantic_query")
def query_index(query_params: Dict[str, Any]):
    question = query_params.get("question")
    index_name = "opinion"
    text_node_property = "opinion"
    contextualized_query = """\n WITH node AS doc, score as similarity
    CALL { WITH doc
        OPTIONAL MATCH (c:Case)-[:has_opinion]->(doc:Opinion)
        RETURN c
    }
    WITH c, similarity, doc
    CALL {
        WITH c
        OPTIONAL MATCH (c)-[:cites_to]->(c1:Case)
        RETURN collect(DISTINCT c1.case_id) AS cited_case_ids
    }
    RETURN 'CASE INFORMATION:: CASE ID IS"' + c.case_id + '",  CASE NAME IS "' +c.case_name + '", DECISION DATE IS "' + c.decision_date + '", CITATION IS "'+ c.citation + '", AND IT CITES TO THE CASES WITH IDs ' + apoc.text.join(cited_case_ids, ' ') + ' AND IT HAS THE FOLLOWING OPINION ' + doc.opinion as text, similarity as score, {} as metadata limit 1 """

    contextualized_vectorstore = neo4j_utils.get_vectorstore_from_existing_index(index_name, text_node_property, contextualized_query)

    if not question:
        return {"error": "Question parameter is required"}

    try:
        response1 = contextualized_vectorstore.similarity_search_with_score(question, k=2)
        vector_plus_context_qa = neo4j_utils.get_retrievalQA_chain(model_name="gpt-3.5-turbo-0125", vector_store=contextualized_vectorstore, topk = 1)
        response = vector_plus_context_qa.run(question)
        return {"answer": response, "query": response1}
    except Exception as e:
        return {"error": str(e)}

@app.post("/cypher_gds")
def run_gds_cypher(query_params: Dict[str, Any]):
    query = query_params.get("query")
    if 'params' in query_params:
        params = query_params.get("params")
        response = neo4j_utils.run_cypher(query, params)
    else:
        response = neo4j_utils.run_cypher(query)
    return {"answer": response}

@app.post("/cypher")
def run_cypher(query_params: Dict[str, Any]):
    query = query_params.get("query")
    if 'params' in query_params:
        params = query_params.get("params")
        response = neo4j_utils.execute_cypher_query(query, params)
    else:
        response = neo4j_utils.execute_cypher_query(query)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


