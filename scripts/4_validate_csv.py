# scripts/4_validate_csv.py
import pandas as pd
import json
import os

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Load CSV files
recipes = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\recipe.csv")
ingredients = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\ingredients.csv")
interactions = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\interactions.csv")
steps = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\steps.csv")
users = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\users.csv")

# Prepare validation report structure
report = {
    "recipes": [],
    "ingredients": [],
    "interactions": [],
    "users": [],
    "steps": []       # NEW SECTION ADDED
}

# Helper function to validate required fields
def check_required(row, fields):
    errors = []
    for f in fields:
        if pd.isna(row.get(f)) or row.get(f) == "":
            errors.append(f"Missing {f}")
    return errors



# VALIDATE RECIPES

for _, r in recipes.iterrows():
    errs = []

    errs += check_required(r, [
        "id", "title", "prep_time_minutes",
        "cook_time_minutes", "difficulty"
    ])

    if not pd.isna(r["prep_time_minutes"]) and r["prep_time_minutes"] < 0:
        errs.append("prep_time negative")

    if not pd.isna(r["cook_time_minutes"]) and r["cook_time_minutes"] < 0:
        errs.append("cook_time negative")

    if r.get("difficulty") not in ["easy", "medium", "hard"]:
        errs.append("invalid difficulty")

    if pd.isna(r.get("tags")) or r.get("tags") == "":
        errs.append("missing tags")

    report["recipes"].append({
        "id": r["id"],
        "valid": len(errs) == 0,
        "errors": errs
    })



# VALIDATE INGREDIENTS

for _, ing in ingredients.iterrows():
    errs = check_required(ing, ["recipe_id", "ingredient_name"])

    report["ingredients"].append({
        "recipe_id": ing.get("recipe_id"),
        "ingredient": ing.get("ingredient_name"),
        "valid": len(errs) == 0,
        "errors": errs
    })



# VALIDATE INTERACTIONS

for _, it in interactions.iterrows():
    errs = []

    errs += check_required(it, ["id", "recipe_id", "user_id", "type"])

    if it.get("type") not in ["view", "like", "cook_attempt"]:
        errs.append("invalid type")

    if not pd.isna(it.get("rating")):
        try:
            r_value = float(it["rating"])
            if r_value < 1 or r_value > 5:
                errs.append("rating out of range")
        except:
            errs.append("rating not numeric")

    report["interactions"].append({
        "id": it.get("id"),
        "valid": len(errs) == 0,
        "errors": errs
    })



# VALIDATE USERS

for _, u in users.iterrows():
    errs = check_required(u, ["id", "name"])

    report["users"].append({
        "id": u.get("id"),
        "valid": len(errs) == 0,
        "errors": errs
    })



# VALIDATE EACH STEP (NEW)

for _, st in steps.iterrows():
    errs = []

    errs += check_required(st, ["recipe_id", "step_order", "step_text"])

    # step_order must be positive
    try:
        if int(st["step_order"]) <= 0:
            errs.append("step_order must be positive")
    except:
        errs.append("step_order not a number")

    report["steps"].append({
        "recipe_id": st.get("recipe_id"),
        "step_order": st.get("step_order"),
        "valid": len(errs) == 0,
        "errors": errs
    })



# VALIDATE STEP ORDER SEQUENCE (advanced)

grouped = steps.sort_values(
    ["recipe_id", "step_order"]
).groupby("recipe_id")

for recipe_id, group in grouped:
    expected = list(range(1, len(group) + 1))
    actual = list(group["step_order"])

    if expected != actual:
        report["recipes"].append({
            "id": recipe_id,
            "valid": False,
            "errors": [f"Step order incorrect. Expected {expected}, got {actual}"]
        })


# SAVE VALIDATION REPORT

with open("outputs/validation_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Validation complete! See outputs/validation_report.json")
