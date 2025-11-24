import pandas as pd
import os
import logging
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
# RETRY CSV READ (in case file is locked or slow)
# =====================================================
@retry(Exception, tries=3, delay=1, backoff=2)
def safe_read_csv(path):
    return pd.read_csv(path)


# =====================================================
# MAIN TRANSFORMATION FUNCTION
# =====================================================
def transform_data():

    input_folder = "outputs"
    output_folder = "outputs/clean"
    os.makedirs(output_folder, exist_ok=True)
    logger.info("Clean output folder created.")

    # ---------------------------- READ FILES ----------------------------
    logger.info("Loading exported CSV files...")

    recipes = safe_read_csv(f"{input_folder}/recipe.csv")
    ingredients = safe_read_csv(f"{input_folder}/ingredients.csv")
    steps = safe_read_csv(f"{input_folder}/steps.csv")
    users = safe_read_csv(f"{input_folder}/users.csv")
    interactions = safe_read_csv(f"{input_folder}/interactions.csv")

    logger.info("All source CSV files successfully read.")

    # ---------------------------- CLEAN RECIPES ----------------------------
    logger.info("Cleaning recipes...")

    recipes["title"] = recipes["title"].astype(str).str.strip()
    recipes["difficulty"] = recipes["difficulty"].astype(str).str.lower()

    # Remove duplicates if any
    recipes = recipes.drop_duplicates(subset=["id"])

    recipes.to_csv(f"{output_folder}/recipes_clean.csv", index=False)
    logger.info("recipes_clean.csv created.")

    # ---------------------------- CLEAN INGREDIENTS ----------------------------
    logger.info("Cleaning ingredients...")

    ingredients["ingredient_name"] = ingredients["ingredient_name"].astype(str).str.strip()
    ingredients = ingredients.drop_duplicates()

    ingredients.to_csv(f"{output_folder}/ingredients_clean.csv", index=False)
    logger.info("ingredients_clean.csv created.")

    # ---------------------------- CLEAN STEPS ----------------------------
    logger.info("Cleaning steps...")

    steps = steps.drop_duplicates()

    steps["order"] = steps["order"].astype(int)

    steps = steps.sort_values(by=["recipe_id", "order"])

    steps.to_csv(f"{output_folder}/steps_clean.csv", index=False)
    logger.info("steps_clean.csv created.")

    # ---------------------------- CLEAN USERS ----------------------------
    logger.info("Cleaning users...")

    users = users.drop_duplicates()
    users["name"] = users["name"].astype(str).str.title()

    users.to_csv(f"{output_folder}/users_clean.csv", index=False)
    logger.info("users_clean.csv created.")

    # ---------------------------- CLEAN INTERACTIONS ----------------------------
    logger.info("Cleaning interactions...")

    interactions = interactions.drop_duplicates(subset=["id"])

    # Convert timestamp to datetime safely
    interactions["timestamp"] = pd.to_datetime(interactions["timestamp"], errors="coerce")

    interactions.to_csv(f"{output_folder}/interactions_clean.csv", index=False)
    logger.info("interactions_clean.csv created.")

    # ---------------------------- DONE ----------------------------
    logger.info("Transformation completed successfully!")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    try:
        transform_data()
    except Exception as e:
        logger.error("Transformation failed: %s", e)
        raise
