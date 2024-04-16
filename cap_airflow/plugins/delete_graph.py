import requests
import os

BASE_URL = "http://localhost:8000/cypher"
os.environ["no_proxy"]="*"

def delete_relationships():
    cypher_query = """
                MATCH (n)-[r]->()
                DELETE r
                """
    payload = {'query': cypher_query}
    res = requests.post(BASE_URL, json=payload)
    print(res)
    if res.status_code == 200:
        ans = res.json()
        ans = ans['answer']

def delete_nodes():
    cypher_query = """
                MATCH (n)
                DELETE n
                """
    payload = {'query': cypher_query}
    res = requests.post(BASE_URL, json=payload)
    print(res)
    if res.status_code == 200:
        ans = res.json()
        ans = ans['answer']

def main():
    # print('hi')
    delete_relationships()
    delete_nodes()

if __name__== '__main__':
    main()
