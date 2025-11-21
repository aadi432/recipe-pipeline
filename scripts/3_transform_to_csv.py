# scripts/3_transform_to_csv.py
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os

# Initialize Firebase only once
cred = credentials.Certificate(r"C:\Users\DELL\Desktop\recipe-pipeline\serviceAccount.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Create output folder
os.makedirs("outputs", exist_ok=True)


# Extract RECIPES

recipes_docs = db.collection("recipes").stream()
recipes = []
ingredients_rows = []
steps_rows = []

for doc in recipes_docs:
    r = doc.to_dict()

    recipes.append({
        "id": r.get("id"),
        "title": r.get("title"),
        "description": r.get("description"),
        "servings": r.get("servings"),
        "prep_time_minutes": r.get("prep_time_minutes"),
        "cook_time_minutes": r.get("cook_time_minutes"),
        "difficulty": r.get("difficulty"),
        "tags": "|".join(r.get("tags", [])),
        "created_at": r.get("created_at")
    })

    for ing in r.get("ingredients", []):
        ingredients_rows.append({
            "recipe_id": r.get("id"),
            "ingredient_name": ing.get("name"),
            "ingredient_quantity": ing.get("quantity")
        })

    for st in r.get("steps", []):
        steps_rows.append({
            "recipe_id": r.get("id"),
            "step_order": st.get("order"),
            "step_text": st.get("text")
        })


# Extract INTERACTIONS

inter_docs = db.collection("interactions").stream()
interactions = []
for d in inter_docs:
    v = d.to_dict()
    interactions.append({
        "id": v.get("id"),
        "recipe_id": v.get("recipe_id"),
        "user_id": v.get("user_id"),
        "type": v.get("type"),
        "timestamp": v.get("timestamp"),
        "rating": v.get("rating")
    })


# OPTIONAL: Extract USERS

user_docs = db.collection("users").stream()
users_rows = []
for u in user_docs:
    data = u.to_dict()
    users_rows.append({
        "id": data.get("id"),
        "name": data.get("name")
    })


# SAVE CSV FILES

pd.DataFrame(recipes).to_csv("outputs/recipe.csv", index=False)
pd.DataFrame(ingredients_rows).to_csv("outputs/ingredients.csv", index=False)
pd.DataFrame(steps_rows).to_csv("outputs/steps.csv", index=False)
pd.DataFrame(interactions).to_csv("outputs/interactions.csv", index=False)
pd.DataFrame(users_rows).to_csv("outputs/users.csv", index=False)

print("CSV files created in outputs/: recipe.csv, ingredients.csv, steps.csv, interactions.csv, users.csv")