import firebase_admin
from firebase_admin import credentials, firestore
import json
import uuid
import random
import datetime
import re
import os
import logging
from dotenv import load_dotenv
from utils_retry import retry   # RETRY DECORATOR

# =====================================================
# 1. LOGGING CONFIGURATION
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =====================================================
# 2. LOAD ENVIRONMENT VARIABLES
# =====================================================
load_dotenv()

SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
PAV_SEED_PATH = os.getenv("PAV_SEED_PATH")

if not SERVICE_ACCOUNT_PATH:
    raise ValueError("SERVICE_ACCOUNT_PATH not found in .env")

if not PAV_SEED_PATH:
    raise ValueError("PAV_SEED_PATH not found in .env")

# =====================================================
# 3. FIRESTORE INITIALIZATION WITH RETRY
# =====================================================
@retry(Exception, tries=5, delay=1, backoff=2)
def init_firestore():
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

try:
    db = init_firestore()
    logger.info("Connected to Firebase Firestore successfully!")
except Exception as e:
    logger.error("Failed to initialize Firestore: %s", e)
    raise


# =====================================================
# SAFE WRITE (RETRY FOR .set())
# =====================================================
@retry(Exception, tries=3, delay=1, backoff=2)
def safe_set(collection: str, doc_id: str, data: dict):
    db.collection(collection).document(doc_id).set(data)


# =====================================================
# HELPER FUNCTIONS
# =====================================================
def slugify(text):
    t = text.lower()
    t = re.sub(r"[^a-z0-9]+", "_", t)
    return t.strip("_")


def random_difficulty():
    return random.choices(["easy", "medium", "hard"],
                          weights=[0.5, 0.35, 0.15])[0]


def timestamp():
    return datetime.datetime.utcnow().isoformat()


def make_ingredients(main, pool, count=8):
    items = []

    # Main ingredient
    items.append({
        "name": main,
        "quantity": random.choice(["100g", "150g", "1 cup", "200g", "2 cups"])
    })

    # Extra ingredients
    extras = random.sample(pool, k=count - 1)
    qty_options = ["1 tsp", "2 tsp", "1 tbsp", "2 tbsp", "½ cup"]

    for e in extras:
        items.append({"name": e, "quantity": random.choice(qty_options)})

    return items


def make_steps(title, main, steps_n=8):
    base = [
        f"Wash all ingredients for {title}.",
        "Heat oil on medium flame.",
        "Add onions, ginger, garlic; sauté until golden.",
        f"Add {main} and other vegetables.",
        "Add spices and cook until masala thickens.",
        "Add water, cover and simmer for 10 minutes.",
        "Adjust salt and mix well.",
        "Serve hot with roti or rice."
    ]
    return [{"order": i+1, "text": base[i]} for i in range(steps_n)]


# =====================================================
# 5. INSERT MAIN PAV BHAJI RECIPE
# =====================================================
try:
    logger.info("Loading Pav Bhaji seed data...")
    with open(PAV_SEED_PATH, "r", encoding="utf-8") as f:
        pav = json.load(f)

    pav["id"] = "pav_bhaji_001"
    pav["difficulty"] = random_difficulty()
    pav["cuisine"] = "Indian"
    pav["region"] = "Maharashtra"
    pav["created_at"] = timestamp()

    safe_set("recipes", pav["id"], pav)
    logger.info("Inserted main recipe: Pav Bhaji")

except Exception as e:
    logger.error("Failed to insert Pav Bhaji: %s", e)
    raise


# =====================================================
# 6. INSERT 19 OTHER RECIPES (ONE-BY-ONE WITH RETRY)
# =====================================================
recipe_titles = [
    "Paneer Tikka Masala", "Kadai Paneer", "Palak Paneer", "Shahi Paneer",
    "Paneer Bhurji", "Veg Biryani", "Jeera Rice", "Aloo Gobi", "Chole Masala",
    "Rajma Masala", "Dal Tadka", "Dal Makhani", "Masala Dosa",
    "Vegetable Sambar", "Upma", "Poha", "Veg Manchurian",
    "Vegetable Fried Rice", "Bhindi Masala"
]

common_ing = [
    "onion", "tomato", "ginger", "garlic", "turmeric",
    "red chilli powder", "coriander powder", "garam masala",
    "oil", "butter", "peas", "carrot", "beans", "capsicum"
]

logger.info("Generating vegetarian recipes...")

try:
    for idx, title in enumerate(recipe_titles, start=2):
        rid = f"{slugify(title)}_{idx:03d}"

        first = slugify(title).split("_")[0]
        main_map = {
            "paneer": "paneer",
            "aloo": "potato",
            "veg": "mixed vegetables",
            "chole": "chickpeas",
            "rajma": "kidney beans",
            "dal": "lentils",
            "rice": "rice",
            "poha": "flattened rice",
            "bhindi": "okra",
            "dosa": "rice batter",
            "sambar": "lentils"
        }
        main_ing = main_map.get(first, "mixed vegetables")

        ingredients = make_ingredients(main_ing, common_ing, random.randint(7, 9))
        steps = make_steps(title, main_ing, random.randint(6, 8))

        recipe = {
            "id": rid,
            "title": title,
            "description": f"{title} prepared in a simple home-style method.",
            "servings": random.choice([2, 3, 4]),
            "prep_time_minutes": random.randint(10, 25),
            "cook_time_minutes": random.randint(15, 40),
            "difficulty": random_difficulty(),
            "cuisine": random.choice(["North Indian", "South Indian", "Indo-Chinese"]),
            "region": random.choice(["North India", "West India", "South India"]),
            "calories": random.randint(250, 550),
            "tags": ["vegetarian"],
            "ingredients": ingredients,
            "steps": steps,
            "created_at": timestamp()
        }

        safe_set("recipes", rid, recipe)

    logger.info("All vegetarian recipes inserted successfully!")

except Exception as e:
    logger.error("Failed to insert veg recipes: %s", e)
    raise


# =====================================================
# 7. INSERT USERS
# =====================================================
user_names = [
    "Aarav Sharma", "Riya Singh", "Kunal Verma", "Sneha Gupta", "Rohan Mehta",
    "Ananya Pillai", "Kavya Patil", "Manav Jain", "Tanvi Desai", "Siddharth Rao"
]

logger.info("Inserting users...")

try:
    for name in user_names:
        uid = "user_" + slugify(name)
        user = {"id": uid, "name": name}
        safe_set("users", uid, user)

    logger.info("Users inserted successfully!")

except Exception as e:
    logger.error("Failed to insert users: %s", e)
    raise


# =====================================================
# 8. INSERT INTERACTIONS
# =====================================================
logger.info("Generating interactions...")

try:
    all_recipes = ["pav_bhaji_001"] + [
        f"{slugify(title)}_{idx:03d}" for idx, title in enumerate(recipe_titles, start=2)
    ]
    interaction_types = ["view", "like", "cook_attempt"]

    for _ in range(120):
        rec = random.choice(all_recipes)
        user = random.choice(user_names)
        user_id = "user_" + slugify(user)

        itype = random.choices(interaction_types, weights=[0.7, 0.2, 0.1])[0]

        inter = {
            "id": str(uuid.uuid4()),
            "recipe_id": rec,
            "user_id": user_id,
            "type": itype,
            "timestamp": timestamp(),
            "rating": random.choice([None]*6 + [3, 4, 5])
        }

        safe_set("interactions", inter["id"], inter)

    logger.info("Interactions inserted successfully!")

except Exception as e:
    logger.error("Failed to insert interactions: %s", e)
    raise

# =====================================================
# DONE
# =====================================================
logger.info("Setup script completed successfully!")
