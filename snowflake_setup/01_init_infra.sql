-- FICHIER : snowflake_setup/01_init_infra.sql

-- 1. Utiliser le rôle d'admin pour créer l'infra
USE ROLE ACCOUNTADMIN;

-- 2. Créer le Warehouse (le moteur de calcul)
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- 3. Créer la Database et le Schema
CREATE DATABASE IF NOT EXISTS INSURANCE_DB;
CREATE SCHEMA IF NOT EXISTS INSURANCE_DB.CLAIMS;
CREATE SCHEMA IF NOT EXISTS INSURANCE_DB.RAW;

-- 4. Donner les droits CORTEX (Indispensable pour ton projet)
-- Cela permet au rôle ACCOUNTADMIN (que tu utilises) d'appeler l'IA
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE ACCOUNTADMIN;

-- 2. Création de la table de réception des données brutes
CREATE OR REPLACE TABLE INSURANCE_DB.RAW.CONSTATS (
    metadata_filename VARCHAR,
    metadata_row_number INT,
    record_content VARIANT, -- Le JSON brut
    ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 3. Création du Stage interne
CREATE OR REPLACE STAGE INSURANCE_DB.RAW.SF_STAGE_CONSTATS
    FILE_FORMAT = (TYPE = 'JSON', STRIP_OUTER_ARRAY = TRUE);