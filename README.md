# Legal_Insights_Engine

![Legal Insights Engine](https://github.com/PranithaPoosa/Legal_Insights_Engine/blob/main/assets/LIE_image.png)

##### Image Source: [LexRatio]
----- 

## Links

[![Streamlit](https://img.shields.io/badge/Streamlit%20Application-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](http://localhost:8501/)  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)](http://localhost:8000/docs)  [![Documentation](https://img.shields.io/badge/Documentation-4285F4?style=for-the-badge&logo=Google&logoColor=white)](https://github.com/PranithaPoosa/Legal_Insights_Engine/blob/main/assets/Legal%20Insights%20Engine_documentation.pdf)  [![Application Demo](https://img.shields.io/badge/Application_Demo-orange?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/embed/ywKlXsZLMv4)  [![Blog Post](https://img.shields.io/badge/Blog_Post-black?style=for-the-badge&logo=Medium&logoColor=white)](https://medium.com/@pranithapoosa.30/legal-insights-engine-simplifying-legal-analysis-for-everyone-804d61a81604)

## Overview
Legal research and decision-making can be complex and time-consuming, often requiring personalized and scenario specific insights tailored to individual preferences. The Legal Insights Engine project endeavors to address this challenge by developing an innovative platform that leverages advanced technologies to provide contextualized semantic search and graph-based recommendations. Users can interact with the system to access comprehensive legal knowledge, analyze historical legal cases, and make informed decisions.

## Objectives
- To develop a scalable and user-friendly platform for analysing and understanding legal case data.
- To create a knowledge graph representing relationships between all the case attributes.
- To provide visualizations and reports for exploring legal cases distribution as per categories and courts.
- To integrate a chatbot with retrieval augmented generation (RAG) capabilities for answering questions about possible outcomes, case details.
- To automate the end-to-end workflow using Apache Airflow for enhanced efficiency and scalability.

## Technologies Used

![Python](https://img.shields.io/badge/python-grey?style=for-the-badge&logo=python&logoColor=ffdd54)
![](https://img.shields.io/badge/FastAPI-4285F4?style=for-the-badge&logo=fastapi&logoColor=white)
![](https://img.shields.io/badge/Neo4J-orange?style=for-the-badge&logo=neo4j&logoColor=white)
![](https://img.shields.io/badge/Apache_Airflow-green?style=for-the-badge&logo=apache-airflow&logoColor=white)
![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![](https://img.shields.io/badge/Snowflake-blue?style=for-the-badge&logo=Snowflake&logoColor=white)
![](https://img.shields.io/badge/dbt-yellow?style=for-the-badge&logo=Dbt&logoColor=white)

## Architecture Diagram

![Legal Insights Engine](https://github.com/PranithaPoosa/Legal_Insights_Engine/blob/main/architecture_diagram/LIE_arch_diag.jpg)

## Project Structure

```
  ├── backend           # FastAPI Component
  │   ├── Neo4JUtils.py            # Utility functions for Neo4J connection and querying    
  │   └── main.py                  # REST API endpoints
  ├── architecture-diagram           # Architecture Diagram
  │   ├── architecture_diagram.py          
  │   └── arts_recommendation_system.png   
  ├── streamlit           # Streamlit Component
  │   ├── pages            
  │   │    └── ... .py
  │   └── Home.py           
  ├── cap_airflow           # Airflow Component
  │   ├── dags            
  │   ├── plugins           
  │   ├── logs           
  │   └── airflow.cfg
  ├── cap_dbt           # DBT
  │   │── models            
  │   │── tests
  │   │── logs            
  │   └── dbt_project.yaml
  ├── .gitignore   
  ├── README.md                         # ReadMe file
  └── requirements.txt                # Requirements for the project
```

## How to run it locally
### Prerequisties
> [!IMPORTANT]
> Install Airflow Standalone and Neo4J Desktop
> Run Neo4j and create a database
> Copy and run the dag to create graph in neo4j

### Streamlit

Step 1 -  Clone the repository on your local system using the below command and Change the directory to streamlit:
```bash
git clone https://github.com/PranithaPoosa/Legal_Insights_Engine
```

Step 2 - Create and activate Virtual Environment
```bash
python -m venv .venv
```
```bash
source .venv/bin/activate
```

Step 3 - Install all the requirements by navigating to the streamlit folder and enter the command:
```bash
pip install -r requirements.txt
```

Step 4 - Run the streamlit application using the below command
```bash
streamlit run src/Home.py
```

Step 5 - The Application will be up on ```http://localhost:8501```

## FastAPI

Step 1 - Open an other tab in the terminal and activate the virtual environment created above

Step 2 - Navigate to backend folder and the Run the FastAPI using the following command:
```bash
uvicorn main:app --reload
```

Step 3 - The Application will be up on ```http://localhost:8000/docs```









