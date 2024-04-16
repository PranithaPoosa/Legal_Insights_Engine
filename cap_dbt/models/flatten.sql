with flatten as (
    select case_id, case_name, citation, decision_date, court_name, f.value as flattened_opinion, c.value as flattened_cites_to_case_id   from {{ref('raw_data_processing')}} a, LATERAL FLATTEN(input => a.opinions) f, LATERAL FLATTEN(input => a.cites_to) c
)

select *,
    cast(flattened_opinion:text as varchar) as opinion_text,
    cast(flattened_opinion:author as varchar) as author,
    cast(flattened_opinion:category as varchar) as category,
    flattened_cites_to_case_id::STRING as cites_to
from flatten where flattened_opinion:type = 'majority'