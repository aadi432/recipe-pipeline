# scripts/1_setup_firestore.py
import firebase_admin
from firebase_admin import credentials, firestore
import json
import uuid
import random
import datetime
import re
import os

# CONFIG
SERVICE_ACCOUNT_PATH = r"C:\Users\DELL\Desktop\recipe-pipeline\serviceAccount.json"
PAV_SEED_PATH = r"C:\Users\DELL\Desktop\recipe-pipeline\seed_data.json"


cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

#HELPERS 
def slugify(text):
    t = text.lower()
    t = re.sub(r"[^a-z0-9]+", "_", t)
    return t.strip("_")

def random_difficulty():
    return random.choices(["easy", "medium", "hard"], weights=[0.5, 0.35, 0.15])[0]

def timestamp():
    return datetime.datetime.utcnow().isoformat()

def make_ingredients(main, pool, count=8):
    items = []
    main_qty = random.choice(["200g", "150g", "1 cup", "2 cups", "250g"])
    items.append({"name": main, "quantity": main_qty})

    extras = random.sample(pool, k=count - 1)
    qty_list = ["1 tsp", "2 tsp", "1 tbsp", "2 tbsp", "½ cup", "1 cup"]
    for e in extras:
        items.append({"name": e, "quantity": random.choice(qty_list)})

    return items

def make_steps(title, main, steps_n=7):
    base = [
        f"Wash, chop and prepare all ingredients needed for {title}.",
        "Heat oil or ghee in a heavy-bottom pan on medium flame until lightly aromatic.",
        "Add onions, ginger, garlic or green chillies and sauté until soft and golden.",
        f"Add {main} along with any supporting vegetables or masala bases and cook briefly.",
        "Add tomatoes and spice powders. Cook until the mixture thickens and becomes glossy.",
        "Add a little water to adjust consistency. Cover and simmer on low flame.",
        "Taste, adjust seasoning and cook for another minute for better flavor balance.",
        "Finish with coriander, butter or lemon juice and serve warm."
    ]
    return [{"order": i + 1, "text": base[i]} for i in range(steps_n)]


# INSERT PRIMARY PAV BHAJI 
with open(PAV_SEED_PATH, "r", encoding="utf-8") as f:
    pav = json.load(f)

pav["id"] = "pav_bhaji_001"
pav["difficulty"] = random_difficulty()
pav["cuisine"] = "Indian"
pav["region"] = "Maharashtra"
pav["calories"] = 420
pav["tags"] = ["vegetarian", "street-food"]
pav["created_at"] = timestamp()

db.collection("recipes").document(pav["id"]).set(pav)



#19 MORE VEGETARIAN RECIPES 
recipe_titles = [
    "Paneer Tikka Masala",
    "Kadai Paneer",
    "Palak Paneer",
    "Shahi Paneer",
    "Paneer Bhurji",
    "Veg Biryani",
    "Jeera Rice",
    "Aloo Gobi",
    "Chole Masala",
    "Rajma Masala",
    "Dal Tadka",
    "Dal Makhani",
    "Masala Dosa",
    "Vegetable Sambar",
    "Upma",
    "Poha",
    "Veg Manchurian",
    "Vegetable Fried Rice",
    "Bhindi Masala"
]

common_ing = [
    "onion", "tomato", "ginger", "garlic", "turmeric", "red chilli powder",
    "coriander powder", "garam masala", "cumin seeds", "mustard seeds",
    "green chilli", "oil", "butter", "peas", "carrot", "beans",
    "capsicum", "lemon", "coriander leaves"
]

recipe_ids = []

for idx, title in enumerate(recipe_titles, start=2):
    rid = f"{slugify(title)}_{idx:03d}"

    # Determine main ingredient
    first = slugify(title).split("_")[0]
    main_map = {
        "paneer": "paneer",
        "aloo": "potato",
        "veg": "mixed vegetables",
        "chole": "chickpeas",
        "rajma": "kidney beans",
        "dal": "lentils",
        "biryani": "basmati rice",
        "rice": "rice",
        "dosa": "rice batter",
        "sambar": "lentils",
        "poha": "flattened rice",
        "bhindi": "okra"
    }
    main_ing = main_map.get(first, "mixed vegetables")

    ing_count = random.choice([7, 8, 9])
    ingredients = make_ingredients(main_ing, common_ing, ing_count)

    steps = make_steps(title, main_ing, random.choice([6, 7, 8]))

    recipe = {
        "id": rid,
        "title": title,
        "description": f"{title} prepared in a simple vegetarian style with balanced spices.",
        "servings": random.choice([2,3,4]),
        "prep_time_minutes": random.randint(10, 25),
        "cook_time_minutes": random.randint(20, 45),
        "difficulty": random_difficulty(),
        "cuisine": random.choice(["North Indian", "South Indian", "Indo-Chinese"]),
        "region": random.choice(["North India", "South India", "West India"]),
        "calories": random.randint(250, 550),
        "tags": ["vegetarian", "home-style"],
        "ingredients": ingredients,
        "steps": steps,
        "created_at": timestamp()
    }

    db.collection("recipes").document(recipe["id"]).set(recipe)
    recipe_ids.append(recipe["id"])



# USERS 
user_names = [
    "Aarav Sharma", "Riya Singh", "Kunal Verma", "Sneha Gupta", "Rohan Mehta",
    "Ananya Pillai", "Kavya Patil", "Manav Jain", "Tanvi Desai", "Siddharth Rao"
]

users = []

for name in user_names:
    uid = "user_" + slugify(name)
    user = {"id": uid, "name": name}
    users.append(user)
    db.collection("users").document(uid).set(user)


#  INTERACTIONS
all_recipes = ["pav_bhaji_001"] + recipe_ids
interaction_types = ["view", "like", "cook_attempt"]

for _ in range(120):
    rec = random.choice(all_recipes)
    user = random.choice(users)["id"]
    itype = random.choices(interaction_types, weights=[0.7, 0.2, 0.1])[0]

    inter = {
        "id": str(uuid.uuid4()),
        "recipe_id": rec,
        "user_id": user,
        "type": itype,
        "timestamp": timestamp(),
        "rating": random.choice([None]*5 + [3,4,5])
    }

    db.collection("interactions").document(inter["id"]).set(inter)

# PRINT SAFE 
print("Recipes added.")
print("Users created.")
print("Interactions generated.")
print("Setup finished.")

