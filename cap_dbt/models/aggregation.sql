{{ config(materialized='table') }}

with aggregation as (
    select * from {{ref ('flatten')}}
)

select case_id, case_name, decision_date, court_name, citation, opinion_text, author, category, ARRAY_AGG(cites_to) as cites_to
from aggregation
group by case_id, case_name, decision_date, court_name, citation, opinion_text, author, category having category IS NOT NULL