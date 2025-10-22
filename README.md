
# Live Deployment

Frontend (Vercel): https://new2-mu-six.vercel.app

Backend API (Hugging Face): https://akshdeep497-ikuras.hf.space

API Docs (Swagger UI): https://akshdeep497-ikuras.hf.space/docs


# Ikuras Product Recommendation & Analytics Web App

This project is a full-stack furniture product recommendation system with semantic search, computer vision-aware reranking, and generative AI descriptions powered by FastAPI backend and React frontend.



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

- `GEMINI_API_KEY`: AIzaSyBVUaP6WyC-ngFkBZR6MPYaovxL4gb8C08
  ```
  GEMINI_API_KEY=AIzaSyBVUaP6WyC-ngFkBZR6MPYaovxL4gb8C08
  ```


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
# what is used 
# Machine Learning (ML)
Implemented embedding-based semantic recommendation using SentenceTransformer all-MiniLM-L6-v2 with normalized embeddings and FAISS inner-product search; indices are built from CSV via build_indices and persisted under data/ikarus_index.*.​

API: POST /recommend takes {query, k} and returns top-k items with similarity scores and product metadata for rendering.​

Key modules: embed.py (encoder), retriever.py (query > FAISS), vector_store.py (FAISS), ingest.py (CSV > index), recommend.py (endpoint).​

# Natural Language Processing (NLP)
Product text is composed from title, description, categories, brand, material, and color, then encoded into 384‑dim vectors for grouping similar or related products.​

Normalized embeddings enable cosine-equivalent inner-product retrieval in FAISS for clustering and top‑k semantic matches.​

# Computer Vision (CV)
Current build parses and returns product image URLs from the dataset and surfaces a cv_label histogram in analytics if the column exists; the classifier itself is planned as a next step.​

Planned: add a lightweight classifier (e.g., ResNet18/ViT‑tiny) to predict category/type per image and write outputs to cv_label for analytics and UI filtering.​

# Generative AI (GenAI)
Integrated LangChain ChatGoogleGenerativeAI with model “gemini‑2.5‑flash‑lite” to generate 60–90 word product design descriptions via POST /recommend/gen-desc.​

Uses GOOGLE_API_KEY; generation is decoupled from retrieval to control latency/cost and can be invoked per recommended item from the frontend.​

# Vector Database
Using FAISS CPU (IndexFlatIP) persisted to .index and .meta.json; vectors are 384‑dim MiniLM embeddings and searched via inner product.​

To switch to Pinecone, replace FaissStore usage in ingestion/retrieval with a Pinecone client while keeping the same stored metadata structure.​

# Frontend (React)
Vite + React frontend calls POST /recommend with the user prompt and then POST /recommend/gen-desc for each item to render product cards with images and generated descriptions.​

CORS is configured to allow localhost dev servers on ports 5173, 5175, and 5176 for smooth local development.​

# Analytics Page
GET /analytics/summary returns total products, price stats (avg, median, p10, p90), top categories/brands, image coverage, and an optional cv_label histogram if present.​

Analytics normalizes prices (currency symbols, ranges) and parses categories for histograms; consume this route in a React page with charts via client-side routing.
## License

MIT or your preferred license. Add a LICENSE file if publishing publicly.

---










