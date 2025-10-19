# Ikuras Product Recommendation & Analytics Web App

This project is a full-stack furniture product recommendation system with semantic search, computer vision-aware reranking, and generative AI descriptions powered by FastAPI backend and React frontend.

#What I used
Backend: FastAPI, Uvicorn, Pydantic

Frontend: React (Vite), React Router

Dataset: intern_data_ikarus.csv

ML (recommendations): sentence-transformers all-MiniLM-L6-v2 (384‑dim), cosine similarity search

NLP: Hugging Face Transformers, text normalization, LangChain for orchestration

CV: MobileNetV3‑Small for offline image category labels (cv_label, cv_conf)

GenAI: Google Gemini Pro API via LangChain for per‑item descriptions

Vector database: FAISS (local dev) and Pinecone (cloud semantic search)

Analytics: pandas, numpy, seaborn, matplotlib (analytics.ipynb)

Config: .env for secrets (GEMINI_API_KEY, Pinecone keys), CORS in FastAPI

Deployment: Frontend on Vercel (static), Backend on Vercel Python Serverless Functions

Build tools: Node.js 18+, Python 3.10+, Git

## Features

- Backend (FastAPI) exposing APIs for recommendation, analytics, and generative descriptions.
- Frontend (React + Vite) providing a user interface to search, view products, generate descriptions, and view analytics.
- Embedding-based semantic retrieval with sentence-transformers.
- Optional computer vision-based reranking for more relevant product suggestions.
- Analytics summaries with price, brand, and category distributions.

## Prerequisites

- Python 3.10+ for Backend
- Node.js 18+ for Frontend
- Git for version control
- API keys for generative AI (e.g., GEMINI_API_KEY)

## Environment Variables

### Backend

- `GEMINI_API_KEY`: Your Gemini Pro API key to access generative AI services.


Example: create a `.env` file in `ikarus-backend/backend` (ignored by Git) or set environment variables directly in your deployment platform.

### Frontend

- `VITE_API_BASE_URL`: Base URL of the backend API (e.g., `http://localhost:8000` for development).

Create a `.env` file in `ikarus-frontend`:

## Setup & Run Locally

### Backend (FastAPI)
```
# Navigate to the backend folder
cd ikarus-backend/backend

# Create a virtual environment (only once)
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (only once or after changes)
pip install -r requirements.txt

# Run the FastAPI backend server
uvicorn app.main:app --reload --port 8000

```

Backend API docs available at `http://127.0.0.1:8000/docs`.

### Frontend (React + Vite)

```
# Navigate to the frontend folder
cd ikarus-frontend

# Install npm dependencies (only once or after package.json changes)
npm install

# Ensure your .env file has VITE_API_BASE_URL=http://127.0.0.1:8000

# Run the React frontend development server
npm run dev -- --host --port 5176

```


## Running the App

- On the frontend home page, enter a search query and optionally filter by category or price.
- Click “Generate description” on product cards to get AI-generated product summaries.
- Use the Analytics page to view dataset insights such as price distributions and top brands.

## Deployment

### Backend

- Package and deploy the backend on any Python-friendly host (Render, Railway, HuggingFace Spaces with Docker, etc.).
- Set environment variables (GEMINI_API_KEY, optional Pinecone keys) on the target platform.
- Ensure CORS middleware allows the frontend's deployed URL.

### Frontend

- Deploy the frontend on Vercel or any static hosting provider.
- Set `VITE_API_BASE_URL` environment variable in the deployment settings to your backend’s deployed URL.
- Redeploy after environment variable changes for settings to apply.

## Recommended Git Ignore

Add `.gitignore` files ignoring environment folders, node_modules, build artifacts, and sensitive files such as `.env`.

Example `.gitignore` content in the project root:
node_modules/
dist/
build/
.venv/
venv/
pycache/
.pyc
.env
.env.
.DS_Store
Thumbs.db

## Notebooks

- Located in `notebooks/`, containing:
  - `analytics.ipynb`: Data exploration, cleaning, and summary metrics.
  - `cv_training.ipynb`: Computer vision model setup, training, and predictions.

## Additional Notes

- Ensure your models and vector indexes are sized to prevent long cold starts or timeouts.
- Cache expensive generated descriptions to reduce calls to generative AI services.
- Maintain consistent embedding dimensions (384 for all-MiniLM-L6-v2).
- Regularly rotate and protect your API keys, never commit them to version control.

## License

MIT or your preferred license. Add a LICENSE file if publishing publicly.

---

If you need help with deployment on specific platforms or further customization, please check the respective platform guides or contact the maintainer.




