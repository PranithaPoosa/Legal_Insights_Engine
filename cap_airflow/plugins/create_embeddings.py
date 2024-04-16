from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.embeddings.openai import OpenAIEmbeddings

url = "bolt://localhost:7687"
username = 'neo4j'
password = ""


def main():
    vector_index = Neo4jVector.from_existing_graph(
        OpenAIEmbeddings(openai_api_key = ''),
        url=url,
        username=username,
        password=password,
        index_name='opinion',
        node_label="Opinion",
        text_node_properties=['opinion_text'],
        embedding_node_property='embedding',
    )

if __name__=='__main__':
    main()