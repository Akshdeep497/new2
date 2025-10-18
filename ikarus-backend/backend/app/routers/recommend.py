from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from pathlib import Path
from ..schemas import RecommendRequest, RecommendResponse
from ..services.retriever import Recommender
from langchain_google_genai import ChatGoogleGenerativeAI
import os

router = APIRouter(prefix="/recommend", tags=["recommend"])

# Retrieval instance (lazy)
_rec = None
def _idx_base(): return Path(__file__).resolve().parents[2] / "data"
def _idx_path():  return str(_idx_base() / "ikarus_index")

@router.options("")
def preflight():  # clean preflight for browsers
    return Response(status_code=204)

@router.post("", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    global _rec
    base = _idx_base()
    if _rec is None:
        if not (base / "ikarus_index.index").exists():
            raise HTTPException(status_code=409, detail="Index not built. Call POST /ingest first.")
        _rec = Recommender(idx_path=_idx_path())
    items = _rec.search(req.query, k=req.k)
    return {"items": items}  # NO GENAI HERE

# -------- On-demand generation --------
class GenDescIn(BaseModel):
    title: str = ""
    brand: str = ""
    categories: list[str] = []
    color: str = ""
    material: str = ""
    package_dimensions: str = ""
    price: float | None = None

_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",  # fast & low-cost [switch to 'gemini-2.5-flash' for quality]
    api_key=_api_key,
    transport="rest",
    max_retries=0,  # avoid long backoff loops on free-tier 429
)

@router.post("/gen-desc")
def gen_desc(body: GenDescIn):
    prompt = (
        "Write a 60-90 word product design description for a catalog card.\n"
        f"Title: {body.title}\n"
        f"Brand: {body.brand}\n"
        f"Categories: {', '.join(body.categories[:4])}\n"
        f"Key specs: color={body.color}, material={body.material}, "
        f"dimensions={body.package_dimensions}, price={body.price}\n"
        "Focus on practical use-cases, materials, and style; avoid unverifiable claims."
    )
    try:
        r = _llm.invoke(prompt)
        text = getattr(r, "content", str(r))[:800]
        return {"gen_description": text}
    except Exception as e:
        raise HTTPException(status_code=429, detail=f"GenAI error: {e}")