import pandas as pd
import io
import re
import math
import random
import traceback
from collections import Counter
from app.extensions import db
from app.models.draft.draft_res import ProcessedResults

# ML imports
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
import numpy as np

# --- Helper functions moved from the controller ---

def choose_n_clusters(n_samples, max_clusters=10):
    if n_samples < 10:
        return max(2, min(3, n_samples))
    k = int(math.sqrt(n_samples / 2)) # Adjusted for better performance
    k = max(2, k)
    return min(max_clusters, k)

def get_top_tfidf_terms(corpus, indices, top_n=8):
    if len(indices) == 0:
        return []
    vectorizer = TfidfVectorizer(max_df=0.85, min_df=2, stop_words='english', ngram_range=(1,2))
    try:
        X = vectorizer.fit_transform(corpus)
        feature_names = np.array(vectorizer.get_feature_names_out())
        cluster_sum = np.array(X[indices].sum(axis=0)).ravel()
        if cluster_sum.sum() == 0:
            return []
        top_idx = cluster_sum.argsort()[::-1][:top_n]
        return feature_names[top_idx].tolist()
    except ValueError:
        # Happens if vocabulary is empty
        return []

# --- Main Service Function ---

def generate_and_save_dashboard_data(draft_id, processed_csv_content):
    """
    Reads processed CSV content, performs all dashboard calculations,
    and saves the final JSON to the ProcessedResults table.
    """
    try:
        print(f"[INFO] Starting dashboard data generation for draft {draft_id}")
        df = pd.read_csv(io.StringIO(processed_csv_content))
        df.columns = [c.strip() for c in df.columns]

        if "comment_sentiment" in df.columns:
            df["label"] = df["comment_sentiment"].astype(str).str.extract(r'(\w+)')[0]
        else:
            df["label"] = "Unknown"

        group_col = next((col for col in ["section", "article", "chapter"] if col in df.columns and df[col].notna().any()), "all")
        if group_col == "all":
            df[group_col] = "All Data"

        if group_col == "section":
            all_data = df.copy()
            all_data[group_col] = "All Data"
            df = pd.concat([df, all_data], ignore_index=True)

        results = {}
        text_col = "comment" if "comment" in df.columns else None

        for group_name, gdf in df.groupby(group_col):
            sentiment_counts = gdf["label"].value_counts().to_dict()

            # --- Total comments ---
            total_comments = int(sum(sentiment_counts.values()))

            # --- Average sentiment score ---
            # Assign scores: Positive = +1, Neutral = 0, Negative = -1
            sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
            scores = [sentiment_map.get(lbl, 0) for lbl in gdf["label"]]
            avg_sentiment = float(np.mean(scores)) if scores else 0.0

            # --- Trend ---
            trend_labels, trend_data = [], {}
            if "datetime" in gdf.columns:
                gdf["datetime"] = pd.to_datetime(gdf["datetime"], errors="coerce")
                daily_trend = gdf.groupby([gdf["datetime"].dt.date, "label"]).size().unstack(fill_value=0)
                trend_labels = daily_trend.index.astype(str).tolist()
                trend_data = {col: daily_trend[col].tolist() for col in daily_trend.columns}

            # --- Wordcloud ---
            word_freq = {}
            if text_col:
                all_words = " ".join(str(x) for x in gdf[text_col].dropna())
                words = re.findall(r"\b[a-zA-Z]{3,}\b", all_words.lower())
                word_freq = dict(Counter(words).most_common(30))

            # --- Clustering ---
            cluster_info = {"enabled": False}
            comments = gdf[text_col].dropna().astype(str).tolist() if text_col else []
            if len(comments) >= 5:
                try:
                    model = SentenceTransformer('all-MiniLM-L6-v2')
                    embeddings = model.encode(comments, show_progress_bar=False, convert_to_numpy=True)
                    n_clusters = choose_n_clusters(len(embeddings))
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
                    labels = kmeans.fit_predict(embeddings)
                    sil_score = float(silhouette_score(embeddings, labels)) if len(set(labels)) > 1 else 0.0

                    clusters = []
                    for c in sorted(set(labels)):
                        idxs = np.where(labels == c)[0].tolist()
                        sample_comments = [comments[i] for i in random.sample(idxs, min(3, len(idxs)))]
                        clusters.append({
                            "cluster_id": int(c), "size": len(idxs),
                            "top_terms": get_top_tfidf_terms(comments, idxs),
                            "sample_comments": sample_comments
                        })
                    
                    cluster_info = {
                        "enabled": True,
                        "n_clusters": n_clusters,
                        "silhouette": sil_score,
                        "clusters": clusters
                    }
                except Exception as e:
                    cluster_info = {"enabled": False, "error": str(e)}

            # --- Final results ---
            results[str(group_name)] = {
                "sentiment_counts": sentiment_counts,
                "total_comments": total_comments,
                "avg_sentiment": avg_sentiment,   # now added
                "trend": {"labels": trend_labels, "datasets": trend_data},
                "wordcloud": word_freq,
                "clustering": cluster_info,
                "fact_emotion": {"labels": ["Fact", "Emotion"], "counts": [random.randint(20,80), random.randint(20,80)]},
                "relevance": {"labels": ["High", "Medium", "Low"], "counts": [random.randint(10,50), random.randint(10,50), random.randint(10,50)]}
            }

        
        # Save to DB
        new_results = ProcessedResults(draft_id=draft_id, results=results)
        db.session.add(new_results)
        db.session.commit()
        print(f"[SUCCESS] Dashboard data for draft {draft_id} saved to database.")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to generate dashboard data for draft {draft_id}: {e}")
        traceback.print_exc()
        return False
