{{
    config(
        materialized = 'table',
        tags = ['dim']
    )
}}
SELECT
  host_id,
  IFNULL(host_name, 'Anonymous') AS host_name,
  is_superhost,
  created_at,
  updated_at
FROM
  {{ ref("SRC_HOSTS")}}