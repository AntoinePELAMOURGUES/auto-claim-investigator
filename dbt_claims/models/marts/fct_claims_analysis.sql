{{ config(
    materialized='table'
) }}

WITH source_data AS (
    SELECT * FROM {{ ref('stg_claims') }}
),

ai_analysis AS (
    SELECT
        claim_id,
        accident_date,
        damage_amount,
        accident_description,

        -- On concatène une consigne claire avec la description de l'accident.
        -- On utilise 'mistral-large' car il est excellent en Français.
        SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large',
            CONCAT(
                'Tu es un expert en assurance automobile. Analyse le constat amiable suivant. ',
                'Détermine la responsabilité du narrateur (celui qui dit "Je") en pourcentage (0, 50, ou 100). ',
                'Donne une raison courte. ',
                'Format de réponse STRICT : "RESPONSABILITE: [Pourcentage]% | RAISON: [Explication]" ',
                'Voici le récit : ',
                accident_description
            )
        ) AS ai_assessment

    FROM source_data
)

SELECT * FROM ai_analysis