from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

def _safe_str(v: Any) -> str:
    # Convert None/NaN/float to clean strings for joining
    try:
        if v is None:
            return ""
        s = str(v)
        s_low = s.strip().lower()
        if s_low in ("nan", "none", "null"):
            return ""
        return s.strip()
    except Exception:
        return ""

def _list_to_str(vals):
    if not vals:
        return ""
    try:
        return " ".join(_safe_str(x) for x in vals if _safe_str(x))
    except Exception:
        return ""

class TextEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def product_text(self, p: Dict) -> str:
        parts = [
            _safe_str(p.get("title")),
            _safe_str(p.get("description")),
            _list_to_str(p.get("categories")),
            _safe_str(p.get("brand")),
            _safe_str(p.get("material")),
            _safe_str(p.get("color")),
            # If you later want price included textually:
            # _safe_str(p.get("price")),
        ]
        # Join only non-empty strings
        parts = [x for x in parts if x]
        return " | ".join(parts)

    def encode(self, texts: List[str]):
        return self.model.encode(texts, normalize_embeddings=True)

    def encode_products(self, products: List[Dict]):
        texts = [self.product_text(p) for p in products]
        return self.encode(texts), texts
