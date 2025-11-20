# recipe-pipeline

# 📘 Recipe Analytics Pipeline
This project implements a complete **end-to-end Data Engineering Pipeline** using **Firebase Firestore** as the source system and **Python** for ETL, transformation, validation, and analytical reporting.  
It combines **technical depth (Option C)** with **professional formatting (Option A)** and **clarity for beginners (Option D)**.


# 📑 Table of Contents
1. Overview  
2. Architecture Diagram  
3. Data Model  
4. Firestore Source System  
5. ETL Pipeline  
6. Validation Rules  
7. Analytics & Insights  
8. Folder Structure  
9. How to Run  
10. Limitations  
11. Conclusion  


# 1️⃣ Project Overview

This project simulates a production-ready recipe platform.  
The pipeline automatically generates structured data into Firestore, exports it, transforms it into normalized tables, validates the dataset, and then performs analysis to extract insights.

**Primary Recipe:** Pav Bhaji  
**Total Recipes:** 20 (1 real + 19 synthetically generated vegetarian recipes)  
**Additional Collections:** users, interactions  

This project demonstrates:

- Data modeling  
- ETL/ELT workflows  
- Realistic synthetic dataset creation  
- Data validation strategies  
- Analytical reporting  
- Visualization generation  


# 2️⃣ Architecture Diagram 

```
                ┌───────────────────────────┐
                │   1. Generate Firestore    │
                │     (Recipes + Users +     │
                │      Interactions)         │
                └──────────────┬────────────┘
                               │
                               ▼
                ┌───────────────────────────┐
                │   2. Export Firestore      │
                │      Collections (JSON)    │
                └──────────────┬────────────┘
                               │
                               ▼
                ┌───────────────────────────┐
                │   3. Transform JSON → CSV │
                │      (Normalized Tables)   │
                └──────────────┬────────────┘
                               │
                               ▼
                ┌───────────────────────────┐
                │   4. Data Validation       │
                │    (Required fields,       │
                │     consistency, steps)    │
                └──────────────┬────────────┘
                               │
                               ▼
                ┌───────────────────────────┐
                │   5. Analytics + Charts    │
                │    (Insights Summary)      │
                └───────────────────────────┘
```


# 3️⃣ Data Model 

## 📌 Recipes Collection (Core Dataset)
| Field             | Type   | Description                         |
|-------------------|--------|-------------------------------------|
| id                | string | Unique recipe ID                    |
| title             | string | Name of dish                        |
| description       | string | Short explanation                   |
| servings          | number | Servings count                      |
| prep_time_minutes | number | Prep duration                       | 
| cook_time_minutes | number | Cook duration                       |
| difficulty        | string | easy / medium / hard                |
| cuisine           | string | e.g., Indian, South Indian          |
| region            | string | Where the recipe originates         |
| calories          | number | Approx nutritional value            |
| tags              | array  | Labels e.g. vegetarian              |
| ingredients       | array  | List of ingredient objects          |
| steps             | array  | List of cooking instruction objects |
| created_at        | string | ISO timestamp                       |


## 👥 Users Collection
Simple user profile with:
- id  
- name  


## 👍 Interactions Collection
Represents user behavior.

| Field     | Description                |
|-----------|----------------------------|
| id        | Unique log entry           |
| recipe_id | Linked recipe              |
| user_id   | Linked user                |
| type      | view / like / cook_attempt |
| timestamp | ISO format                 |
| rating    | optional (1–5)             |

This dataset allows trend analysis and user engagement metrics.


# 4️⃣ Firestore Source System

The script `1_setup_firestore.py` performs:

- Inserts **Pav Bhaji** as the primary record  
- Generates **19 additional vegetarian recipes**  
- Creates **10 sample users**  
- Inserts **120 user interactions**  

Recipes are structured with:

- 7–9 ingredients  
- 6–8 steps  
- Authentic tags  
- Weighted difficulty levels (50% easy, 35% medium, 15% hard)


# 5️⃣ ETL Pipeline 

### ✔ Extraction  
Using `firebase_admin`, data is exported from Firestore to JSON files.

### ✔ Transformation  
JSON is transformed into:

- recipe.csv  
- ingredients.csv  
- steps.csv  
- interactions.csv  
- users.csv  

This ensures **third normal form (3NF)** and separates repeating structures.

### ✔ Load  
Data is loaded into `outputs/` folder for further processing.


# 6️⃣ Data Validation Rules

Validation performed in `4_validate_csv.py`:

### ✔ Recipe-Level Validation
- Required fields present  
- No negative timing values  
- Difficulty ∈ {easy, medium, hard}  
- Tags not empty  
- Step order strictly increasing  

### ✔ Ingredients Validation
- recipe_id must exist  
- ingredient_name required  

### ✔ Interactions Validation
- Valid interaction type  
- Rating must be numeric (1–5)  

### ✔ Users Table
- Each user must have id and name  

A structured report is generated:
```
outputs/validation_report.json
```


# 7️⃣ Analytics & Insights

All analytics results saved in `analysis/`.

### Generated Outputs:
- Top ingredients  
- Difficulty distribution  
- Most viewed recipes  
- Ingredients in high-engagement recipes  
- Step count distribution  
- Most active users  
- Prep-time vs likes correlation  
- Summary text file  

### Charts included:
- Bar charts  
- Pie charts  
- Frequency distributions  


# 8️⃣ Folder Structure 

```
recipe-pipeline/
│
├── scripts/
├── outputs/
├── analysis/
├── seed_data.json
├── serviceAccount.json  (not included in repo)
└── README.md
```


# 9️⃣ How to Run the Pipeline

### Step 1 — Install Dependencies
```
pip install -r requirements.txt
```

### Step 2 — Generate Data
```
python scripts/1_setup_firestore.py
```

### Step 3 — Export Collections
```
python scripts/2_export_firestore.py
```

### Step 4 — Convert JSON → CSV
```
python scripts/3_transform_to_csv.py
```

### Step 5 — Validate CSV Files
```
python scripts/4_validate_csv.py
```

### Step 6 — Analytics
```
python scripts/5_analytics.py
```


# 🔟 Limitations

- Dataset is synthetic  
- Calories and regions approximated  
- Interaction patterns semi-random  
- Firestore performance depends on network  


# 🏁 Conclusion

This project demonstrates a **production-style data engineering workflow** integrating:

- Data generation  
- Data modeling  
- Firestore storage  
- ETL & normalization  
- Data validation  
- Insightful analytics  
- Visual report creation  

It is suitable for academic evaluation, industry portfolio, and learning end-to-end DE pipelines.
