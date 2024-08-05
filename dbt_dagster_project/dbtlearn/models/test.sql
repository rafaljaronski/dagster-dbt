WITH raw_data AS (
    SELECT
        1 AS id,
        'Test2' AS name
    UNION ALL
    SELECT
        2 AS id,
        'Test2' AS name
)

SELECT
    id,
    name
FROM
    raw_data