import json
import random
import os
from faker import Faker
from datetime import datetime, timedelta

# On initialise le générateur de fausses données en Français
fake = Faker("fr_FR")

# Configuration
OUTPUT_DIR = "./data"
OUTPUT_FILE = "raw_constats.json"
NUM_RECORDS = 100


def generate_accident_narrative(driver_a, driver_b, case_type):
    """
    Génère un récit d'accident (le 'constat') basé sur un scénario type.
    C'est ici que Cortex devra travailler plus tard.
    """
    scenarios = {
        "rear_end": [
            f"Je, {driver_a}, étais à l'arrêt au feu rouge quand le véhicule B m'a percuté par l'arrière.",
            f"Le conducteur {driver_b} n'a pas freiné à temps et a heurté mon pare-chocs arrière alors que je ralentissais.",
            "Choc arrière. Je respectais les distances de sécurité mais j'ai été poussé.",
        ],
        "refusal_priority": [
            f"Le véhicule {driver_b} est sorti d'un stop sans regarder et m'a coupé la route.",
            f"Je circulais sur la voie principale, {driver_b} a grillé la priorité à droite.",
            "Refus de priorité évident du véhicule adverse venant de ma gauche.",
        ],
        "parking": [
            f"J'étais stationné correctement sur une place de parking, {driver_b} a reculé dans ma portière.",
            "En sortant de mon stationnement, j'ai accroché le véhicule B qui arrivait vite.",
            f"Le véhicule {driver_b} a ouvert sa portière sans regarder au moment où je passais.",
        ],
    }

    # Choix aléatoire d'une phrase type pour le scénario donné
    base_narrative = random.choice(scenarios[case_type])
    return base_narrative


def generate_claim():
    """Génère un constat amiable unique au format dictionnaire."""

    # Scénario aléatoire
    case_type = random.choice(["rear_end", "refusal_priority", "parking"])

    driver_a_name = fake.name()
    driver_b_name = fake.name()

    claim = {
        "claim_id": fake.uuid4(),
        "accident_date": fake.date_time_between(
            start_date="-1y", end_date="now"
        ).isoformat(),
        "location": {
            "city": fake.city(),
            "zipcode": fake.postcode(),
            "street": fake.street_address(),
        },
        "drivers": [
            {
                "id": "A",
                "name": driver_a_name,
                "license_plate": fake.license_plate(),
                "insurance_company": random.choice(["AXA", "Allianz", "GMF", "Matmut"]),
            },
            {
                "id": "B",
                "name": driver_b_name,
                "license_plate": fake.license_plate(),
                "insurance_company": random.choice(
                    ["Direct Assurance", "MAIF", "Generali"]
                ),
            },
        ],
        "vehicle_type": random.choice(["Berline", "SUV", "Utilitaire", "Moto"]),
        # LE CHAMP CRITIQUE POUR L'IA :
        "constat_description": generate_accident_narrative(
            driver_a_name, driver_b_name, case_type
        ),
        "estimated_damage_amount": round(random.uniform(500.0, 15000.0), 2),
    }
    return claim


def main():
    # Vérification dossier data
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Dossier créé : {OUTPUT_DIR}")

    print(f"🕵️  Génération de {NUM_RECORDS} constats en cours...")

    claims_list = [generate_claim() for _ in range(NUM_RECORDS)]

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as f:
        # On écrit du JSON compatible Snowflake (NDJSON ou liste d'objets)
        # Ici on fait une liste d'objets JSON standard
        json.dump(claims_list, f, indent=4, ensure_ascii=False)

    print(f"✅ Preuves déposées dans : {output_path}")
    print("   -> Prêt pour l'ingestion Snowflake.")


if __name__ == "__main__":
    main()
