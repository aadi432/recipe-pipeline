import pandas as pd
import matplotlib.pyplot as plt
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
def safe_read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# =====================================================
# MAIN ANALYTICS FUNCTION
# =====================================================
def run_analytics():
    # Folders
    clean_folder = os.path.join("outputs", "clean")
    analysis_folder = "analysis"
    os.makedirs(analysis_folder, exist_ok=True)
    logger.info("Analysis folder ready.")

    # -----------------------------
    # Load cleaned CSV files
    # -----------------------------
    logger.info("Loading cleaned CSV files for analytics...")

    recipes = safe_read_csv(os.path.join(clean_folder, "recipes_clean.csv"))
    ingredients = safe_read_csv(os.path.join(clean_folder, "ingredients_clean.csv"))
    interactions = safe_read_csv(os.path.join(clean_folder, "interactions_clean.csv"))
    steps = safe_read_csv(os.path.join(clean_folder, "steps_clean.csv"))
    users = safe_read_csv(os.path.join(clean_folder, "users_clean.csv"))

    # Safe copies
    recipes = recipes.copy()
    ingredients = ingredients.copy()
    interactions = interactions.copy()
    steps = steps.copy()
    users = users.copy()

    logger.info("CSV files loaded successfully. Starting analytics...")

    # --------------------------------------------------------------
    # DERIVED METRICS
    # --------------------------------------------------------------
    logger.info("Calculating derived metrics...")

    # Total time
    recipes["total_time"] = (
        recipes["prep_time_minutes"].fillna(0) +
        recipes["cook_time_minutes"].fillna(0)
    )

    # Interactions split
    likes = interactions[interactions["type"] == "like"]
    views = interactions[interactions["type"] == "view"]
    attempts = interactions[interactions["type"] == "cook_attempt"]

    likes_count = likes.groupby("recipe_id").size().rename("likes")
    views_count_full = views.groupby("recipe_id").size().rename("views")
    attempts_count = attempts.groupby("recipe_id").size().rename("attempts")

    # Merge engagement metrics back to recipes
    recipes = recipes.merge(likes_count, left_on="id", right_index=True, how="left")
    recipes = recipes.merge(views_count_full, left_on="id", right_index=True, how="left")
    recipes = recipes.merge(attempts_count, left_on="id", right_index=True, how="left")

    recipes["likes"] = recipes["likes"].fillna(0)
    recipes["views"] = recipes["views"].fillna(0)
    recipes["attempts"] = recipes["attempts"].fillna(0)

    # --------------------------------------------------------------
    # RECIPE COMPLEXITY SCORE
    # complexity = prep_time + cook_time + number_of_steps
    # --------------------------------------------------------------
    step_counts_raw = steps.groupby("recipe_id").size().rename("step_count")
    recipes = recipes.merge(step_counts_raw, left_on="id", right_index=True, how="left")
    recipes["step_count"] = recipes["step_count"].fillna(0)

    recipes["complexity_score"] = (
        recipes["prep_time_minutes"].fillna(0)
        + recipes["cook_time_minutes"].fillna(0)
        + recipes["step_count"]
    )

    # --------------------------------------------------------------
    # USER ENGAGEMENT SCORE
    # engagement_score = views*0.5 + likes*1 + attempts*2
    # --------------------------------------------------------------
    recipes["engagement_score"] = (
        recipes["views"] * 0.5 +
        recipes["likes"] * 1.0 +
        recipes["attempts"] * 2.0
    )

    # ==============================================================
    # 1. MOST COMMON INGREDIENTS
    # ==============================================================
    logger.info("Generating: Top common ingredients chart & CSV...")

    top_ingredients = ingredients["ingredient_name"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    top_ingredients.plot(kind="bar", color="skyblue")
    plt.title("Top 10 Most Common Ingredients")
    plt.xlabel("Ingredient")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "top_ingredients.png"))
    plt.clf()

    top_ingredients.to_csv(os.path.join(analysis_folder, "top_ingredients.csv"))

    # ==============================================================
    # 2. AVERAGE PREPARATION & TOTAL TIME
    # ==============================================================
    logger.info("Generating: Prep time summary CSV...")

    avg_prep = recipes["prep_time_minutes"].mean()
    avg_total = recipes["total_time"].mean()

    pd.DataFrame({
        "average_prep_time": [avg_prep],
        "average_total_time": [avg_total]
    }).to_csv(os.path.join(analysis_folder, "prep_time_summary.csv"), index=False)

    # ==============================================================
    # 3. DIFFICULTY DISTRIBUTION
    # ==============================================================
    logger.info("Generating: Difficulty distribution chart & CSV...")

    difficulty_dist = recipes["difficulty"].value_counts()

    plt.figure(figsize=(7, 7))
    difficulty_dist.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Difficulty Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "difficulty_distribution.png"))
    plt.clf()

    difficulty_dist.to_csv(os.path.join(analysis_folder, "difficulty_distribution.csv"))

    # ==============================================================
    # 4. CORRELATION BETWEEN PREP TIME AND LIKES
    # ==============================================================
    logger.info("Generating: Prep vs Likes correlation and scatter chart...")

    correlation_value = recipes["prep_time_minutes"].corr(recipes["likes"])

    pd.DataFrame({"correlation_prep_vs_likes": [correlation_value]}).to_csv(
        os.path.join(analysis_folder, "correlation_prep_likes.csv"), index=False
    )

    plt.figure(figsize=(8, 6))
    plt.scatter(recipes["prep_time_minutes"], recipes["likes"])
    plt.title(f"Prep Time vs Likes (corr = {correlation_value:.2f})")
    plt.xlabel("Prep Time (minutes)")
    plt.ylabel("Likes")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "prep_vs_likes_scatter.png"))
    plt.clf()

    # ==============================================================
    # 5. MOST FREQUENTLY VIEWED RECIPES (Top 10 and Top 15)
    # ==============================================================
    logger.info("Generating: Top viewed recipes charts & CSV...")

    top_views_10 = recipes.sort_values("views", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(top_views_10["id"], top_views_10["views"], color="orange")
    plt.title("Top 10 Most Viewed Recipes")
    plt.xlabel("Recipe ID")
    plt.ylabel("Views")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "top_viewed_recipes.png"))
    plt.clf()

    top_views_10.to_csv(os.path.join(analysis_folder, "top_viewed_recipes.csv"), index=False)

    # Extra: Top 15 viewed
    top_views_15 = recipes.sort_values("views", ascending=False).head(15)
    plt.figure(figsize=(12, 6))
    plt.bar(top_views_15["id"], top_views_15["views"], color="orange")
    plt.title("Top 15 Most Viewed Recipes")
    plt.xlabel("Recipe ID")
    plt.ylabel("Views")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "top15_viewed_recipes.png"))
    plt.clf()

    # ==============================================================
    # 6. INGREDIENTS ASSOCIATED WITH HIGH ENGAGEMENT
    # ==============================================================
    logger.info("Generating: High engagement ingredients chart & CSV...")

    median_likes = recipes["likes"].median()
    high_engaged_recipe_ids = recipes[recipes["likes"] >= median_likes]["id"]

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
    plt.savefig(os.path.join(analysis_folder, "high_engagement_ingredients.png"))
    plt.clf()

    high_engagement_ingredients.to_csv(
        os.path.join(analysis_folder, "high_engagement_ingredients.csv")
    )

    # ==============================================================
    # 7. STEP COUNT ANALYSIS
    # ==============================================================
    logger.info("Generating: Step count analysis chart & CSV...")

    step_counts = steps.groupby("recipe_id").size().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    step_counts.head(10).plot(kind="bar", color="purple")
    plt.title("Top Recipes by Step Count")
    plt.xlabel("Recipe ID")
    plt.ylabel("Number of Steps")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "top_step_counts.png"))
    plt.clf()

    step_counts.to_csv(os.path.join(analysis_folder, "step_counts.csv"))

    avg_steps_per_recipe = step_counts.mean()

    # ==============================================================
    # 8. MOST ACTIVE USERS (Top 20)
    # ==============================================================
    logger.info("Generating: Most active users chart & CSV...")

    user_activity_20 = interactions.groupby("user_id").size().sort_values(ascending=False).head(20)

    plt.figure(figsize=(12, 6))
    user_activity_20.plot(kind="bar")
    plt.title("Top 20 Most Active Users")
    plt.xlabel("User ID")
    plt.ylabel("Total Interactions")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "top_active_users_20.png"))
    plt.clf()

    user_activity_20.to_csv(os.path.join(analysis_folder, "top_active_users_20.csv"))

    # ==============================================================
    # 9. PREP TIME vs COOK TIME (Scatter)
    # ==============================================================
    logger.info("Generating: Prep vs Cook time scatter chart...")

    plt.figure(figsize=(8, 6))
    plt.scatter(recipes["prep_time_minutes"], recipes["cook_time_minutes"], alpha=0.7)
    plt.title("Prep Time vs Cook Time")
    plt.xlabel("Prep Time (minutes)")
    plt.ylabel("Cook Time (minutes)")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "prep_vs_cook_scatter.png"))
    plt.clf()

    # ==============================================================
    # 10. CORRELATION MATRIX (Numeric Fields)
    # ==============================================================
    logger.info("Generating: Correlation matrix chart & CSV...")

    numeric_cols = [
        "prep_time_minutes",
        "cook_time_minutes",
        "total_time",
        "likes",
        "views",
        "attempts",
        "complexity_score",
        "engagement_score",
    ]
    numeric_present = [c for c in numeric_cols if c in recipes.columns]

    corr_matrix = recipes[numeric_present].corr()

    plt.figure(figsize=(10, 8))
    plt.imshow(corr_matrix, cmap="coolwarm", interpolation="nearest")
    plt.colorbar()
    plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=45)
    plt.yticks(range(len(corr_matrix)), corr_matrix.columns)
    plt.title("Correlation Matrix (Numeric Recipe Analytics)")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "correlation_matrix.png"))
    plt.clf()

    corr_matrix.to_csv(os.path.join(analysis_folder, "correlation_matrix.csv"))

    # ==============================================================
    # 11. COMPLEXITY DISTRIBUTION + TOP/SIMPLEST RECIPES
    # ==============================================================
    logger.info("Generating: Complexity distribution charts & CSV...")

    plt.figure(figsize=(10, 6))
    recipes["complexity_score"].plot(kind="hist", bins=15)
    plt.title("Recipe Complexity Score Distribution")
    plt.xlabel("Complexity Score")
    plt.ylabel("Number of Recipes")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "complexity_distribution.png"))
    plt.clf()

    top_complex = recipes.sort_values("complexity_score", ascending=False).head(10)
    top_complex.to_csv(os.path.join(analysis_folder, "top10_most_complex_recipes.csv"), index=False)

    simplest = recipes.sort_values("complexity_score", ascending=True).head(10)
    simplest.to_csv(os.path.join(analysis_folder, "simplest_recipes.csv"), index=False)

    # ==============================================================
    # 12. TOP ENGAGED RECIPES (Using engagement_score)
    # ==============================================================
    logger.info("Generating: Top engaged recipes chart & CSV...")

    top_engaged = recipes.sort_values("engagement_score", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(top_engaged["id"], top_engaged["engagement_score"], color="red")
    plt.title("Top 10 Recipes by Engagement Score")
    plt.xlabel("Recipe ID")
    plt.ylabel("Engagement Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "top_engaged_recipes.png"))
    plt.clf()

    top_engaged.to_csv(os.path.join(analysis_folder, "top_engaged_recipes.csv"), index=False)

    # ==============================================================
    # 13. SENTIMENT ANALYSIS (Titles + Steps)
    # ==============================================================
    logger.info("Running simple sentiment analysis and chart...")

    positive_words = [
        "delicious", "tasty", "yummy", "flavourful", "flavorful",
        "crispy", "creamy", "buttery", "spicy", "rich"
    ]
    negative_words = [
        "burnt", "soggy", "bland", "overcooked",
        "undercooked", "salty", "bitter"
    ]

    sentiment_rows = []

    for _, r in recipes.iterrows():
        rid = r["id"]
        title = str(r.get("title", ""))
        desc = str(r.get("description", ""))

        # gather all step text for this recipe
        step_texts = steps[steps["recipe_id"] == rid]["step_text"].astype(str).tolist()
        full_text = (title + " " + desc + " " + " ".join(step_texts)).lower()

        pos_count = sum(word in full_text for word in positive_words)
        neg_count = sum(word in full_text for word in negative_words)
        score = pos_count - neg_count

        if score > 0:
            label = "Positive"
        elif score < 0:
            label = "Negative"
        else:
            label = "Neutral"

        sentiment_rows.append({
            "id": rid,
            "title": title,
            "sentiment_score": score,
            "sentiment_label": label
        })

    sentiment_df = pd.DataFrame(sentiment_rows)
    sentiment_df.to_csv(os.path.join(analysis_folder, "recipe_sentiment.csv"), index=False)

    # Sentiment distribution chart
    sent_counts = sentiment_df["sentiment_label"].value_counts()

    plt.figure(figsize=(8, 5))
    plt.bar(sent_counts.index, sent_counts.values, color=["green", "red", "gray"])
    plt.title("Recipe Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Recipes")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_folder, "sentiment_bar_chart.png"))
    plt.clf()

    # ==============================================================
    # SUMMARY FILE
    # ==============================================================
    logger.info("Writing insights_summary.txt...")

    summary_path = os.path.join(analysis_folder, "insights_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=== ANALYTICS SUMMARY ===\n\n")
        f.write(f"Average Preparation Time: {avg_prep:.2f} minutes\n")
        f.write(f"Average Total Cooking Time: {avg_total:.2f} minutes\n")
        f.write(f"Correlation (Prep Time vs Likes): {correlation_value:.4f}\n")
        f.write(f"Average Steps Per Recipe: {avg_steps_per_recipe:.2f}\n\n")

        f.write("\nTOP INGREDIENTS:\n")
        f.write(top_ingredients.to_string())
        f.write("\n\n")

        f.write("TOP VIEWED RECIPES (Top 10):\n")
        f.write(top_views_10[["id", "views"]].to_string())
        f.write("\n\n")

        f.write("HIGH ENGAGEMENT INGREDIENTS:\n")
        f.write(high_engagement_ingredients.to_string())
        f.write("\n\n")

        f.write("TOP ENGAGED RECIPES (by engagement_score):\n")
        f.write(top_engaged[["id", "engagement_score"]].to_string())
        f.write("\n\n")

        f.write("COMPLEXITY: Most complex recipes:\n")
        f.write(top_complex[["id", "title", "complexity_score"]].to_string())
        f.write("\n\n")

        f.write("Sentiment distribution:\n")
        f.write(sent_counts.to_string())
        f.write("\n\n")

    logger.info("Analytics complete! Check the analysis folder.")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    try:
        run_analytics()
    except Exception as e:
        logger.error("Analytics failed: %s", e)
        raise
