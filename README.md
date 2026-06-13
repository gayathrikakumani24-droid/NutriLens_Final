# 🍽️ NutriLens AI – Intelligent Food Detection & Nutrition Assistant

<img width="1366" height="643" alt="Screenshot (345)" src="https://github.com/user-attachments/assets/75f3d4e9-a877-4a8e-aef4-05dafd34d610" />

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
## 📂 Project Structure

### Frontend
- **app.py** – Streamlit application entry point and user interface (optional).
- **index.html** – Frontend template for web rendering.

### Backend
- **main.py** – Main API and application logic using FASTAPI.
- **auth.py** – User authentication and authorization.
- **database.py** – Database connection and operations.
- **mongo_db.py** – MongoDB integration and queries.
- **rag_retriever.py** – Retrieves nutrition knowledge using RAG.
- **vector_search.py** – FAISS-based semantic search functionality.
- **recommender.py** – Personalized food recommendation engine.
- **medical_retriever.py** – Retrieves disease-specific dietary information.
- **portion_estimator.py** – Estimates food portion sizes from detected items.
- **build_rag_db.py** – Builds the nutrition knowledge vector database.
- **build_medical_db.py** – Builds the medical knowledge vector database.

### Models
- Model weights are excluded from GitHub due to size limitations.
- **clip_model.py** – CLIP-based image-text embedding utilities.
- **yolov8n.pt** – YOLOv8 model for food object detection.
- **sam_vit_b.pth** – Segment Anything Model (SAM) for food segmentation.
- **checkpoint_best.pt** – Custom trained food classification model.

### Vector Database
- **fndds_rag.faiss** – FAISS index for nutrition retrieval.
- **fndds_docs.pkl** – Nutrition document metadata.
- **ifnd_rag.faiss** – Indian food nutrition vector index.
- **ifnd_docs.pkl** – Indian food nutrition metadata.
- **medical.faiss** – Medical knowledge vector index.
- **medical.pkl** – Medical knowledge metadata.

### Data
- **diet.db** – Local database containing dietary information.
- **disease.csv** – Disease and dietary guideline dataset.
- **fndds.xlsx** – Food and Nutrient Database for Dietary Studies.
- **indian_food_nutrition.xlsx** – Indian food nutrition dataset.

### Additional Resources
- **assets/** – Screenshots of outputs.
- **docs/** – Project documentation.
- **requirements.txt** – Python dependencies.
- **README.md** – Project overview and setup instructions.

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
# Architecture
<img width="1366" height="768" alt="Screenshot (115)" src="https://github.com/user-attachments/assets/9003ea92-d78f-4529-9032-9b637fc5e7ec" />

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
git clone https://github.com/gayathrikakumani24-droid/NutriLens_Final.git

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
## Create vector databases

```bash
python build_rag_db.py
python build_medical_db.py
```

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
---
## 📈 Results

- Accurate food recognition using fine-tuned CLIP on Food-20 dataset.
- Multi-food detection using YOLOv8.
- Portion estimation using U²-Net segmentation and MiDaS depth estimation.
- Nutrition analysis from FNDDS and Indian Food Nutrition datasets.
- Personalized dietary recommendations generated using Llama via Groq API.
### Login Page

<img width="1366" height="643" alt="Screenshot (345)" src="https://github.com/user-attachments/assets/75f3d4e9-a877-4a8e-aef4-05dafd34d610" />

### Analysis Page

<img width="1366" height="635" alt="Screenshot (350)" src="https://github.com/user-attachments/assets/e7e825a2-5f8e-4c1f-bd37-2d23e714e0fa" />

### Analytics Page

<img width="1366" height="640" alt="Screenshot (353)" src="https://github.com/user-attachments/assets/9d11dff3-2646-4685-9699-ccc84a291a59" />

### Profile Page

<img width="1366" height="638" alt="Screenshot (355)" src="https://github.com/user-attachments/assets/15dd4361-bb6d-4146-b61e-89740054778e" />

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
