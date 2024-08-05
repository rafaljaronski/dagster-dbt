{{
    config(
        materialized = 'table',
        tags = ['dim']
    )
}}
SELECT
  listing_id,
  review_date,
  reviewer_name,
  review_text,
  review_sentiment
FROM
  {{ ref("SRC_REVIEWS")}}