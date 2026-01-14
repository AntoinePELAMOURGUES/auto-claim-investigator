import snowflake.connector
import os
import sys
from dotenv import load_dotenv

# 2. CHARGEMENT DES VARIABLES (Cherche le .env à la racine)
load_dotenv()

# Configuration
FILE_PATH = os.path.join("..", "data", "raw_constats.json")
STAGE_NAME = "@INSURANCE_DB.RAW.SF_STAGE_CONSTATS"
TABLE_NAME = "INSURANCE_DB.RAW.CONSTATS"


def get_connection():
    """Établit la connexion sécurisée via variables d'environnement"""
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database="INSURANCE_DB",
        schema="RAW",
    )


def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Erreur : Le fichier {FILE_PATH} est introuvable.")
        sys.exit(1)

    print("🔌 Connexion à Snowflake...")
    try:
        conn = get_connection()
        cur = conn.cursor()

        # 1. Upload du fichier (PUT)
        # On utilise file:// pour indiquer un fichier local
        # auto_compress=True est activé par défaut (gain de bande passante)
        print(f"🚀 Upload de {FILE_PATH} vers le Stage...")
        put_query = (
            f"PUT file://{FILE_PATH} {STAGE_NAME} AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
        )
        cur.execute(put_query)

        # 2. Chargement en table (COPY INTO)
        print(f"📥 Ingestion du Stage vers la table {TABLE_NAME}...")
        copy_query = f"""
            COPY INTO {TABLE_NAME}
            (metadata_filename, metadata_row_number, record_content)
            FROM (
                SELECT
                    METADATA$FILENAME,
                    METADATA$FILE_ROW_NUMBER,
                    $1
                FROM {STAGE_NAME}
            )
        """
        cur.execute(copy_query)

        print("✅ Mission accomplie. Données ingérées.")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()
