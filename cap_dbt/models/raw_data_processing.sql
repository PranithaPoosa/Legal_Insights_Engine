with raw_data_processing as (
    select * from {{source('raw','raw_data')}}
)

select
    cast(JSON_DATA : id as VARCHAR) as case_id,
    cast(JSON_DATA : name as VARCHAR) as case_name,
    cast(JSON_DATA : decision_date as VARCHAR) as decision_date,
    cast(JSON_DATA : court : name as VARCHAR) as court_name,
    cast(JSON_DATA : citations[0] : cite as VARCHAR) as citation,
    JSON_DATA : casebody : data : opinions as opinions,
    JSON_DATA : cites_to as cites_to
 from raw_data_processing