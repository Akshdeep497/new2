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

- `GEMINI_API_KEY`: Your Gemini Pro API key to access generative AI services.
- Optional for vector DB:
  - `PINECONE_API_KEY`
  - `PINECONE_INDEX_NAME`

Example: create a `.env` file in `ikarus-backend/backend` (ignored by Git) or set environment variables directly in your deployment platform.

### Frontend

- `VITE_API_BASE_URL`: Base URL of the backend API (e.g., `http://localhost:8000` for development).

Create a `.env` file in `ikarus-frontend`:

## Setup & Run Locally

### Backend (FastAPI)

1. Navigate to backend directory:

2. Create and activate a virtual environment:
- On Windows (PowerShell):
  ```
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- On macOS/Linux:
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  ```

3. Install dependencies:

4. Run the FastAPI server:

Backend API docs available at `http://127.0.0.1:8000/docs`.

### Frontend (React + Vite)

1. Navigate to frontend directory:

2. Install dependencies:

3. Create `.env` with backend API base URL (if not already done).

4. Start development server:

5. Open `http://localhost:5176` in your browser.

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

