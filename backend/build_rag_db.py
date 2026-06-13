from sentence_transformers import SentenceTransformer
import pandas as pd
import faiss
import numpy as np
import pickle


model = SentenceTransformer("all-MiniLM-L6-v2")
def build_db(file_path, file_type="fndds"):

    # =========================
    # Load file safely
    # =========================
    try:
        print(f"📂 Loading CSV: {file_path}")
        df = pd.read_csv(file_path)
    except:
        print("⚠️ Using robust CSV loader...")
        df = pd.read_csv(file_path, engine="python", on_bad_lines="skip")

    print("Columns:", df.columns)
    print("Total rows:", len(df))

    documents = []
    texts = []

    for _, row in df.iterrows():
        try:
            # -------- CLEANED FNDDS --------
            if file_type == "fndds":
                food = str(row.get("food_description", row.get("Food Name", "")))
                calories = float(row.get("energy_kcal", row.get("Calories (kcal)", 0)))
                protein = float(row.get("protein_g", row.get("Protein (g)", 0)))
                carbs = float(row.get("carbs_g", row.get("Carbohydrates (g)", 0)))
                fat = float(row.get("fat_g", row.get("Fats (g)", 0)))

            # -------- INDIAN DATASET --------
            else:
                food = str(row.get("Food Name", row.get("food_description", "")))
                calories = float(row.get("Calories (kcal)", row.get("energy_kcal", 0)))
                protein = float(row.get("Protein (g)", row.get("protein_g", 0)))
                carbs = float(row.get("Carbohydrates (g)", row.get("carbs_g", 0)))
                fat = float(row.get("Fats (g)", row.get("fat_g", 0)))

            if food.strip() == "":
                continue

            text = f"""
            Food: {food}
            Calories: {calories}
            Protein: {protein}
            Carbs: {carbs}
            Fat: {fat}
            """

            documents.append(text)
            texts.append(food)

        except:
            continue

    print(f"✅ Processed {len(documents)} documents")
    embeddings=model.encode(texts)
    embeddings = np.array(embeddings)

# 🚨 Handle single vector case
    if len(embeddings.shape) == 1:
      embeddings = embeddings.reshape(1, -1)

    print("Embedding shape:", embeddings.shape)

# Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.astype("float32"))


    return index, documents


# =========================
# BUILD CLEANED FNDDS
# =========================
fndds_index, fndds_docs = build_db("E:\\food_detctor\\data\\fndds.xlsx", "fndds")
faiss.write_index(fndds_index, "fndds_rag.faiss")

with open("fndds_docs.pkl", "wb") as f:
    pickle.dump(fndds_docs, f)

print("✅ CLEANED FNDDS DB built")


# =========================
# BUILD INDIAN DATASET
# =========================
ifnd_index, ifnd_docs = build_db("E:\\food_detctor\\data\\indian_food_nutrition_dataset_v2 (1).csv.xls", "ifnd")
faiss.write_index(ifnd_index, "ifnd_rag.faiss")

with open("ifnd_docs.pkl", "wb") as f:
    pickle.dump(ifnd_docs, f)

print("✅ INDIAN FOOD DB built")

print("🎉 DONE")