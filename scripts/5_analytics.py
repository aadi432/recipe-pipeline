# scripts/5_analytics.py
import pandas as pd
import matplotlib.pyplot as plt
import os


# Setup

os.makedirs("analysis", exist_ok=True)

# Load ALL FIVE CSV FILES
recipes = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\recipe.csv")
ingredients = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\ingredients.csv")
interactions = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\interactions.csv")
steps = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\steps.csv")
users = pd.read_csv(r"C:\Users\DELL\Desktop\recipe-pipeline\outputs\users.csv")

# Safe copy
recipes = recipes.copy()
ingredients = ingredients.copy()
interactions = interactions.copy()
steps = steps.copy()
users = users.copy()


# 1. MOST COMMON INGREDIENTS

top_ingredients = ingredients["ingredient_name"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_ingredients.plot(kind="bar", color="skyblue")
plt.title("Top 10 Most Common Ingredients")
plt.xlabel("Ingredient")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("analysis/top_ingredients.png")
plt.clf()

top_ingredients.to_csv("analysis/top_ingredients.csv")


# 2. AVERAGE PREPARATION TIME

recipes["total_time"] = (
    recipes["prep_time_minutes"].fillna(0)
    + recipes["cook_time_minutes"].fillna(0)
)

avg_prep = recipes["prep_time_minutes"].mean()
avg_total = recipes["total_time"].mean()

pd.DataFrame({
    "average_prep_time": [avg_prep],
    "average_total_time": [avg_total]
}).to_csv("analysis/prep_time_summary.csv", index=False)


# 3. DIFFICULTY DISTRIBUTION

difficulty_dist = recipes["difficulty"].value_counts()

plt.figure(figsize=(7, 7))
difficulty_dist.plot(kind="pie", autopct="%1.1f%%")
plt.title("Difficulty Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("analysis/difficulty_distribution.png")
plt.clf()

difficulty_dist.to_csv("analysis/difficulty_distribution.csv")


# 4. CORRELATION BETWEEN PREP TIME AND LIKES

likes = interactions[interactions["type"] == "like"]
likes_count = likes.groupby("recipe_id").size().rename("likes")

time_likes = recipes.merge(
    likes_count, left_on="id", right_on="recipe_id", how="left"
)
time_likes["likes"] = time_likes["likes"].fillna(0)

correlation_value = time_likes["prep_time_minutes"].corr(time_likes["likes"])

pd.DataFrame({"correlation_prep_vs_likes": [correlation_value]}).to_csv(
    "analysis/correlation_prep_likes.csv", index=False
)


# 5. MOST FREQUENTLY VIEWED RECIPES

views = interactions[interactions["type"] == "view"]
views_count = views.groupby("recipe_id").size().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
views_count.plot(kind="bar", color="orange")
plt.title("Top 10 Most Viewed Recipes")
plt.xlabel("Recipe ID")
plt.ylabel("Views")
plt.tight_layout()
plt.savefig("analysis/top_viewed_recipes.png")
plt.clf()

views_count.to_csv("analysis/top_viewed_recipes.csv")


# 6. INGREDIENTS ASSOCIATED WITH HIGH ENGAGEMENT

median_likes = likes_count.median() if len(likes_count) > 0 else 0

high_engaged_recipe_ids = likes_count[likes_count >= median_likes].index.tolist()

high_engagement_ingredients = (
    ingredients[ingredients["recipe_id"].isin(high_engaged_recipe_ids)]["ingredient_name"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10, 6))
high_engagement_ingredients.plot(kind="bar", color="green")
plt.title("Ingredients in High-Engagement Recipes")
plt.xlabel("Ingredient")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("analysis/high_engagement_ingredients.png")
plt.clf()

high_engagement_ingredients.to_csv("analysis/high_engagement_ingredients.csv")


# 7. STEP COUNT ANALYSIS

step_counts = steps.groupby("recipe_id").size().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
step_counts.head(10).plot(kind="bar", color="purple")
plt.title("Top Recipes by Step Count")
plt.xlabel("Recipe ID")
plt.ylabel("Number of Steps")
plt.tight_layout()
plt.savefig("analysis/top_step_counts.png")
plt.clf()

step_counts.to_csv("analysis/step_counts.csv")

avg_steps_per_recipe = step_counts.mean()


# 8. MOST ACTIVE USERS

user_activity = interactions.groupby("user_id").size().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
user_activity.head(10).plot(kind="bar")
plt.title("Most Active Users")
plt.xlabel("User ID")
plt.ylabel("Total Interactions")
plt.tight_layout()
plt.savefig("analysis/top_active_users.png")
plt.clf()

user_activity.to_csv("analysis/top_active_users.csv")

# SUMMARY FILE

with open("analysis/insights_summary.txt", "w") as f:
    f.write("=== ANALYTICS SUMMARY ===\n\n")

    f.write(f"Average Preparation Time: {avg_prep:.2f} minutes\n")
    f.write(f"Average Total Cooking Time: {avg_total:.2f} minutes\n")
    f.write(f"Correlation (Prep Time vs Likes): {correlation_value:.4f}\n")
    f.write(f"Average Steps Per Recipe: {avg_steps_per_recipe:.2f}\n\n")

    f.write("\nTOP INGREDIENTS:\n")
    f.write(top_ingredients.to_string())
    f.write("\n\n")

    f.write("TOP VIEWED RECIPES:\n")
    f.write(views_count.to_string())
    f.write("\n\n")

    f.write("HIGH ENGAGEMENT INGREDIENTS:\n")
    f.write(high_engagement_ingredients.to_string())
    f.write("\n\n")

    f.write("STEP COUNTS PER RECIPE:\n")
    f.write(step_counts.to_string())
    f.write("\n\n")

    f.write("MOST ACTIVE USERS:\n")
    f.write(user_activity.to_string())
    f.write("\n\n")

print("Analytics complete! Check the analysis folder.")
