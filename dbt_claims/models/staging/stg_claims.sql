WITH source AS (
    -- On appelle la source déclarée juste avant
    SELECT * FROM {{ source('raw_layer', 'constats') }}
),

renamed AS (
    SELECT
        -- 1. Extraction des métadonnées techniques
        metadata_filename,
        ingested_at,

        -- 2. Extraction des champs métier depuis le JSON (record_content)
        -- On convertit le VARIANT (JSON) en types SQL standards
        record_content:claim_id::VARCHAR(50)            AS claim_id,
        record_content:accident_date::TIMESTAMP         AS accident_date,

        -- Extraction des conducteurs (Le tableau JSON est aplati ici de façon simple)
        record_content:drivers[0]:name::VARCHAR(100)    AS driver_a_name,
        record_content:drivers[1]:name::VARCHAR(100)    AS driver_b_name,

        -- Extraction de la localisation
        record_content:location:city::VARCHAR(100)      AS accident_city,

        -- LE CHAMP CLÉ POUR L'IA : La description
        record_content:constat_description::VARCHAR     AS accident_description,

        -- Le montant estimé
        record_content:estimated_damage_amount::FLOAT   AS damage_amount

    FROM source
)

SELECT * FROM renamed