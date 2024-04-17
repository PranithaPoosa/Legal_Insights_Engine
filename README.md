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
  ├── assets           # images used for readme
  │   └── ... .png
  ├── architecture-diagram
  │   ├── architecture_diagram.py          # architectural diagram python code    
  │   └── arts_recommendation_system.png   # architectural diagram png
  ├── dashboard
  │   ├── home.py                     # code to user dashboard
  │   └── display_images.py           # code to display user selected image, similar images and chatbot
  ├── fastapi
  │   └── repository.py               # application code for Fastapi
  ├── data
  │   ├── Pinecone_Embeddings.ipynb   # notebook to generate embeddings for images and add it to Pinecone Db
  │   └── imagesinfo.csv              # data csv
  ├── main.py                         # code for streamlit application (Sign up, Sign in, Logout)
  └── requirements.txt                # libraries required to build the application
```

## How to run it locally







