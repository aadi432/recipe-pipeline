import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import logging
import os
from dotenv import load_dotenv
from utils_retry import retry

# =====================================================
# LOGGING
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================
load_dotenv()

SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")

if not SERVICE_ACCOUNT_PATH:
    raise ValueError("SERVICE_ACCOUNT_PATH missing in .env")


# =====================================================
# FIRESTORE INIT WITH RETRY
# =====================================================
@retry(Exception, tries=5, delay=1, backoff=2)
def init_firestore():
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()


try:
    db = init_firestore()
    logger.info("Connected to Firestore.")
except Exception as e:
    logger.error("Failed to connect: %s", e)
    raise


# =====================================================
# SAFE GET WITH RETRY
# =====================================================
@retry(Exception, tries=3, delay=1, backoff=2)
def safe_get(collection_name):
    return db.collection(collection_name).stream()


# =====================================================
# EXPORT FUNCTION
# =====================================================
def export_firestore():
    os.makedirs("outputs", exist_ok=True)
    logger.info("Output folder ready.")

    # ---------------------------- RECIPES ----------------------------
    logger.info("Fetching RECIPES...")
    recipe_docs = safe_get("recipes")

    recipes_list = []
    ingredients_list = []
    steps_list = []

    for doc in recipe_docs:
        data = doc.to_dict()
        recipes_list.append(data)

        recipe_id = data.get("id")

        # ---------------- EXTRACT INGREDIENTS ----------------
        ing = data.get("ingredients", [])
        for item in ing:
            ingredients_list.append({
                "recipe_id": recipe_id,
                "ingredient_name": item.get("name"),
                "quantity": item.get("quantity")
            })

        # ---------------- EXTRACT STEPS ----------------
        step_data = data.get("steps", [])
        for step in step_data:
            steps_list.append({
                "recipe_id": recipe_id,
                "order": step.get("order"),
                "step_text": step.get("text")
            })

    # Save recipes
    recipes_df = pd.DataFrame(recipes_list)
    recipes_df.to_csv("outputs/recipe.csv", index=False)
    logger.info("recipes.csv exported.")

    # Save ingredients
    ingredients_df = pd.DataFrame(ingredients_list)
    ingredients_df.to_csv("outputs/ingredients.csv", index=False)
    logger.info("ingredients.csv exported.")

    # Save steps
    steps_df = pd.DataFrame(steps_list)
    steps_df.to_csv("outputs/steps.csv", index=False)
    logger.info("steps.csv exported.")

    # ---------------------------- USERS ----------------------------
    logger.info("Fetching USERS...")
    user_docs = safe_get("users")
    users_list = [doc.to_dict() for doc in user_docs]

    pd.DataFrame(users_list).to_csv("outputs/users.csv", index=False)
    logger.info("users.csv exported.")

    # ---------------------------- INTERACTIONS ----------------------------
    logger.info("Fetching INTERACTIONS...")
    inter_docs = safe_get("interactions")
    inter_list = [doc.to_dict() for doc in inter_docs]

    pd.DataFrame(inter_list).to_csv("outputs/interactions.csv", index=False)
    logger.info("interactions.csv exported.")

    logger.info("All collections exported successfully!")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    try:
        export_firestore()
        logger.info("Export script completed successfully!")
    except Exception as e:
        logger.error("Export failed: %s", e)
        raise
