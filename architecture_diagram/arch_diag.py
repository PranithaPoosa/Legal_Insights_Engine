from diagrams import Cluster, Diagram, Edge
from diagrams.generic.storage import Storage
from diagrams.saas.analytics import Snowflake
from diagrams.onprem.analytics import Dbt
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import Neo4J
from diagrams.programming.framework import Fastapi
from diagrams.programming.language import Python
from diagrams.custom import Custom


with Diagram("Legal Insights Engine", show=True):
    source = Storage("CAP Data")

    airflow = Airflow()
    openai = Custom("OpenAI", "/Users/manideepakreddyaila/Desktop/projects/new/Legal_Insights_Engine/assets/st,small,507x507-pad,600x600,f8f8f8.jpg")
    neo4j = Neo4J("Neo4J")
    fastapi = Fastapi("Backend")
    streamlit = Custom("Frontend", "/Users/manideepakreddyaila/Desktop/projects/new/Legal_Insights_Engine/assets/kn7ucNPv_400x400.png")
    langchain = Custom("Langchain", "/Users/manideepakreddyaila/Desktop/projects/new/Legal_Insights_Engine/assets/lanchain.png")
    knowledge_graph = Custom("Knowledge Graph", "/Users/manideepakreddyaila/Desktop/projects/new/Legal_Insights_Engine/assets/graph-database-ibm-gremlin-graph.jpg")
    snowflake = Snowflake("Data Warehouse")

    with Cluster("Airflow", direction="TB"):
        dbt = Dbt("Transformation")
        python_script = Python("Building Knowledge Graph")
        python_script2 = Python("Embeddings")

        dbt >> python_script >> python_script2

    dbt >> Edge(label = "Transformation") >> snowflake

    python_script2 >> knowledge_graph

    fastapi >> Edge(label = "HTTP requests") >> streamlit
    fastapi << Edge(label="") << streamlit

    knowledge_graph >> fastapi




