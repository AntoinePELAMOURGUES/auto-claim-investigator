{{ config(
    materialized='table'
) }}

WITH analysis AS (
    SELECT * FROM {{ ref('fct_claims_analysis') }}
),

parsed_data AS (
    SELECT
        claim_id,
        accident_date,
        damage_amount,

        -- Extraction propre du verdict
        ai_assessment,

        -- 1. On extrait juste les chiffres (0, 50, 100) de la réponse IA
        -- On cherche la première suite de chiffres trouvée dans le texte
        TRY_TO_NUMBER(REGEXP_SUBSTR(ai_assessment, '\\d+')) AS responsibility_score,

        -- 2. Création de catégories business pour le reporting
        CASE
            WHEN TRY_TO_NUMBER(REGEXP_SUBSTR(ai_assessment, '\\d+')) = 100 THEN 'Responsable'
            WHEN TRY_TO_NUMBER(REGEXP_SUBSTR(ai_assessment, '\\d+')) = 50  THEN 'Partagé'
            WHEN TRY_TO_NUMBER(REGEXP_SUBSTR(ai_assessment, '\\d+')) = 0   THEN 'Non Responsable'
            ELSE 'Analyse Manuelle Requise' -- Si l'IA a répondu un truc bizarre
        END AS responsibility_category

    FROM analysis
)

SELECT * FROM parsed_data