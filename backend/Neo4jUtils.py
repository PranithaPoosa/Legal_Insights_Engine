from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_community.chat_models import ChatOpenAI
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA


class Neo4jUtils():
    def __init__(self, openai_api_key, url, url_gds, username, password, db):
        self.openai_api_key = openai_api_key
        self.url = url
        self.url_gds = url_gds
        self.username = username
        self.password = password
        self.db = db
        self.driver = None
        self.gds = None
        self.neo4j_graph = None

    def initialize_driver(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(self.url, auth=(self.username, self.password))

    def initialize_gds(self):
        if not self.gds:
            self.gds = GraphDataScience(self.url_gds, auth=(self.username, self.password), database=self.db)

    def initialize_neo4j_graph(self):
        if not self.neo4j_graph:
            self.neo4j_graph = Neo4jGraph(url=self.url, username=self.username, password=self.password)

    def get_CypherQA_chain(self):
        self.initialize_neo4j_graph()

        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0, openai_api_key=self.openai_api_key),
            graph=self.neo4j_graph,
            verbose=True,
            return_intermediate_steps=True
        )
        return chain

    def execute_cypher_query(self, query, parameters=None):
        self.initialize_driver()
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result.data()

    def run_cypher(self, query, params = None):
        self.initialize_gds()
        return self.gds.run_cypher(query, params)

    def get_vectorstore_from_existing_index(self, index_name, text_node_property, retrieval_query):
        return Neo4jVector.from_existing_index(
            OpenAIEmbeddings(openai_api_key=self.openai_api_key),
            url=self.url,
            username=self.username,
            password=self.password,
            index_name=index_name,
            text_node_property=text_node_property,
            retrieval_query=retrieval_query,
        )

    def get_retrievalQA_chain(self, model_name, vector_store, topk=1):
        return RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                openai_api_key=self.openai_api_key,
                model_name=model_name
            ),
            chain_type="stuff",
            retriever=vector_store.as_retriever(k=topk)
        )
