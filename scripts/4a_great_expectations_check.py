import os
import logging
import pandas as pd
from utils_retry import retry

# =====================================================
# LOGGING
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_PATH = os.path.join("outputs", "clean")
REPORT_PATH = os.path.join("outputs", "validated", "custom_ge_report.txt")


# =====================================================
# SAFE CSV READ WITH RETRY
# =====================================================
@retry(Exception, tries=3, delay=1, backoff=2)
def safe_read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# =====================================================
# EXPECTATION HELPERS (GE-STYLE)
# =====================================================
def expect_column_to_exist(df, column, table_name):
    success = column in df.columns
    return {
        "table": table_name,
        "check": f"Column exists: {column}",
        "success": success,
        "details": "" if success else f"Missing column '{column}'"
    }


def expect_column_values_not_null(df, column, table_name):
    if column not in df.columns:
        return {
            "table": table_name,
            "check": f"Not null: {column}",
            "success": False,
            "details": f"Column '{column}' does not exist"
        }
    success = not df[column].isnull().any()
    return {
        "table": table_name,
        "check": f"No NULL values in '{column}'",
        "success": success,
        "details": "" if success else f"Found NULL values in '{column}'"
    }


def expect_column_values_unique(df, column, table_name):
    if column not in df.columns:
        return {
            "table": table_name,
            "check": f"Unique values: {column}",
            "success": False,
            "details": f"Column '{column}' does not exist"
        }
    success = not df[column].duplicated().any()
    return {
        "table": table_name,
        "check": f"Unique values in '{column}'",
        "success": success,
        "details": "" if success else f"Duplicates found in '{column}'"
    }


def expect_column_type_integer(df, column, table_name):
    if column not in df.columns:
        return {
            "table": table_name,
            "check": f"Integer type: {column}",
            "success": False,
            "details": f"Column '{column}' does not exist"
        }
    # try to convert to integer type
    try:
        pd.to_numeric(df[column].dropna(), downcast="integer")
        success = True
        details = ""
    except Exception as e:
        success = False
        details = f"Values in '{column}' not all numeric: {e}"
    return {
        "table": table_name,
        "check": f"Integer-like values in '{column}'",
        "success": success,
        "details": details
    }


def expect_foreign_key_match(df_child, child_col, df_parent, parent_col, table_name):
    if child_col not in df_child.columns:
        return {
            "table": table_name,
            "check": f"Foreign key '{child_col}' -> '{parent_col}'",
            "success": False,
            "details": f"Child column '{child_col}' does not exist"
        }
    if parent_col not in df_parent.columns:
        return {
            "table": table_name,
            "check": f"Foreign key '{child_col}' -> '{parent_col}'",
            "success": False,
            "details": f"Parent column '{parent_col}' does not exist"
        }

    missing = ~df_child[child_col].isin(df_parent[parent_col])
    success = not missing.any()
    if success:
        details = ""
    else:
        bad_count = missing.sum()
        details = f"{bad_count} values in '{child_col}' not found in parent '{parent_col}'"
    return {
        "table": table_name,
        "check": f"Foreign key '{child_col}' matches '{parent_col}'",
        "success": success,
        "details": details
    }


# =====================================================
# MAIN VALIDATION FUNCTION
# =====================================================
def run_custom_expectations():
    os.makedirs(os.path.join("outputs", "validated"), exist_ok=True)
    logger.info("Starting custom GE-style validation...")

    results = []

    # -------------------------------------------------
    # Load all cleaned CSVs
    # -------------------------------------------------
    recipes = safe_read_csv(os.path.join(BASE_PATH, "recipes_clean.csv"))
    ingredients = safe_read_csv(os.path.join(BASE_PATH, "ingredients_clean.csv"))
    steps = safe_read_csv(os.path.join(BASE_PATH, "steps_clean.csv"))
    users = safe_read_csv(os.path.join(BASE_PATH, "users_clean.csv"))
    interactions = safe_read_csv(os.path.join(BASE_PATH, "interactions_clean.csv"))

    # =================================================
    # RECIPES CHECKS
    # =================================================
    table = "RECIPES_CLEAN"
    logger.info("Validating %s...", table)

    results.append(expect_column_to_exist(recipes, "id", table))
    results.append(expect_column_to_exist(recipes, "title", table))
    results.append(expect_column_values_not_null(recipes, "id", table))
    results.append(expect_column_values_unique(recipes, "id", table))
    results.append(expect_column_type_integer(recipes, "prep_time_minutes", table))
    results.append(expect_column_type_integer(recipes, "cook_time_minutes", table))

    # =================================================
    # INGREDIENTS CHECKS
    # =================================================
    table = "INGREDIENTS_CLEAN"
    logger.info("Validating %s...", table)

    results.append(expect_column_to_exist(ingredients, "recipe_id", table))
    results.append(expect_column_to_exist(ingredients, "ingredient_name", table))
    results.append(expect_column_values_not_null(ingredients, "recipe_id", table))

    # FK: ingredients.recipe_id -> recipes.id
    results.append(
        expect_foreign_key_match(
            ingredients, "recipe_id", recipes, "id", table
        )
    )

    # =================================================
    # STEPS CHECKS
    # =================================================
    table = "STEPS_CLEAN"
    logger.info("Validating %s...", table)

    results.append(expect_column_to_exist(steps, "recipe_id", table))
    results.append(expect_column_to_exist(steps, "order", table))
    results.append(expect_column_values_not_null(steps, "recipe_id", table))
    results.append(expect_column_values_not_null(steps, "order", table))
    results.append(expect_column_type_integer(steps, "order", table))

    # FK: steps.recipe_id -> recipes.id
    results.append(
        expect_foreign_key_match(
            steps, "recipe_id", recipes, "id", table
        )
    )

    # =================================================
    # USERS CHECKS
    # =================================================
    table = "USERS_CLEAN"
    logger.info("Validating %s...", table)

    results.append(expect_column_to_exist(users, "id", table))
    results.append(expect_column_values_not_null(users, "id", table))
    results.append(expect_column_values_unique(users, "id", table))

    # =================================================
    # INTERACTIONS CHECKS
    # =================================================
    table = "INTERACTIONS_CLEAN"
    logger.info("Validating %s...", table)

    results.append(expect_column_to_exist(interactions, "id", table))
    results.append(expect_column_values_not_null(interactions, "id", table))
    results.append(expect_column_values_unique(interactions, "id", table))

    results.append(expect_column_to_exist(interactions, "recipe_id", table))
    results.append(expect_column_to_exist(interactions, "user_id", table))

    # FK: interactions.recipe_id -> recipes.id
    results.append(
        expect_foreign_key_match(
            interactions, "recipe_id", recipes, "id", table
        )
    )
    # FK: interactions.user_id -> users.id
    results.append(
        expect_foreign_key_match(
            interactions, "user_id", users, "id", table
        )
    )

    # =================================================
    # WRITE TEXT REPORT
    # =================================================
    logger.info("Writing custom GE-style report to %s", REPORT_PATH)

    # group results by table for nicer formatting
    by_table = {}
    for r in results:
        by_table.setdefault(r["table"], []).append(r)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("=== CUSTOM DATA QUALITY REPORT (GE-STYLE) ===\n\n")
        overall_pass = True

        for table_name, checks in by_table.items():
            f.write("===========================================\n")
            f.write(f"{table_name}\n")
            f.write("===========================================\n")
            for c in checks:
                mark = "PASS" if c["success"] else "FAIL"
                if not c["success"]:
                    overall_pass = False
                f.write(f"{mark} - {c['check']}\n")
                if c["details"]:
                    f.write(f"       Details: {c['details']}\n")
            f.write("\n")

        f.write("===========================================\n")
        f.write("OVERALL STATUS\n")
        f.write("===========================================\n")
        if overall_pass:
            f.write("ALL CHECKS PASSED ✅\n")
        else:
            f.write("SOME CHECKS FAILED ❌ - see details above.\n")

    logger.info("Custom GE-style validation complete!")
    logger.info("Report saved to %s", REPORT_PATH)


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    try:
        run_custom_expectations()
    except Exception as e:
        logger.error("Custom expectations validation failed: %s", e)
        raise
