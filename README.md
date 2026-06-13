# 🍽️ NutriLens AI – Intelligent Food Detection & Nutrition Assistant

NutriLens AI is an advanced AI-powered food analysis system that detects food items from images, estimates portion sizes, analyzes nutritional content, and provides personalized dietary recommendations.

The system combines state-of-the-art Computer Vision, Retrieval-Augmented Generation (RAG), and Large Language Models to deliver accurate food recognition and intelligent nutrition guidance.

---

## 🚀 Key Features

### 🥗 Food Detection & Recognition
- Food / Non-Food Classification
- Fine-tuned CLIP model trained on the Food-20 dataset
- Multi-food recognition from a single image
- Robust food identification pipeline

### 🎯 Object Detection
- YOLOv8-based food localization
- Multiple food item detection
- Bounding box visualization
- Efficient inference for real-time applications

### 📏 Portion Estimation
- U²-Net for precise food segmentation
- MiDaS Depth Estimation for volume approximation
- Portion size calculation from segmented food regions
- Calorie estimation based on serving size

### 📊 Nutrition Analysis
- Indian Food Nutrition Dataset
- FNDDS (Food and Nutrient Database for Dietary Studies)
- Nutritional breakdown:
  - Calories
  - Protein
  - Carbohydrates
  - Fats
  - Fiber

### 🤖 AI Nutrition Assistant
- Powered by Llama through Groq API
- Personalized dietary recommendations
- Health-focused food suggestions
- Meal guidance and nutritional insights

### 📚 Retrieval-Augmented Generation (RAG)
- FAISS Vector Database
- Semantic search for nutrition knowledge
- Context-aware responses
- Medical and dietary information retrieval

### 🔐 User Authentication
- Secure registration and login
- Password hashing and authentication
- MongoDB user management

---

# 🧠 AI Pipeline

```text
Image Upload
      │
      ▼
Food / Non-Food Classification
(Fine-Tuned CLIP)
      │
      ▼
YOLOv8 Food Detection
      │
      ▼
Food Cropping
      │
      ▼
CLIP Food Recognition
      │
      ▼
U²-Net Segmentation
      │
      ▼
MiDaS Depth Estimation
      │
      ▼
Portion Size Calculation
      │
      ▼
Nutrition Retrieval
      │
      ▼
Llama (Groq)
Recommendations & Insights
```

---

# 🏗️ Project Structure

```text
FOOD_DETECTOR/
│
├── frontend/
│   ├── app.py
│   └── index.html
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── mongo_db.py
│   ├── rag_retriever.py
│   ├── vector_search.py
│   ├── recommender.py
│   ├── medical_retriever.py
│   ├── portion_estimator.py
│   ├── build_rag_db.py
│   └── build_medical_db.py
│
├── models/
│   ├── clip_model.py
│   ├── yolov8n.pt
│   ├── sam_vit_b.pth
│   └── checkpoint_best.pt
│
├── vector_db/
│   ├── fndds_rag.faiss
│   ├── fndds_docs.pkl
│   ├── ifnd_rag.faiss
│   ├── ifnd_docs.pkl
│   ├── medical.faiss
│   └── medical.pkl
│
├── data/
│   ├── diet.db
│   ├── disease.csv
│   ├── fndds.xlsx
│   └── indian_food_nutrition.xlsx
│
├── assets/
├── docs/
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

## Backend
- FastAPI
- Python

## Frontend
- Streamlit
- HTML/CSS

## Computer Vision
- YOLOv8
- OpenCV
- Pillow
- U²-Net
- MiDaS
- CLIP

## Machine Learning
- PyTorch
- NumPy
- Pandas

## Retrieval System
- FAISS
- Sentence Transformers

## Database
- MongoDB
- SQLite

## Large Language Models
- Llama 3
- Groq API

---

# 📂 Datasets

### Food-20 Dataset
Used for fine-tuning the CLIP model for food recognition.

### Indian Food Nutrition Dataset
Contains nutritional information for Indian food items.

### FNDDS Dataset
Food and Nutrient Database for Dietary Studies.

### Medical Knowledge Dataset
Used for dietary and health-related recommendations.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/NutriLens-AI.git

cd NutriLens-AI
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
MONGO_URI=your_mongodb_connection_string
```

---

# ▶️ Running the Backend

```bash
uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Running the Frontend

```bash
streamlit run frontend/app.py
```

Streamlit URL:

```text
http://localhost:8501
```

---

# 📈 Future Improvements

- Mobile App Integration
- Real-Time Camera Detection
- Barcode Scanner
- Meal Planning Assistant
- Diet Tracking Dashboard
- Cloud Deployment
- Multi-language Support

---

# 🎯 Applications

- Smart Nutrition Assistant
- Diet Monitoring
- Health & Fitness Tracking
- Calorie Estimation
- Personalized Food Recommendations
- Medical Dietary Guidance

---

# 👩‍💻 Author

**Gayathri**  
B.Tech – Computer Science Engineering (AI & ML)

---

# 📜 License

This project is developed for educational, research, and portfolio purposes.