import requests
import streamlit as st

st.title("Similarity")

BASE_URL='http://localhost:8000/cypher'

similarity_cut_off = 0.5

def main():
    st.header("Weighted Jaccard Similarity Calculator")

    # Define sliders for weights

    c1_case_id = st.text_input("Enter case_id")
    k = st.number_input("Enter numnber of simialr cases", min_value = 1, max_value = 3, value = 2)
    with st.container():
        st.subheader("Set Weights for Relationships")
        cites_to_weight = st.slider("Weight for cites_to relationship", 0.0, 1.0, 0.5, 0.1)
        category_weight = st.slider("Weight for category similarity", 0.0, 1.0, 0.4, 0.1)
        court_weight = st.slider("Weight for court similarity", 0.0, 1.0, 0.1, 0.1)

    # Check if weights sum to 1
    if (cites_to_weight + category_weight + court_weight) != 1.0:
        st.warning("Weights must sum to 1.0. Adjust the weights accordingly.")
        return

    query = f'''// Find all pairs of cases (c1, c2) where c1 and c2 are not related by the cites_to relationship
    MATCH (c1:Case), (c2:Case)
    WHERE NOT (c1)-[:cites_to]->(c2) AND c1 <> c2
    WITH c1, c2

    // Count the number of cases c1 cites_to
    OPTIONAL MATCH (c1)-[:cites_to]->(cited1:Case)
    WITH c1, c2, COLLECT(DISTINCT cited1) AS cited_cases_c1

    // Count the number of cases c2 cites_to
    OPTIONAL MATCH (c2)-[:cites_to]->(cited2:Case)
    WITH c1, c2, cited_cases_c1, COLLECT(DISTINCT cited2) AS cited_cases_c2

    // Calculate the intersection and union of cited cases
    WITH c1, c2, cited_cases_c1, cited_cases_c2,
         size(apoc.coll.intersection(cited_cases_c1, cited_cases_c2)) AS intersection_size,
         size(apoc.coll.union(cited_cases_c1, cited_cases_c2)) AS union_size

    WHERE union_size > 0
    WITH c1, c2, intersection_size, union_size,
         toFloat(intersection_size) / union_size AS cites_to_similarity

    OPTIONAL MATCH (c1)-[:is_a]->(cat1:Category)
    OPTIONAL MATCH (c2)-[:is_a]->(cat2:Category)
    WITH c1, c2,cites_to_similarity,
        CASE WHEN id(cat1) = id(cat2) THEN 1 ELSE 0 END as category_similarity

    OPTIONAL MATCH (c1)-[:belongs_to]->(court1:Court)
    OPTIONAL MATCH (c2)-[:belongs_to]->(court2:Court)
    WITH c1, c2, cites_to_similarity, category_similarity,
        CASE WHEN id(court1) = id(court2) THEN 1 ELSE 0 END as court_similarity
    // WHERE c1.case_id = "8626817" and c2.case_id = "8610309"

    WITH c1,c2, {cites_to_weight}*cites_to_similarity + {category_weight}*category_similarity+ {court_weight}* court_similarity as final_similarity_score
    WHERE final_similarity_score >= 0.5 and c1.case_id = "{c1_case_id}"
    RETURN c1.case_id,c2.case_id, final_similarity_score
    ORDER BY final_similarity_score DESC LIMIT {k}'''
    st.success(f"Weights: ({cites_to_weight}, {category_weight}, {court_weight})")
    if st.button("Submit"):
        st.markdown(f"## Cases which are similar to the case {c1_case_id}: ")

        for i in range(k):
            payload = {'query': query}
            res = requests.post(BASE_URL, json=payload)
            if res.status_code == 200:
                ans = res.json()
                ans = ans['answer']
            c2_case_id = ans[i]['c2.case_id']
            query2 = '''
                            MATCH (c1:Case {case_id:"'''+c1_case_id +'''"}), (c2:Case {case_id:"'''+c2_case_id+'''"})
                            OPTIONAL MATCH (c1)-[:cites_to]->(cited:Case)<-[:cites_to]-(c2)
                            OPTIONAL MATCH (c1)-[:is_a]->(cat:Category)<-[:is_a]-(c2)
                            OPTIONAL MATCH (c1)-[:belongs_to]->(court:Court)<-[:belongs_to]-(c2)
                            RETURN c1.case_id AS case_id_1, c2.case_id AS case_id_2,
                            COLLECT(DISTINCT cited.case_id) AS common_cited_cases,
                            cat.category,court.court_name
                            '''
            similarity_score = ans[i]['final_similarity_score']
            st.markdown(f"## :blue[{c2_case_id}]   with a similarity score of {similarity_score}")
            with st.expander(f"How is the case {c1_case_id} similar to the case {c2_case_id}?"):
                payload = {'query': query2}
                res = requests.post(BASE_URL, json=payload)
                if res.status_code == 200:
                    ans2 = res.json()
                    ans2 = ans2['answer']
                common_cited_cases = ans2[0]['common_cited_cases']
                court = ans2[0]['court.court_name']
                category = ans2[0]['cat.category']
                st.write('Both the cases: ')
                if common_cited_cases:
                    st.write(f'cites to :orange[' + ", ".join(common_cited_cases) + ']')
                if court:
                    st.write(f'belong to :orange[' + court + ']')
                if category:
                    st.write(f'are :orange[' + category + 's]')





if __name__ == "__main__":
    main()
