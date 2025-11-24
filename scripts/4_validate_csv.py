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
# SAFE CSV READ WITH RETRY
# =====================================================
@retry(Exception, tries=3, delay=1, backoff=2)
def safe_read_csv(path):
    return pd.read_csv(path)


# =====================================================
# VALIDATION FUNCTION
# =====================================================
def validate_csv_files():

    input_folder = "outputs"
    output_folder = "outputs/validated"
    os.makedirs(output_folder, exist_ok=True)
    logger.info("Validation folder created.")

    # ---------------------------- LOAD CSV FILES ----------------------------
    logger.info("Reading CSV files for validation...")

    recipes = safe_read_csv(f"{input_folder}/recipe.csv")
    ingredients = safe_read_csv(f"{input_folder}/ingredients.csv")
    steps = safe_read_csv(f"{input_folder}/steps.csv")
    users = safe_read_csv(f"{input_folder}/users.csv")
    interactions = safe_read_csv(f"{input_folder}/interactions.csv")

    logger.info("All CSV files loaded successfully.")

    validation_report = []

    # =====================================================
    # 1. Recipe Validation
    # =====================================================
    logger.info("Validating recipes...")
    if recipes["id"].isnull().any():
        validation_report.append("❌ Recipes: Missing recipe IDs")
    else:
        validation_report.append("✔ Recipes: All IDs present")

    if recipes.duplicated(subset=["id"]).any():
        validation_report.append("❌ Recipes: Duplicate recipe IDs found")
    else:
        validation_report.append("✔ Recipes: No duplicate IDs")

    # =====================================================
    # 2. Ingredient Validation
    # =====================================================
    logger.info("Validating ingredients...")

    if ingredients["recipe_id"].isnull().any():
        validation_report.append("❌ Ingredients: Missing recipe_id")
    else:
        validation_report.append("✔ Ingredients: recipe_id OK")

    if ingredients.duplicated().any():
        validation_report.append("❌ Ingredients: Duplicate ingredient rows found")
    else:
        validation_report.append("✔ Ingredients: No duplicate rows")

    # =====================================================
    # 3. Step Validation
    # =====================================================
    logger.info("Validating steps...")

    if steps["recipe_id"].isnull().any():
        validation_report.append("❌ Steps: Missing recipe_id")
    else:
        validation_report.append("✔ Steps: recipe_id OK")

    if steps["order"].isnull().any():
        validation_report.append("❌ Steps: Missing step order")
    else:
        validation_report.append("✔ Steps: step order OK")

    # check if order numbers are valid integers
    if not pd.api.types.is_integer_dtype(steps["order"]):
        validation_report.append("❌ Steps: 'order' column not integer")
    else:
        validation_report.append("✔ Steps: order column valid")

    # =====================================================
    # 4. User Validation
    # =====================================================
    logger.info("Validating users...")

    if users["id"].isnull().any():
        validation_report.append("❌ Users: Missing user ID")
    else:
        validation_report.append("✔ Users: All user IDs present")

    if users.duplicated(subset=["id"]).any():
        validation_report.append("❌ Users: Duplicate user IDs")
    else:
        validation_report.append("✔ Users: No duplicate user IDs")

    # =====================================================
    # 5. Interactions Validation
    # =====================================================
    logger.info("Validating interactions...")

    if interactions["id"].isnull().any():
        validation_report.append("❌ Interactions: Missing ID")
    else:
        validation_report.append("✔ Interactions: IDs OK")

    if interactions.duplicated(subset=["id"]).any():
        validation_report.append("❌ Interactions: Duplicate interaction IDs")
    else:
        validation_report.append("✔ Interactions: No duplicate interaction IDs")

    if interactions["recipe_id"].isin(recipes["id"]).all():
        validation_report.append("✔ Interactions: All recipe_id match recipes table")
    else:
        validation_report.append("❌ Interactions: Some recipe_id do NOT exist in recipes table")

    if interactions["user_id"].isin(users["id"]).all():
        validation_report.append("✔ Interactions: All user_id match users table")
    else:
        validation_report.append("❌ Interactions: Some user_id do NOT exist in users table")

    # =====================================================
    # SAVE REPORT
    # =====================================================
    report_path = f"{output_folder}/validation_report.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=== DATA VALIDATION REPORT ===\n\n")
        for line in validation_report:
            f.write(line + "\n")


    logger.info("Validation completed successfully!")
    logger.info(f"Report saved to {report_path}")


# =====================================================
# MAIN EXECUTION
# =====================================================
if __name__ == "__main__":
    try:
        validate_csv_files()
    except Exception as e:
        logger.error("Validation failed: %s", e)
        raise
