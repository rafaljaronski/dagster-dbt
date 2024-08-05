{{
    config(
        materialized = 'table',
        tags = ['src']
    )
}}
SELECT
  id AS host_id,
  name AS host_name,
  is_superhost,
  created_at,
  updated_at
FROM {{ source('bg', 'hosts') }}