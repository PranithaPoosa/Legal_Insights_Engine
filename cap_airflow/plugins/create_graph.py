from neo4j import GraphDatabase
import snowflake.connector
import pandas as pd

def create_graph():
    # Connect to Snowflake
    snowflake_account = 'rs13501.us-east4.gcp'
    snowflake_user = 'CAP_USER'
    snowflake_password = ''
    snowflake_database = 'CAP'
    snowflake_schema = 'DEV'
    snowflake_table = 'AGGREGATION'
    snowflake_conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database,
        schema=snowflake_schema
    )

    snowflake_cursor = snowflake_conn.cursor()
    snowflake_cursor.execute("USE ROLE CAP_DEV")
    snowflake_cursor.execute("USE WAREHOUSE CAP_WH")
    snowflake_cursor.execute(f"SELECT * FROM CAP.DEV.{snowflake_table}")
    snowflake_data = snowflake_cursor.fetchall()

    df = pd.DataFrame(snowflake_data, columns=[desc[0] for desc in snowflake_cursor.description])
    print(df['CITES_TO'])

    print(df.info())
    snowflake_conn.close()

    # Connect to Neo4j
    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = ""
    neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def create_graph_tx(tx):
        for index, row in df.iterrows():
            # Create Case node
            tx.run(
                "MERGE (c:Case {case_id: $case_id, case_name: $case_name, citation: $citation, decision_date: $decision_date})",
                case_id=row['CASE_ID'],
                case_name=row['CASE_NAME'],
                citation=row['CITATION'],
                decision_date=row['DECISION_DATE']
            )

            # Create Opinion node and 'has_opinion' relationship
            tx.run(
                "MATCH (c:Case {case_id: $case_id}) "
                "MERGE (o:Opinion {opinion_text: $opinion_text, author: $author}) "
                "MERGE (c)-[:has_opinion]->(o)",
                case_id=row['CASE_ID'],
                opinion_text=row['OPINION_TEXT'],
                author=row['AUTHOR']
            )

            # Create Court node
            tx.run(
                "MERGE (ct:Court {court_name: $court_name})",
                court_name=row['COURT_NAME']
            )

            # Create 'belongs_to' relationship between Case and Court
            tx.run(
                "MATCH (c:Case {case_id: $case_id}), (ct:Court {court_name: $court_name}) "
                "MERGE (c)-[:belongs_to]->(ct)",
                case_id=row['CASE_ID'],
                court_name=row['COURT_NAME']
            )

            # Create Category node and 'is_a' relationship
            tx.run(
                "MATCH (c:Case {case_id: $case_id}) "
                "MERGE (ca:Category {category: $category}) "
                "MERGE (c)-[:is_a]->(ca)",
                case_id=row['CASE_ID'],
                category=row['CATEGORY']
            )

            # Create 'cites_to' relationships
            cites_to = row['CITES_TO'].replace("\n", "").replace(" ", "").replace('"', "").replace('[', "").replace(']',
                                                                                                                    "").split(
                ",")
            for cited_case_id in cites_to:
                tx.run(
                    "MATCH (c1:Case {case_id: $case_id}), (c2:Case {case_id: $cited_case_id}) "
                    "MERGE (c1)-[:cites_to]->(c2)",
                    case_id=row['CASE_ID'],
                    cited_case_id=cited_case_id
                )

    with neo4j_driver.session() as session:
        session.write_transaction(create_graph_tx)

    neo4j_driver.close()

def main():
    create_graph()

if __name__ == '__main__':
    main()
