import numpy as np
from typing import Any, Dict, List
from .vector_store import FaissStore
from .embed import TextEmbedder

def _safe_str(v: Any) -> str:
    try:
        if v is None:
            return ""
        s = str(v).strip()
        if s.lower() in ("nan","none","null"):
            return ""
        return s
    except Exception:
        return ""

def _safe_list(v: Any) -> List[str]:
    if isinstance(v, list):
        out = []
        for x in v:
            sx = _safe_str(x)
            if sx:
                out.append(sx)
        return out
    return []

def _safe_float(v: Any):
    try:
        s = str(v).strip()
        if s.lower() in ("nan","none","null",""):
            return None
        return float(s)
    except Exception:
        return None

class Recommender:
    def __init__(self, idx_path: str):
        self.emb = TextEmbedder()
        self.store = FaissStore(dim=384, path=idx_path)  # MiniLM-L6 dim
        self.store.load()

    def _to_product(self, raw: Dict, fallback_id: str) -> Dict:
        return {
            "uniq_id": _safe_str(raw.get("uniq_id")) or fallback_id,
            "title": _safe_str(raw.get("title")),
            "brand": _safe_str(raw.get("brand")),
            "description": _safe_str(raw.get("description")),
            "price": _safe_float(raw.get("price")),
            "categories": _safe_list(raw.get("categories")),
            "images": _safe_list(raw.get("images")),
            "manufacturer": _safe_str(raw.get("manufacturer")),
            "package_dimensions": _safe_str(raw.get("package_dimensions")),
            "country_of_origin": _safe_str(raw.get("country_of_origin")),
            "material": _safe_str(raw.get("material")),
            "color": _safe_str(raw.get("color")),
        }

    def search(self, query: str, k: int = 8):
        qv = self.emb.encode([query]).astype(np.float32)
        hits = self.store.search(qv, k)
        items = []
        for idx, score in hits:
            raw = self.store.meta[idx]
            product = self._to_product(raw, fallback_id=f"row_{idx}")
            items.append({"product": product, "score": float(score)})
        return items
