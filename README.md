# Legal_Insights_Engine
## Application Link
http://localhost:8051

## CLaaT Document

## Overview
Legal research and decision-making can be complex and time-consuming, often requiring personalized and scenario specific insights tailored to individual preferences. The Legal Insights Engine project endeavors to address this challenge by developing an innovative platform that leverages advanced technologies to provide contextualized semantic search and graph-based recommendations. Users can interact with the system to access comprehensive legal knowledge, analyze historical legal cases, and make informed decisions.

## Business Use Case

## Detailed Approach

## Technologies Used

## Architecture Diagram

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
  ├── README.md                         # ReadMe file
  └── requirements.txt                # Requirements for the project
```

## How to run it locally







