# Legal_Insights_Engine

![Legal Insights Engine](https://github.com/PranithaPoosa/Legal_Insights_Engine/blob/main/assets/LIE_image.png)

##### Image Source: [LexRatio]
----- 

[![Streamlit](https://img.shields.io/badge/Streamlit%20Application-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](http://localhost:8501/)  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)](http://localhost:8000/docs)  [![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1K5KXsSgMQ-jTM3fTJxYQWo1an-y66M_F1NfkNllJC_g#0)  [![Demo Link](https://img.shields.io/badge/Demo_Link-808080?style=for-the-badge&logo=YouTube&logoColor=white)](https://drive.google.com/file/d/170hl_0gA1Rog9UF96av5BJ_DmRD4bzvq/view?usp=drivesdk)

## Overview
Legal research and decision-making can be complex and time-consuming, often requiring personalized and scenario specific insights tailored to individual preferences. The Legal Insights Engine project endeavors to address this challenge by developing an innovative platform that leverages advanced technologies to provide contextualized semantic search and graph-based recommendations. Users can interact with the system to access comprehensive legal knowledge, analyze historical legal cases, and make informed decisions.

## Business Use Case

## Detailed Approach

## Technologies Used

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







